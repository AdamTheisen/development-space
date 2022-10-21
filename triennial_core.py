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

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for MET data
datastream = 'sgpkazrcfrgeC1.a1'
startdate = '2020-05-21'
enddate = '2020-05-21'

files = glob.glob(''.join(['./',datastream,'/*.1200*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*1200*nc']))

files.sort()
kazr = act.io.armfiles.read_netcdf(files)

#Plot out background and MET LCL Overlay
display = act.plotting.TimeSeriesDisplay(kazr, subplot_shape=(1,), figsize=(10,7))
display.plot('reflectivity',dsname='sgpkazrcfrgeC1.a1',
             vmin=-40, vmax=40, cmap='act_HomeyerRainbow', subplot_index=(0,))
plt.tight_layout()
plt.show()
#plt.savefig('./images/triennial_core.png')
