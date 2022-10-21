#!/usr/bin/env python
import act
import glob
import matplotlib.pyplot as plt
import json
import xarray as xr
import numpy as np

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Set up datastream name and dates to download
datastream = 'coraosaeth2spotM1.a1'
startdate = '2018-10-15'
enddate = '2019-04-30'
enddate = '2018-10-16'

#Download COR AOS CO Data
files = glob.glob(''.join(['./',datastream,'/*nc']))
if len(files) == 0:
    result = act.discovery.download_data(username, token, datastream, startdate, enddate)
    print(result)
    files = glob.glob(''.join(['./',datastream,'/*nc']))

#Read in CO data using ACT to Standard Object
aeth = act.io.armfiles.read_netcdf(files)

print(aeth)

datastream = 'coraospsap3w1sM1.b1'
#Download COR AOS CO Data
files = glob.glob(''.join(['./',datastream,'/*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*nc']))

#Read in CO data using ACT to Standard Object
psap = act.io.armfiles.read_netcdf(files)


#Plot CO Data
#display = act.plotting.TimeSeriesDisplay(obj,figsize=(15,10))
#display.plot('co',set_title=title)
#plt.show()

#Clean up QC to CF standard
aeth.clean.cleanup()
psap.clean.cleanup()
