import glob
import act
import pandas as pd
import numpy as np
from scipy.interpolate import griddata, Rbf
import matplotlib.pyplot as plt


files = glob.glob('./sgpsondewnpnC1.b1/*20210630*')
obj = act.io.armfiles.read_netcdf(files)

time = obj['time'].values
height = obj['alt'].values
temp = obj['tdry'].values

xgrid = pd.date_range(time[0], time[-1], freq='1min')
ygrid = np.arange(0, 15000, 20)

grid_x, grid_y = np.meshgrid(xgrid, ygrid)
grid = griddata((time, height), temp, (grid_x, grid_y), method='cubic')

grid = np.zeros([len(xgrid), len(ygrid)])

print(grid)

#plt.pcolormesh(grid_x, grid_y, grid, cmap='act_HomeyerRainbow')
#plt.colorbar()
#plt.show()
