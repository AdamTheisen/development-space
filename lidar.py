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
datastream = 'nsaceil10mC1.b1'
startdate = '2019-06-28'
enddate = '2019-06-28'

#Download MPL Data
files = glob.glob(''.join(['./',datastream,'/*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*nc']))

#Read in data to Standard Object
ceil = act.io.armfiles.read_netcdf(files)
ceil = act.corrections.ceil.correct_ceil(ceil)

datastream = 'nsamplpolfsC1.b1'
files = glob.glob(''.join(['./',datastream,'/*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*nc']))
mpl = act.io.armfiles.read_netcdf(files)
mpl = act.corrections.mpl.correct_mpl(mpl)
#mpl = mpl.resample(time='1min').nearest()
#Set Height as Dimension
mpl = mpl.assign_coords(range_bins=(mpl.height.values))

datastream = 'nsadlfptC1.b1'
files = glob.glob(''.join(['./',datastream,'/*cdf']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*cdf']))
#Read in data to Standard Object
dl = act.io.armfiles.read_netcdf(files)
dl = act.corrections.doppler_lidar.correct_dl(dl)
#dl = dl.resample(time='1min').nearest()

datastream = 'nsahsrlC1.a1'
files = glob.glob(''.join(['./',datastream,'/*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*nc']))
#Read in data to Standard Object
hsrl = act.io.armfiles.read_netcdf(files)
#hsrl = hsrl.resample(time='1min').nearest()
hsrl['beta_a_backscatter'].values = np.log10(hsrl['beta_a_backscatter'].values)

#Plot out background and MET LCL Overlay
print('Plotting')

trange = [np.datetime64("2019-06-28T06:00:00"), np.datetime64("2019-06-28T09:00:00")]
display = act.plotting.TimeSeriesDisplay((ceil, mpl, dl, hsrl),figsize=(5,12),subplot_shape=(4,), sharex=True)
display.fig.subplots_adjust(bottom=0.05, top=0.95)
display.plot('backscatter',dsname='nsaceil10mC1.b1',
             vmin=0, vmax=4, cmap='jet', subplot_index=(0,))
display.axes[0].set_ylim([0,7000])
display.axes[0].set_xlim(trange)
display.plot('signal_return_co_pol',dsname='nsamplpolfsC1.b1',
             vmin=-20, vmax=15, cmap='jet', subplot_index=(1,))
display.axes[1].set_ylim([0,7])
display.axes[1].set_xlim(trange)
display.plot('attenuated_backscatter',dsname='nsadlfptC1.b1',
             vmin=-10, vmax=0, cmap='jet', subplot_index=(2,))
display.axes[2].set_ylim([0,7000])
display.axes[2].set_xlim(trange)
display.plot('beta_a_backscatter',dsname='nsahsrlC1.a1',
             vmin=-10, vmax=0,cmap='jet', subplot_index=(3,))
display.axes[3].set_ylim([0,7000])
display.axes[3].set_xlim(trange)
plt.show()
#plt.savefig('./images/triennial_core.png')

ceil.close()
