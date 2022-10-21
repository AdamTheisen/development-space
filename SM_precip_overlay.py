#!/usr/bin/env python
# coding: utf-8

# In[2]:


"""
Time Series Visualization of a Soil Moisture Parameter with Precipitation Overlay
"""
import act
import matplotlib.pyplot as plt
import json
import glob
import numpy as np
from datetime import datetime


# In[3]:


#Read in ARM Live Data Webservice Token and Username
#Get a token and sign up here: https://adc.arm.gov/armlive/
#token.json format
#{
#    "username": "name",
#    "token": "longtoken1243"
#}
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']


# In[4]:


#Set data download properties (user-defined dates)
datastream_stamp = 'sgpstampE13.b1'
datastream_stamppcp = 'sgpstamppcpE13.b1'
date_start = '2019-10-01'
date_end = '2019-10-31'


# In[208]:


#Download data
#result = act.discovery.download_data(username, token, datastream_stamp, date_start, date_end)
#act.discovery.download_data(username, token, datastream_stamppcp, date_start, date_end)


# In[5]:


#Download data and create an array of filenames
stamp_files = glob.glob(''.join(['./',datastream_stamp,'/*nc']))
if len(stamp_files) == 0:
    act.discovery.download_data(username, token, datastream_stamp, date_start, date_end)
    stamp_files = glob.glob(''.join(['./',datastream_stamp,'/*nc']))
    
stamppcp_files = glob.glob(''.join(['./',datastream_stamppcp,'/*nc']))
if len(stamppcp_files) == 0:
    act.discovery.download_data(username, token, datastream_stamppcp, date_start, date_end)
    stamppcp_files = glob.glob(''.join(['./',datastream_stamppcp,'/*nc']))


# In[6]:


#Read files into data objects
stamp_data = act.io.armfiles.read_netcdf(stamp_files)
stamppcp_data = act.io.armfiles.read_netcdf(stamppcp_files)


# In[7]:


#Create an accumulated precipitation variable from rainfall rate in precipitation data object 
accum_precip = act.utils.data_utils.accumulate_precip(stamppcp_data,'precip')


# In[8]:


#Convert datetime64 to datetime for plot functionality
#datetime_array = []
#for i in range(0,len(stamppcp_data.time)):
#    timestamp = ((stamppcp_data.time[i] - np.datetime64('1970-01-01T00:00:00'))
#                 / np.timedelta64(1, 's'))
#    datetime = datetime.utcfromtimestamp(timestamp)
#    datetime_array.append(datetime)


# In[9]:

new = {'stamp': stamp_data, 'stamppcp': stamppcp_data}
display = act.plotting.TimeSeriesDisplay(new)
display.plot('real_dielectric_permittivity_west', dsname='stamp', force_line_plot=True, labels=True)
#display.plot('precip_accumulated', dsname='stamppcp',secondary_y=True)
#display.legend(['5','10','25','50','100','Precipitation'])
#display.fill_between('precip_accumulated', dsname='stamppcp',color='gray',alpha=0.2, secondary_y=True)
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

stamp_data.close()
stamppcp_data.close()
