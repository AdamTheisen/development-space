import matplotlib
matplotlib.use('Agg')

import act
import glob
import xarray as xr
import pandas as pd
import datetime as dt
import json
import matplotlib.pyplot as plt

# Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

# Set year to process
year = '2019'

#Specify datastream and date range for MET data
datastream = 'nsametC1.b1'
startdate = year+'-01-01'
enddate = year+'-12-31'

#Download MET Data
files = glob.glob(''.join(['./',datastream,'/*'+year+'*cdf']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*'+year+'*cdf']))

#Read in MET data to Standard Object
met = act.io.armfiles.read_netcdf(files)

#Specify datastream and date range for MAWS data
datastream = 'nsamawsC1.b1'
startdate = year+'-01-01'
enddate = year+'-12-31'

#Download MAWS Data
files = glob.glob(''.join(['./',datastream,'/*'+year+'*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*'+year+'*nc']))

#Read in MAWS data to Standard Object
maws = act.io.armfiles.read_netcdf(files)

# Get already downloaded NOAA files
noaa_files = glob.glob('./data/met_brw/*'+year+'*txt')
noaa_files.sort()

# Define header for NOAA files
header = ['site','year','month','day','hour','minute','wind_direction',
          'wind_speed','wind_steadiness','pressure','temperature_2m',
          'temperature_10m','temperature_tt','relative_humidity',
          'precipitation_intensity']

# Run through NOAA files for specified year and create temp variable
t = []
temp = []
for f in noaa_files:
    obj = act.io.csvfiles.read_csv(f,'\s+',column_names=header)
    df = pd.DataFrame({'year': obj.year, 'month': obj.month,
                  'day': obj.day, 'hour': obj.hour, 'minute': obj.minute})
    time = pd.to_datetime(df)
    obj['time'] = time.to_xarray()
    obj = obj.set_index({'index': 'time'})
    obj = obj.where(obj['temperature_2m'] > -100.)
    temp += list(obj['temperature_2m'].values)
    t += list(obj['index'].values)

#Put data into data array
noaa = xr.DataArray(temp, coords={'time':t}, dims=['time'])
noaa.attrs['units'] = 'C'
noaa.attrs['long_name'] = 'NOAA 2m Temperature at Barrow'
noaa = xr.Dataset({'noaa_temp': noaa})


# Plot data out
new = {'nsametC1.b1': met, 'nsamawsC1.b1':maws, 'noaaftp':noaa}
display = act.plotting.TimeSeriesDisplay(new,figsize=(15,10))
display.plot('temp_mean',dsname='nsametC1.b1',color='k')
display.plot('atmospheric_temperature',dsname='nsamawsC1.b1',color='b', markersize=1)
display.plot('noaa_temp',dsname='noaaftp',color='y', marker=',')
plt.savefig('./images/barrow_arm_noaa_'+year+'.png')
