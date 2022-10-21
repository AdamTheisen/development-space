import matplotlib

import act
import glob
import matplotlib.pyplot as plt
import json
import xarray as xr
import numpy as np
import sys

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for MET data
datastream = 'sgpvdisE13.b1'
startdate = '2019-08-09'
enddate = '2019-08-09'

sdate='20190809'
#Download MET Data
files = glob.glob(''.join(['./data/',datastream,'/*'+sdate+'*cdf']))

#Read in MET data to Standard Object
vdis = act.io.armfiles.read_netcdf(files)
obj = act.io.armfiles.create_obj_from_arm_dod('vdis.b1', {'time': 1440}, scalar_fill_dim='time')

print(obj)

for v in vdis:
    obj[v].values = vdis[v].values

for v in vdis.dims:
    obj.coords[v] = vdis[v].values

obj.to_netcdf('./data/pcm.nc')

new_obj = act.io.armfiles.read_netcdf('./data/pcm.nc')

display = act.plotting.TimeSeriesDisplay(new_obj,figsize=(8,5))
display.plot('num_drops')
plt.show()
