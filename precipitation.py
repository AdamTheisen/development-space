import matplotlib
matplotlib.use('Agg')

import act
import glob
import matplotlib.pyplot as plt
import json
import xarray as xr
import numpy as np
import sys
from itertools import accumulate

# Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

# Specify dictionary of datastreams, variables, and weights
cf_ds = {'sgpmetE13.b1': {'variable': ['tbrg_precip_total', 'org_precip_rate_mean', 
                                       'pwd_precip_rate_mean_1min'], 
                          'weight': [0.25, 0.05, 0.0125]},
         'sgpvdisC1.b1': {'variable': ['rain_rate'], 'weight': [0.05]},
         'sgpvdisE13.b1': {'variable': ['rain_rate'], 'weight': [0.05]},
         'sgpdisdrometerC1.b1': {'variable': ['rain_rate'], 'weight': [0.10]},
         'sgpdisdrometerE13.b1': {'variable': ['rain_rate'], 'weight': [0.10]},
         'sgpstamppcpE13.b1': {'variable': ['precip'], 'weight': [0.10]},
         'sgpwbpluvio2C1.a1': {'variable': ['intensity_rtnrt'], 'weight': [0.25]},
         'sgpaosmetE13.a1': {'variable': ['rain_intensity'], 'weight': [0.025]},
         'sgpmwr3cC1.b1': {'variable': ['rain_intensity'], 'weight': [0.0125]}
        }

# Specify date for analysis
startdate = '2019-08-09'
enddate = startdate
sdate = ''.join(startdate.split('-'))

# Set up complicated for loops to go through each datastream 
# and variable
ds = {}
new = {}
out_units = 'mm/hr'
for d in cf_ds:
    # Find cdf/nc files and download if don't exist
    files = glob.glob(''.join(['./',d,'/*'+sdate+'*cdf']))
    if len(files) == 0:
        files = glob.glob(''.join(['./',d,'/*'+sdate+'*nc']))
        if len(files) == 0:
            act.discovery.download_data(username, token, d, startdate, enddate)
            files = glob.glob(''.join(['./',d,'/*'+sdate+'*cdf']))
            if len(files) == 0:
                files = glob.glob(''.join(['./',d,'/*'+sdate+'*nc']))

    # Read in the data to ACT object
    obj = act.io.armfiles.read_netcdf(files)

    # Loop through each variable and add to data list
    new_da = []
    for v in cf_ds[d]['variable']:
        da = obj[v]
        # Accumulate precip variables in new object i
        obj = act.utils.data_utils.accumulate_precip(obj, v)

        # Convert units and add to dataarray list
        units = da.attrs['units']
        if units == 'mm':
            da.attrs['units'] = 'mm/min'
        da.values = act.utils.data_utils.convert_units(da.values,da.attrs['units'],out_units)
        da = da.resample(time='1min').mean()
        new_da.append(da)

    # Depending on number of variables for each datastream, merge or create dataset
    if len(new_da) > 1:
        new_da = xr.merge(new_da)
    else:
        new_da = new_da[0].to_dataset()

    # Add to dictionary for the weighting
    cf_ds[d]['object'] = new_da

    # Add object to dictionary for plotting
    new[d] = obj

# Calculate weighted averages using the dict defined above
data = act.utils.data_utils.ts_weighted_average(cf_ds)

# Add weighted mean to plotting object and calculate accumulation
new['weighted'] = data.to_dataset(name='weighted_mean')
new['weighted']['weighted_mean'].attrs['units'] = 'mm/hr'
new['weighted'] = act.utils.data_utils.accumulate_precip(new['weighted'], 'weighted_mean')

# Plot the rain rates and accumulations
display = act.plotting.TimeSeriesDisplay(new, figsize=(12,12), subplot_shape=(2,))
display.plot('tbrg_precip_total', dsname='sgpmetE13.b1', color='b', label='MET TBRG', subplot_index=(0,))
display.plot('org_precip_rate_mean', dsname='sgpmetE13.b1', color='b',label='MET ORG', subplot_index=(0,))
display.plot('pwd_precip_rate_mean_1min', dsname='sgpmetE13.b1', color='b', label='MET PWD', subplot_index=(0,))
display.plot('rain_rate', dsname='sgpvdisC1.b1', color='w', label='VDIS C1', subplot_index=(0,))
display.plot('rain_rate', dsname='sgpvdisE13.b1', color='w', label='VDIS E13', subplot_index=(0,))
display.plot('rain_rate', dsname='sgpdisdrometerC1.b1', color='c', label='Disd C1', subplot_index=(0,))
display.plot('rain_rate', dsname='sgpdisdrometerE13.b1', color='c', label='Disd E13', subplot_index=(0,))
display.plot('precip', dsname='sgpstamppcpE13.b1', color='y', label='STAMP TBRG', subplot_index=(0,))
display.plot('intensity_rtnrt', dsname='sgpwbpluvio2C1.a1', color='g', label='WB', subplot_index=(0,))
display.plot('rain_intensity', dsname='sgpaosmetE13.a1', color='m', label='AOSMET', subplot_index=(0,))
display.plot('rain_intensity', dsname='sgpmwr3cC1.b1', color='m', label='MWR3C', subplot_index=(0,))
display.plot('weighted_mean', dsname='weighted', color='r', label='Weighted Avg', subplot_index=(0,))
display.day_night_background('sgpmetE13.b1')
display.axes[0].legend()

display.plot('tbrg_precip_total_accumulated', dsname='sgpmetE13.b1', color='b', label='MET TBRG',
             subplot_index=(1,))
display.plot('org_precip_rate_mean_accumulated', dsname='sgpmetE13.b1', color='b', label='MET ORG',
             subplot_index=(1,))
display.plot('pwd_precip_rate_mean_1min_accumulated', dsname='sgpmetE13.b1', color='b', label='MET PWD',
              subplot_index=(1,))
display.plot('rain_rate_accumulated', dsname='sgpvdisC1.b1', color='w', label='VDIS C1', subplot_index=(1,))
display.plot('rain_rate_accumulated', dsname='sgpvdisE13.b1', color='w', label='VDIS E13', subplot_index=(1,))
display.plot('rain_rate_accumulated', dsname='sgpdisdrometerC1.b1', color='c', label='Disd C1',
             subplot_index=(1,))
display.plot('rain_rate_accumulated', dsname='sgpdisdrometerE13.b1', color='c', label='Disd E13',
             subplot_index=(1,))
display.plot('precip_accumulated', dsname='sgpstamppcpE13.b1', color='y', label='STAMP TBRG', subplot_index=(1,))
display.plot('intensity_rtnrt_accumulated', dsname='sgpwbpluvio2C1.a1', color='g', label='WB', subplot_index=(1,))
display.plot('rain_intensity_accumulated', dsname='sgpaosmetE13.a1', color='m', label='AOSMET',
             subplot_index=(1,))
display.plot('rain_intensity_accumulated', dsname='sgpmwr3cC1.b1', color='m', label='MWR3C', subplot_index=(1,))
display.plot('weighted_mean_accumulated', dsname='weighted', color='r', label='Weighted Avg', subplot_index=(1,))
display.day_night_background('sgpmetE13.b1', subplot_index=(0,))
display.axes[1].legend()


plt.savefig('./images/precipitation.png')
plt.clf()


