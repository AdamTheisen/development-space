#!/usr/bin/env python
# coding: utf-8

# In[2]:


"""
Time Series Visualization of a Soil Moisture Parameter with Precipitation Overlay
"""
import sys
sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')
import act
import matplotlib.pyplot as plt
import json
import glob
import numpy as np
from datetime import datetime

#Read files into data objects
files = glob.glob('./sgpmetE13.b1/*202*')
obj = act.io.armfiles.read_netcdf(files)
display = act.plotting.TimeSeriesDisplay(obj, subplot_shape=(4, 3))
groupby = display.group_by('month')
groupby.plot_group('plot', None, field='temp_mean')
plt.show()

##Plot data
#fig, ax1 = plt.subplots()
#ax2 = ax1.twinx()
#plot_sm = ax1.plot(stamp_data.time, stamp_data.real_dielectric_permittivity_west)
#plot_precip = ax2.fill_between(datetime_array, stamppcp_data.precip_accumulated, color='gray', alpha=0.2, label='precip')
#plt.autoscale(enable=True, axis='x', tight=True)
#ax2.set_ylim(0,)
#plt.setp(ax1.get_xticklabels(), rotation=30, horizontalalignment='right')
#ax1.set_xlabel('Time', labelpad=20)
#ax1.set_ylabel('Moisture', labelpad=20)
#ax2.set_ylabel('Precipitation (mm)', rotation=270, labelpad=20)
#plt.title('Soil Moisture and Precipitation')
#ax1.legend(plot_sm, ('5cm', '10cm', '20cm', '50cm', '100cm'), bbox_to_anchor=(-0.1,0.4))
#ax2.legend(bbox_to_anchor=(1.3,0.1))
#plt.show()

obj.close()
