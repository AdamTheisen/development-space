import act
import glob
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file = './detections.txt'
ds_detect = act.io.read_csv(file, sep='\t', index_col=0, header=0, infer_datetime_format=True)

ds_detect = ds_detect.drop_duplicates(dim='time')
time = pd.to_datetime(ds_detect['time'].values)
ds_detect = ds_detect.assign_coords({'time': time})

files = glob.glob('./data/enaaoscpcfC1.b1/*')
ds_cpc = act.io.read_netcdf(files)

files = glob.glob('./data/enaaoscoC1.b1/*')
ds_co = act.io.read_netcdf(files)

files = glob.glob('./data/enaaosmetC1.a1/*')
ds_aosmet = act.io.read_netcdf(files)

ds = xr.merge([ds_cpc, ds_co, ds_detect, ds_aosmet])

detection = ds_detect['detection'].values
idx = np.where(detection == 'aeroplane')[0]

display = act.plotting.TimeSeriesDisplay(ds, subplot_shape=(3,))
display.plot('concentration', subplot_index=(0,))
display.axes[0].plot(ds_detect['time'].values, np.full(len(ds_detect['time'].values), 0), 'r|', markersize=15)
display.axes[0].plot(ds_detect['time'].values[idx], np.full(len(ds_detect['time'].values[idx]), 0), 'y|', markersize=15)

title = 'ENA CO'
display.plot('co', subplot_index=(1,), set_title=title)
display.axes[1].plot(ds_detect['time'].values, np.full(len(ds_detect['time'].values), 0.08), 'r|', markersize=15)
display.axes[1].plot(ds_detect['time'].values[idx], np.full(len(idx), 0.08), 'y|', markersize=15)

title = 'ENA Wind Direction'
display.plot('wind_direction', subplot_index=(2,), set_title=title)
display.axes[2].plot(ds_detect['time'].values, np.full(len(ds_detect['time'].values), 0.0), 'r|', markersize=15)
display.axes[2].plot(ds_detect['time'].values[idx], np.full(len(idx), 0.0), 'y|', markersize=15)
plt.show()
