import matplotlib
#matplotlib.use('Agg')

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
datastream = 'sgpceil10mC1.b1'
startdate = '2024-07-17'
enddate = '2024-07-17'

#Download MPL Data
files = glob.glob(''.join(['./',datastream,'/*nc']))
if len(files) == 0:
    act.discovery.download_arm_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*nc']))

#Read in data to Standard Object
ceil = act.io.arm.read_arm_netcdf(files)
ceil = act.corrections.ceil.correct_ceil(ceil)

datastream = 'sgpmplpolfsC1.b1'
files = glob.glob(''.join(['./',datastream,'/*nc']))
if len(files) == 0:
    act.discovery.download_arm_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*nc']))
mpl = act.io.arm.read_arm_netcdf(files)
mpl = act.corrections.mpl.correct_mpl(mpl)
mpl = mpl.resample(time='1min').nearest()
#Set Height as Dimension
mpl = mpl.assign_coords(range_bins=(mpl.height.values))

datastream = 'sgpdlfptE13.b1'
files = glob.glob(''.join(['./',datastream,'/*cdf']))
if len(files) == 0:
    act.discovery.download_arm_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*cdf']))
#Read in data to Standard Object
dl = act.io.arm.read_arm_netcdf(files)
dl = act.corrections.doppler_lidar.correct_dl(dl)
dl = dl.resample(time='1min').nearest()

datastream = 'sgphsrlC1.a1'
files = glob.glob(''.join(['./',datastream,'/*nc']))
if len(files) == 0:
    act.discovery.download_arm_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*nc']))
#Read in data to Standard Object
hsrl = act.io.arm.read_arm_netcdf(files)
hsrl = hsrl.resample(time='1min').nearest()
hsrl['beta_a_backscatter'].values = np.log10(hsrl['beta_a_backscatter'].values)
hsrl['beta_a_1064_backscatter'].values = np.log10(hsrl['beta_a_1064_backscatter'].values)

datastream = 'sgprlproftemp2news10mC1.c0' # 'sgprlprofmerge2newsC1.c0'
files = glob.glob(''.join(['./',datastream,'/*nc']))
if len(files) == 0:
    act.discovery.download_arm_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*nc']))
#Read in data to Standard Object
rl = act.io.arm.read_arm_netcdf(files)
rl = rl.resample(time='1min').nearest()
#Plot out background and MET LCL Overlay
print('Plotting')

#trange = [np.datetime64("2014-07-17T06:00:00"), np.datetime64("2024-07-17T12:00:00")]
display = act.plotting.TimeSeriesDisplay((ceil, mpl, dl, hsrl, rl),figsize=(10,12),subplot_shape=(5,), sharex=True)
display.fig.subplots_adjust(bottom=0.05, top=0.95)
display.plot('backscatter',dsname='sgpceil10mC1.b1',
             vmin=0, vmax=4, cvd_friendly=True, subplot_index=(0,))
display.axes[0].set_ylim([0,7000])
#display.axes[0].set_xlim(trange)
display.plot('signal_return_cross_pol',dsname='sgpmplpolfsC1.b1',
             vmin=-20, vmax=15, cvd_friendly=True, subplot_index=(1,))
display.axes[1].set_ylim([0,7])
#display.axes[1].set_xlim(trange)
display.plot('radial_velocity',dsname='sgpdlfptE13.b1',
             vmin=-5, vmax=5, cmap='seismic', subplot_index=(2,))
display.axes[2].set_ylim([0,7000])
#display.axes[2].set_xlim(trange)
#display.plot('depolarization_counts_high',dsname='sgprlprofmerge2newsC1.c0',
display.plot('temperature',dsname='sgprlproftemp2news10mC1.c0',
             vmin=270, vmax=310, cvd_friendly=True, subplot_index=(3,))
display.axes[3].set_ylim([0,7])

display.plot('color_ratio',dsname='sgphsrlC1.a1',
              vmin=0, vmax=10, cvd_friendly=True, subplot_index=(4,))
display.axes[4].set_ylim([0,7000])
#display.axes[3].set_xlim(trange)
#plt.show()
plt.savefig('./images/triennial_lidar.png')

ceil.close()
