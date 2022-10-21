import matplotlib
matplotlib.use('Agg')

import act
import glob
import matplotlib.pyplot as plt
import json
import xarray as xr

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for MET data
datastream = 'cormetM1.b1'
startdate = '2019-02-15'
enddate = '2019-03-01'

#Download MET Data
files = glob.glob(''.join(['./',datastream,'/*2019020*cdf']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*cdf']))
#Read in MET data to Standard Object
met = act.io.armfiles.read_netcdf(files)

#Specify datastream and date range for MET data
datastream = 'coraosmetM1.a1'
#Download MET Data
files = glob.glob(''.join(['./',datastream,'/*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*2019020*nc']))
#Read in MET data to Standard Object
aosmet = act.io.armfiles.read_netcdf(files)

#Specify datastream and date range for MET data
datastream = 'corsondewnpnM1.b1'
#Download MET Data
files = glob.glob(''.join(['./',datastream,'/*cdf']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*2019020*cdf']))
#Read in MET data to Standard Object
sonde_data = []
sonde_data10m = []
sonde_time = []
for f in files:
    sonde = act.io.armfiles.read_netcdf(f)
    sonde_data.append(sonde['tdry'].values[0])
    sonde_data10m.append(sonde['tdry'].values[2])
    sonde_time.append(sonde['time'].values[0])

#Display data using plotting methods
new = {'cormetM1.b1': met, 'coraosmetM1.a1':aosmet}
display = act.plotting.TimeSeriesDisplay(new,figsize=(15,10))
set_title = ' '.join(['COR MET, AOSMET, and SONDE Temperature Comparison'])
display.plot('temp_mean',dsname='cormetM1.b1',color='b')
display.plot('temperature_ambient',dsname='coraosmetM1.a1',color='g',set_title=set_title)
display.day_night_background('cormetM1.b1')
display.axes[0].plot(sonde_time,sonde_data,'.r',markersize=15)
display.axes[0].plot(sonde_time,sonde_data10m,'.c',markersize=15)
    
#display.plot('first_cbh',dsname='sgpceilC1.b1',color='g',set_title=set_title)
display.set_yrng([5,35])
display.axes[0].legend()
plt.savefig('./cor_met.png')
