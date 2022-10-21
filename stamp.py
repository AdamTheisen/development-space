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
obj_ds = site+'stampE13.b1'
startdate = '2019-08-30'
enddate = startdate

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

#Download KAZR Data
files = glob.glob(''.join(['./',obj_ds,'/*'+sdate+'*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, obj_ds, startdate, enddate)
    files = glob.glob(''.join(['./',obj_ds,'/*'+sdate+'*nc']))

#Read in KAZR data to Standard Object
obj = act.io.armfiles.read_netcdf(files)

display = act.plotting.TimeSeriesDisplay(obj,figsize=(15,10))
display.plot('soil_specific_water_content_west',dsname=obj_ds, cmap='jet', force_line_plot=True, linestyle='solid')
plt.savefig('./images/stamp.png')
plt.clf()
