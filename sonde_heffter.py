import numpy as np
import act
import glob
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from operator import itemgetter
from itertools import groupby
from act.utils.data_utils import convert_to_potential_temp

date = '.20210'
base = 5  # 5 mb base
file = glob.glob('./Data/sgpsondewnpnC1.b1/*'+date+'*')
file.sort()

time = []
pbl = []
act_pbl = []
vap_pbl = []
vap_liu = []

temperature='tdry'
pressure='pres'
height='alt'
smooth_height=3
land_parameter=True
for f in file:
    d = '.'.join(f.split('.')[-3:])
    file2 = glob.glob('./Data/sgppblhtsonde1mcfarlC1.c1/*'+d+'*')[0]

    obj2 = act.io.armfiles.read_netcdf(file2)
    if np.isnan(obj2['pbl_height_heffter'].values):
        continue

    ds = act.io.armfiles.read_netcdf(f)
    test_obj = act.retrievals.sonde.calculate_pbl_heffter(ds)

    time.append(ds['time'].values[0])
    act_pbl.append(test_obj['pblht_heffter'].values)
    vap_pbl.append(obj2['pbl_height_heffter'].values)
    vap_liu.append(obj2['pbl_height_liu_liang'].values)
    print('Bottom Inversion ', obj2['bottom_inversion'].values)
    print('Top Inversion ', obj2['top_inversion'].values)
    print('Delta Theta Max ', obj2['delta_theta_max'].values)
    print('Lapse Rate ', obj2['lapserate_max'].values)
    print(obj2['pbl_height_heffter'].values)

fig, ax = plt.subplots()
ax.plot(time, act_pbl, label='ACT')
ax.plot(time, vap_pbl, label='VAP')
ax.plot(time, vap_liu, label='VAP Liu')
plt.legend()
plt.show()

diff = [i - j for i, j in zip(act_pbl, vap_pbl)]
print(diff)
print(np.nanmean(diff))
print(np.nanmedian(diff))

from sklearn.metrics import mean_squared_error
rms = mean_squared_error(act_pbl, vap_pbl, squared=False)
print(rms)
