import matplotlib
matplotlib.use('Agg')

import act
import glob
import matplotlib.pyplot as plt
import json
import sys

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for KAZR data
site = 'sgp'
kazr_ds = site+'kazrgeC1.a1'
startdate = '2019-05-29'
enddate = startdate

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

#Download KAZR Data
files = glob.glob(''.join(['./',kazr_ds,'/*'+sdate+'*cdf']))
if len(files) == 0:
    act.discovery.download_data(username, token, kazr_ds, startdate, enddate)
    files = glob.glob(''.join(['./',kazr_ds,'/*'+sdate+'*cdf']))

#Read in KAZR data to Standard Object
kazr = act.io.armfiles.read_netcdf(files)
kazr = kazr.resample(time='1min').nearest()
kazr = act.retrievals.cbh.generic_sobel_cbh(kazr,variable='reflectivity_copol',
                                            height_dim='range', var_thresh=-10.)

#Display data using plotting methods
display = act.plotting.TimeSeriesDisplay(kazr,figsize=(15,10))
display.plot('reflectivity_copol',dsname=kazr_ds, cmap='jet')
#display.plot('signal_return_co_pol',dsname=site+'mplpolfsC1.b1', cmap='jet')
plt.savefig('./images/kazr_cmap.png')
plt.clf()
