import matplotlib

import act
import glob
import matplotlib.pyplot as plt
import json
import xarray as xr
import numpy as np
import sys
import pyproj

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for MET data
datastream = 'maraosmetM1.a1'
startdate = '2018-02-01'
enddate = '2018-03-01'

sdate=''.join(startdate.split('-'))
sdate = '20180201'
#Download MET Data
ddir = './data/'+datastream
files = glob.glob(ddir+'/*'+sdate+'*nc')
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate,output=ddir)
    files = glob.glob(ddir+'/*nc')

files.sort()
#Read in MET data to Standard Object
aosmet = act.io.armfiles.read_netcdf(files, parallel=True)
aosmet = aosmet.sortby('time')

_, index = np.unique(aosmet['time'], return_index=True)
aosmet = aosmet.isel(time=index)
aosmet = aosmet.resample(time='1min').nearest()
aosmet.to_netcdf('./data/maraosmetM1.a1.20180201.000000.nc')

#Download NAV Data
nav_ds = 'marnavM1.a1'
ddir = './data/'+nav_ds
files = glob.glob(ddir+'/*'+sdate+'*nc')
if len(files) == 0:
    act.discovery.download_data(username, token, nav_ds, startdate, enddate,output=ddir)
    files = glob.glob(ddir+'/**nc')
files.sort()

nav = act.io.armfiles.read_netcdf(files, parallel=True)
nav = nav.sortby('time')
_, index = np.unique(nav['time'], return_index=True)
nav = nav.isel(time=index)
nav = nav.resample(time='1min').nearest()

nav.to_netcdf('./data/marnavM1.20180201.000000.a1')

nav = act.utils.ship_utils.calc_cog_sog(nav)

obj = xr.merge([nav, aosmet],compat='override')

obj = act.corrections.ship.correct_wind(obj)

#Download NAV Data
nav_ds = 'marsondewnpnM1.b1'
ddir = './data/'+nav_ds
files = glob.glob(ddir+'/*'+sdate+'*cdf')
if len(files) == 0:
    act.discovery.download_data(username, token, nav_ds, startdate, enddate,output=ddir)
    files = glob.glob(ddir+'/**cdf')
files.sort()

s_time = []
s_dir = []
s_spd = []
for f in files:
    sonde = act.io.armfiles.read_netcdf(f, parallel=True)
    s_time.append(sonde['time'].values[0])
    s_dir.append(np.mean(sonde['deg'].values[0:20]))
    s_spd.append(np.mean(sonde['wspd'].values[0:20]))


obj.close()
nav.close()
aosmet.close()

xlim = [obj['time'].values[0], obj['time'].values[-1]]

fig, ax = plt.subplots(4,1,figsize=(15,10))
ax[0].plot(aosmet['time'], aosmet['wind_direction'], '.', label='Uncorrected')
ax[0].plot(obj['time'], obj['wind_direction_corrected'], '.', label='Corrected')
ax[0].plot(s_time,s_dir, '.r', label='Sonde', markersize=10)
ax[0].set_xlim(xlim)
ax[0].set_title('Wind Direction')
ax[0].legend()
ax[1].plot(aosmet['time'], aosmet['wind_speed'], '.', label='Uncorrected')
ax[1].plot(obj['time'], obj['wind_speed_corrected'], label='Corrected')
ax[1].plot(s_time, s_spd, '.r', label='Sonde', markersize=10)
ax[1].set_xlim(xlim)
ax[1].set_title('Wind Speed')
ax[2].plot(obj['time'], obj['course_over_ground'])
ax[2].set_xlim(xlim)
ax[2].set_title('Course Over Ground')
ax[3].plot(obj['time'], obj['speed_over_ground'])
ax[3].set_xlim(xlim)
ax[3].set_title('Speed Over Ground')
plt.tight_layout()
plt.show()
