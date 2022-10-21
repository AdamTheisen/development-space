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

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for MET data
datastream = 'olimplpolfsM1.b1'
startdate = '2019-12-31'
enddate = '2019-12-31'

#Download MPL Data
files = glob.glob(''.join(['./',datastream,'/*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*nc']))


files.sort()
#Read in MET data to Standard Object
mpl = act.io.armfiles.read_netcdf(files)
mpl = mpl.resample(time='1min').nearest()


mpl2 = act.corrections.mpl.correct_mpl(mpl)
#Plot out background and MET LCL Overlay
print('Plotting')
display = act.plotting.TimeSeriesDisplay({'corrected': mpl2, 'uncorrected': mpl},figsize=(15,8),subplot_shape=(2,))
display.fig.subplots_adjust(bottom=0.05, top=0.95)
display.plot('signal_return_co_pol', dsname='uncorrected',
             cmap='jet', subplot_index=(0,))
#Set Height as Dimension
#mpl.range_bins.values = mpl.height.values
display.plot('signal_return_co_pol', dsname='corrected',
             vmin=-20, vmax=20, cmap='jet', subplot_index=(1,))
display.set_yrng([0,15])
plt.savefig('./images/mpl_cor.png')

mpl.close()
