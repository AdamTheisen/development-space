import matplotlib
#matplotlib.use('Agg')

import act
import glob
import matplotlib.pyplot as plt
import json
import sys
import xarray as xr
import numpy as np

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for KAZR data
site = 'sgp'
startdate = '2009-01-01'
enddate = '2009-12-31'

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

#Download, read, and display CEIL Data
datastream = site+'ceilC1.b1'
files = glob.glob(''.join(['./',datastream,'/*2009*']))
files.sort()

ceil = act.io.armfiles.read_netcdf(files)
#ceil = act.corrections.ceil.correct_ceil(ceil)
#ceil['first_cbh'].values = ceil['first_cbh'].values-ceil['alt'].values
#ceil = ceil.resample(time='1min').nearest()
#ceil = act.retrievals.cbh.generic_sobel_cbh(ceil,variable='backscatter',
#                                            height_dim='range', var_thresh=1000.,
#                                            fill_na=0)
dmin= 500.
dmax = np.nanmax(ceil['first_cbh'].values)
ceil = ceil.where(ceil['first_cbh'] >= dmin)

ceil = ceil['first_cbh'].resample(time='1min').max()


datastream = site+'30smplcmask1zwangC1.c1'
files = glob.glob(''.join(['./',datastream,'/*2009*']))
files.sort()
mpl = act.io.armfiles.read_netcdf(files)
mpl['cloud_base'].values = mpl['cloud_base'].values*1000.

mpl = mpl.where(mpl['cloud_base'] >= dmin)
mpl = mpl.where(mpl['cloud_base'] <= dmax)

mpl = mpl['cloud_base'].resample(time='1min').max()

obj = xr.merge([ceil,mpl])

plt.scatter(obj['first_cbh'], obj['cloud_base'])
plt.show()

xedges = np.arange(dmin, dmax, 250)
yedges = np.arange(dmin, dmax, 250)
plt.hist2d(a_09/1000, b_09, bins=(xedges, yedges))
plt.show()

