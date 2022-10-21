import matplotlib
matplotlib.use('Agg')

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

#Specify datastream and date range for MET data
datastream = 'sgpmetE13.b1'
startdate = '2019-01-01'
enddate = '2019-01-07'

sdate='20190101'
#Download MET Data
files = glob.glob(''.join(['./data/',datastream,'/*'+sdate+'*cdf']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*cdf']))

#Read in MET data to Standard Object
met = act.io.armfiles.read_netcdf(files)
print(met)

#Get temp and rh for basic LCL calculation
met_temp = met.temp_mean
met_rh = met.rh_mean
met_lcl = (20.+met_temp/5.)*(100.-met_rh)

index = np.where(met_temp < -2.)[0]


#Add LCL data to MET object in meters
met['met_lcl'] = met_lcl
met['met_lcl'].attrs['units'] = 'm'
met['met_lcl'].attrs['long_name'] = 'LCL Calculated from SGP MET E13'

#Write LCL data out to netCDF file
met['met_lcl'].to_netcdf('./met_lcl.nc')

#Download, read, and display CEIL Data
datastream = 'sgpceilC1.b1'
files = glob.glob(''.join(['./data/',datastream,'/*'+sdate+'*']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*']))
files.sort()
ceil = act.io.armfiles.read_netcdf(files)
ceil = act.corrections.ceil.correct_ceil(ceil)

#Display data using plotting methods
new = {'sgpmetE13.b1': met, 'sgpceilC1.b1':ceil}
display = act.plotting.TimeSeriesDisplay(new,figsize=(8,5))
display.plot('met_lcl',dsname='sgpmetE13.b1',color='b')
display.day_night_background('sgpmetE13.b1')
set_title = ' '.join(['MET LCL and CEIL CBH on',
    act.utils.datetime_utils.numpy_to_arm_date(met.time.values[0])])
display.plot('first_cbh',dsname='sgpceilC1.b1',color='g',set_title=set_title)
display.set_yrng([0,7500])
display.axes[0].plot(met['time'].values[index], np.full(len(index), display.axes[0].get_ylim()[0]), '|r')
display.axes[0].legend()
plt.savefig('./images/lcl.png')
plt.clf()

#Plot out background and MET LCL Overlay
display2 = act.plotting.TimeSeriesDisplay(new,figsize=(8,5))
display2.plot('backscatter','sgpceilC1.b1')
set_title = ' '.join(['MET LCL and CEIL Backscatter on',
    act.utils.datetime_utils.numpy_to_arm_date(met.time.values[0])])
display2.plot('met_lcl','sgpmetE13.b1',color='r',set_title=set_title)
display2.set_yrng([0,7500])
#display.axes[0].legend()
plt.savefig('./images/lcl_bs.png')

met.close()
ceil.close()
