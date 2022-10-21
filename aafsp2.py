import matplotlib
#matplotlib.use('Agg')


import act
import glob
import matplotlib.pyplot as plt
import json
import xarray as xr
import sys
import datetime as dt
import numpy as np


#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for MET data
datastream = 'coraafsp2rbc10sF1.c1'
startdate = '2018-11-04'
enddate = '2018-12-09'
campaign = 'CACTI'

#datastream = 'enaaafsp2rbc10sF1.c1'
#startdate = '2018-01-01'
#enddate = '2018-12-31'
#campaign = 'ACE-ENA'

#Download MPL Data
files = glob.glob(''.join(['./',datastream,'/*2018*nc']))
#if len(files) == 0:
#act.discovery.download_data(username, token, datastream, startdate, enddate)
#files = glob.glob(''.join(['./',datastream,'/*2018*nc']))

files.sort()

obj = act.io.armfiles.read_netcdf(files)

#fig, ax = plt.subplots(figsize=(7, 8))
#sc = ax.scatter(obj['rBC'], obj['alt'], c=obj['time'].values)
#ax.set_title(campaign+' AAF Refractory Black Carbon')
#ax.set_xlabel('Refractory Black Carbon (ng m^-3)')
#ax.set_ylabel('Altitude (m)')
#ax.set_xlim([0,500])
#ax.set_ylim([0,6500])
#cbar = plt.colorbar(sc)
#cbar.ax.set_yticklabels(pd.to_datetime(cbar.get_ticks()).strftime(date_format='%d/%m/%Y'))
#cbar.ax.set_ylabel('Date', rotation=90)
#plt.show()

#fig, ax = plt.subplots(figsize=(7,8))
#rng = [0, 500]
#xbin = range(500)[0::10]
#ybin = range(6500)[0::250]
#hist, x, y = np.histogram2d(obj['rBC'], obj['alt'], bins=(xbin, ybin))
#
#h = ax.hist2d(obj['rBC'], obj['alt'], bins=(xbin, ybin), cmin=0, cmax=2000, norm=matplotlib.colors.LogNorm())
#plt.show()

display = act.plotting.GeographicPlotDisplay(obj)
display.geoplot('rBC', s=1, vmin=0, vmax=100)
plt.show()

obj.close()
sys.exit()
fig, ax = plt.subplots(figsize=(7,8), nrows=6, sharex=True)
xbin = range(500)[0::10]
h = ax[5].hist(obj['rBC'].where(obj['alt'].values <= 1000.), bins=xbin, log=True)
ax[5].set_xlim([0,500])

idx = ((obj['alt'].values > 1000.) & (obj['alt'].values <= 2000.))
ind = np.where(idx)
h = ax[4].hist(obj['rBC'].values[ind], bins=xbin, log=True)
ax[4].set_xlim([0,500])

idx = ((obj['alt'].values > 2000.) & (obj['alt'].values <= 3000.))
ind = np.where(idx)
h = ax[3].hist(obj['rBC'].values[ind], bins=xbin, log=True)
ax[3].set_xlim([0,500])

idx = ((obj['alt'].values > 3000.) & (obj['alt'].values <= 4000.))
ind = np.where(idx)
h = ax[2].hist(obj['rBC'].values[ind], bins=xbin, log=True)
ax[2].set_xlim([0,500])

idx = ((obj['alt'].values > 4000.) & (obj['alt'].values <= 5000.))
ind = np.where(idx)
h = ax[1].hist(obj['rBC'].values[ind], bins=xbin, log=True)
ax[1].set_xlim([0,500])

idx = (obj['alt'].values > 5000.)
ind = np.where(idx)
h = ax[0].hist(obj['rBC'].values[ind], bins=xbin, log=True)
ax[0].set_xlim([0,500])

plt.show()
obj.close()
