import matplotlib
matplotlib.use('Agg')

import act
import glob
import matplotlib.pyplot as plt
import json
import sys
import numpy as np

#Download, read, and display CEIL Data
files = glob.glob(''.join(['./sgpceilC1.b1/sgpceilC1.b1.2008*.nc']))

files.sort()

ceil = act.io.armfiles.read_netcdf(files,data_vars=['first_cbh', 'base_time'])
ceil = ceil['first_cbh'].where(ceil['first_cbh'] >= 500., drop=True)

print(ceil['time'])

low = np.where(ceil.values < 1500.)[0]
med = np.where((ceil.values >= 1500.) & (ceil.values < 4000.))[0]
high = np.where(ceil.values > 4000.)[0]
print(len(low), len(med), len(high))

#ceil = ceil.resample(time='1min').nearest()
#ceil = act.retrievals.cbh.generic_sobel_cbh(ceil,variable='backscatter',
#                                            height_dim='range', var_thresh=1000.,
#                                            fill_na=0)


#diff = ceil['first_cbh']-ceil['cbh_sobel']

#print(np.nanmean(diff.values),np.nanstd(diff.values))

#Display data using plotting methods
#display = act.plotting.TimeSeriesDisplay(ceil,figsize=(15,10))
#display.plot('backscatter', cmap='jet')
#set_title = ' '.join(['KAZR Zh and CEIL CBH on',
#    act.utils.datetime_utils.numpy_to_arm_date(ceil.time.values[0])])
##display.plot('first_cbh',color='k',label='CEIL')
#display.plot('cbh_sobel',color='w',set_title=set_title,label='CEIL Sobel')
#display.set_yrng([0,8000])
#display.axes[0].legend()
#plt.savefig('./images/ceil_cbh_calc.png')
#plt.clf()
