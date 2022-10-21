import matplotlib
matplotlib.use('Agg')

import sys
sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')

import act
print(act.__file__)
import glob
import matplotlib.pyplot as plt
import json

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for KAZR data
site = 'sgp'
kazr_ds = site+'kazrgeC1.a1'
startdate = '2019-05-29'
enddate = '2019-05-31'

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

#Download KAZR Data
files = glob.glob(''.join(['./',kazr_ds,'/*'+sdate+'*cdf']))
if len(files) == 0:
    act.discovery.download_data(username, token, kazr_ds, startdate, enddate)
    files = glob.glob(''.join(['./',kazr_ds,'/*'+sdate+'*cdf']))

#Read in KAZR data to Standard Object
kazr = act.io.armfiles.read_netcdf(files)
kazr = kazr.resample(time='1min').nearest()
kazr = act.retrievals.cbh.generic_sobel_cbh(kazr,variable='reflectivity_copol',
                                            height_dim='range', var_thresh=-10.)

#Download, read, and display CEIL Data
#datastream = site+'ceilC1.b1'
#files = glob.glob(''.join(['./',datastream,'/*'+sdate+'*']))
#if len(files) == 0:
#    result = act.discovery.download_data(username, token, datastream, startdate, enddate)
#    files = glob.glob(''.join(['./',datastream,'/*'+sdate+'*']))
#files.sort()
#ceil = act.io.armfiles.read_netcdf(files)
#ceil = act.corrections.ceil.correct_ceil(ceil)
#ceil['first_cbh'].values = ceil['first_cbh'].values-ceil['alt'].values
#ceil = ceil.resample(time='1min').nearest()
#ceil = act.retrievals.cbh.generic_sobel_cbh(ceil,variable='backscatter',
#                                            height_dim='range', var_thresh=1000.,
#                                            fill_na=0)

#Download, read, and display MPL Data
datastream = site+'mplpolfsC1.b1'
files = glob.glob(''.join(['./',datastream,'/*'+sdate+'*']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*'+sdate+'*']))
files.sort()
mpl = act.io.armfiles.read_netcdf(files)
mpl = mpl.resample(time='1min').nearest()
mpl = act.corrections.mpl.correct_mpl(mpl)
mpl.range_bins.values = mpl.height.values[0,:]*1000.
mpl.range_bins.attrs['units'] = 'm'
mpl['signal_return_co_pol'].values[:,0:15] = 0.
mpl = act.retrievals.cbh.generic_sobel_cbh(mpl,variable='signal_return_co_pol',
                                            height_dim='range_bins',var_thresh=10.,
                                            fill_na=0.)


#Display data using plotting methods
#new = {kazr_ds: kazr, site+'ceilC1.b1':ceil, site+'mplpolfsC1.b1':mpl}
new = {kazr_ds: kazr,site+'mplpolfsC1.b1':mpl}
display = act.plotting.TimeSeriesDisplay(new,figsize=(15,10))
display.plot('reflectivity_copol',dsname=kazr_ds, cmap='jet')
#display.plot('signal_return_co_pol',dsname=site+'mplpolfsC1.b1', cmap='jet')
set_title = ' '.join(['KAZR Zh and CEIL CBH on',
    act.utils.datetime_utils.numpy_to_arm_date(ceil.time.values[0])])
display.plot('cbh_sobel',dsname=site+'kazrgeC1.a1',color='w',label='KAZR')
display.plot('cbh_sobel',dsname=site+'mplpolfsC1.b1',color='m',set_title=set_title,label='MPL')
display.set_yrng([0,8000])
display.axes[0].legend()
plt.savefig('./images/ceil_comp.png')
plt.clf()
