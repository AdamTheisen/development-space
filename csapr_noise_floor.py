import matplotlib.pyplot as plt
import pyart
import numpy as np
import glob
import dask
import pandas as pd

def get_radar_min(filename):
    radar = pyart.io.read(filename)
    eind = radar.sweep_end_ray_index['data'][0]
    sind = radar.sweep_start_ray_index['data'][0]

    data = radar.fields['reflectivity']['data']
    min_0 = np.nanmean(data[sind:eind,:])
    min_all = np.nanmean(data)

    t = pd.to_datetime(radar.time['units'].split(' ')[-1])

    return t, min_0, min_all


files = glob.glob('./data/sgpcsaprsurI7.00/sur/20110520/*.mdv')
#files = glob.glob('./data/sgpcsaprsurI7.00/sur/20170306/*.nc')

min_0 = []
min_all = []

files.sort()
task = []
for f in files:
    a = dask.delayed(get_radar_min)(f)
    task.append(a)

data = dask.compute(task)
time = [t[0] for t in data[0]]
min_0 = [t[1] for t in data[0]]
min_all = [t[2] for t in data[0]]

plt.plot(time, min_0, '.-b', label='Sweep 0 Min')
plt.plot(time, min_all, '.-g', label='Volume Min')
plt.legend()
plt.show()
