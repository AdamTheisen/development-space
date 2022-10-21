import matplotlib
matplotlib.use('Agg')

import sys
sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')

import act
print(act.__file__)
import glob
import matplotlib.pyplot as plt
import json

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for KAZR data
site = 'sgp'
kazr_ds = site+'kazrgeC1.a1'
startdate = '2019-05-29'
enddate = '2019-05-31'

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

#Download KAZR Data
files = glob.glob(''.join(['./data/',kazr_ds,'/*cdf']))
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
display.plot('reflectivity_copol', cmap='jet')
plt.savefig('./images/ceil_comp.png')
plt.clf()
