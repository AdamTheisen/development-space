
#https://journals.ametsoc.org/view/journals/atot/35/4/jtech-d-17-0107.1.xml
import act
import glob
import numpy as np
from scipy.interpolate import griddata
import pandas as pd
import matplotlib.pyplot as plt

files = glob.glob('./data/sgpirtE13.b1/*.2024*')
ds_irt = act.io.read_arm_netcdf(files)


files = glob.glob('./data/sgpsondewnpnC1.b1/*.2024*')
time = []
data = []
height = []
for f in [files[2]]:
    ds_sonde = act.io.read_arm_netcdf(f)
    time += list(ds_sonde['time'].values)
    data += list(ds_sonde['tdry'].values)
    height += list(ds_sonde['alt'].values)

grid_yi = np.arange(0, 8000, 10)
grid_xi = pd.date_range(time[0], time[-1], freq='min')

grid_x, grid_y = np.meshgrid(grid_xi, grid_yi)

height = np.array(height)
data = np.array(data)
#grid = griddata((time, height), data + 273.15, (grid_x, grid_y), method='linear')
#plt.subplot(111)
#plt.contourf(grid_xi, grid_yi, grid, 50)
#plt.scatter(time, height, data)
#plt.colorbar()
#plt.show()
cbh_irt = []
sig_clear = []
tbc = []
for i in range(len(ds_irt['time'].values)):
    index = np.nanargmin(np.abs((ds_sonde['tdry'].values + 273.15) - ds_irt['sky_ir_temp'].values[i]))
    cbh_irt.append(ds_sonde['alt'].values[index])

    sig_clear.append(0.09789 - 0.0008875 * ds_irt['sky_ir_temp'].values[i] -3.74e-6 * ds_irt['sky_ir_temp'].values[i] ** 2 - 3.883e-7 * ds_irt['sky_ir_temp'].values[i] **3)
#    index = np.nanargmin(np.abs(grid_xi - ds_irt['time'].values[i]))
#    try:
#        index2 = np.nanargmin(np.abs(grid[:, index] - ds_irt['sky_ir_temp'].values[i]))
#        cbh_irt.append(grid_yi[index2])
#    except:
#        cbh_irt.append(np.nan)

df = pd.DataFrame(sig_clear, ds_irt['time'].values).rolling('10min').std()
df['cbh'] = cbh_irt
df = df[df[0] < 0.05]
df = df[df['cbh'] < 10000]

files = glob.glob('./data/sgpceil10mC1.b1/*.2024*')
ds_ceil = act.io.read_arm_netcdf(files)
plt.subplot(311)
plt.plot(ds_irt['time'].values, ds_irt['sky_ir_temp'].values)
plt.subplot(312)
plt.plot(df.index, df['cbh'])
plt.plot(ds_ceil['time'].values, ds_ceil['first_cbh'].values, '.')
plt.subplot(313)
plt.plot(df.index, df[0])
plt.show()
