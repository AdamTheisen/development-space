import matplotlib
matplotlib.use('Agg')

import act
import glob
import matplotlib.pyplot as plt
import json
import numpy as np

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for KAZR data
site = 'sgp'
kazr_ds = site+'kazrgeC1.a1'
startdate = '2019-08-30'
enddate = '2019-08-30'

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

#Download KAZR Data
files = glob.glob(''.join(['./',kazr_ds,'/*cdf']))
if len(files) == 0:
    act.discovery.download_data(username, token, kazr_ds, startdate, enddate)
    files = glob.glob(''.join(['./',kazr_ds,'/*cdf']))

# Read in KAZR data to Standard Object
kazr = act.io.armfiles.read_netcdf(files)
kazr = kazr.resample(time='1min').nearest()

#Download STAMP Data
ds = site + 'stamppcpE13.b1'
files = glob.glob(''.join(['./',ds,'/*'+sdate+'*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, ds, startdate, enddate)
    files = glob.glob(''.join(['./',ds,'/*nc']))
stamp = act.io.armfiles.read_netcdf(files)
stamp = act.utils.data_utils.accumulate_precip(stamp, 'precip')

#Download STAMP Data
ds = site + 'stampE13.b1'
files = glob.glob(''.join(['./',ds,'/*'+sdate+'*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, ds, startdate, enddate)
    files = glob.glob(''.join(['./',ds,'/*nc']))
stamp2 = act.io.armfiles.read_netcdf(files)
stamp2['depth'].values = 0 - stamp2['depth'].values

#Download MET Data
ds = site + 'metE13.b1'
files = glob.glob(''.join(['./',ds,'/*'+sdate+'*cdf']))
if len(files) == 0:
    act.discovery.download_data(username, token, ds, startdate, enddate)
    files = glob.glob(''.join(['./',ds,'/*cdf']))
met = act.io.armfiles.read_netcdf(files)
met = act.utils.data_utils.accumulate_precip(met, 'tbrg_precip_total')

#Download WB Data
ds = site + 'wbpluvio2C1.a1'
files = glob.glob(''.join(['./',ds,'/*'+sdate+'*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, ds, startdate, enddate)
    files = glob.glob(''.join(['./',ds,'/*nc']))
wb = act.io.armfiles.read_netcdf(files)
wb = act.utils.data_utils.accumulate_precip(wb, 'intensity_rtnrt')

new = {'sgpkazrgeC1.a1': kazr, 'sgpmetE13.b1': met, 'sgpstamppcpE13.b1': stamp,
       'sgpwbpluvio2C1.b1': wb, 'sgpstampE13.b1': stamp2}

# Creat Plot Display
display = act.plotting.TimeSeriesDisplay(new,figsize=(10,15),subplot_shape=(3,))

# Plot first_cbh data in top plot
display.plot('reflectivity_copol',dsname='sgpkazrgeC1.a1',subplot_index=(0,), cmap='jet')
display.plot('precip_accumulated',dsname='sgpstamppcpE13.b1',subplot_index=(1,),label='STAMP TBRG')
display.plot('tbrg_precip_total_accumulated',dsname='sgpmetE13.b1',subplot_index=(1,), label='MET TBRG')
display.plot('intensity_rtnrt_accumulated',dsname='sgpwbpluvio2C1.b1',subplot_index=(1,), label='WBRG')
display.axes[1].legend()

display.plot('soil_specific_water_content_west',dsname='sgpstampE13.b1',subplot_index=(2,), cmap='ocean')
# Save figure
plt.savefig('./images/ldrd_example.png')
plt.clf()

display = act.plotting.WindRoseDisplay(met, figsize=(8,10))
display.plot('wdir_vec_mean','wspd_vec_mean',spd_bins=np.linspace(0, 10, 5), subplot_index=(0,))
plt.savefig('./images/ldrd_example_windrose.png')
plt.clf()

kazr.close()
stamp.close()
met.close()
wb.close()
stamp2.close()
