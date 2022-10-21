import matplotlib
matplotlib.use('Agg')

import act
import glob
import matplotlib.pyplot as plt
import json
import xarray as xr
import sys
import datetime as dt
import pandas as pd
import numpy as np

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for MET data
datastream = 'sgpdlprofwind4newsC1.c1'
startdate = '2018-05-20'
enddate = '2018-05-20'

#Download MPL Data
files = glob.glob(''.join(['./',datastream,'/*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*nc']))

files.sort()
#Read in MET data to Standard Object
obj = act.io.armfiles.read_netcdf(files)

obj = act.corrections.doppler_lidar.correct_dl(obj, var_name='mean_snr')

#Plot out background and MET LCL Overlay
display = act.plotting.TimeSeriesDisplay(obj,figsize=(15,15),subplot_shape=(4,))
display.fig.subplots_adjust(bottom=0.05, top=0.95)
display.plot('wind_speed',vmin=0, vmax=30, cmap='jet', subplot_index=(0,))
display.axes[0].set_ylim([0,3000])
display.plot('wind_direction',vmin=0, vmax=360, cmap='jet', subplot_index=(1,))
display.axes[1].set_ylim([0,3000])
display.plot('w', vmin=-2.0, vmax=2, cmap='seismic', subplot_index=(2,))
display.axes[2].set_ylim([0,3000])
display.plot('mean_snr', cmap='jet', subplot_index=(3,))
display.axes[3].set_ylim([0,3000])

plt.savefig('./images/dlprof.png')
