#!/usr/bin/env python
# coding: utf-8

# In[2]:


"""
Time Series Visualization of a Soil Moisture Parameter with Precipitation Overlay
"""
import sys
#sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')
import act
import matplotlib.pyplot as plt
import json
import glob
import numpy as np
from datetime import datetime
import xarray as xr
import matplotlib.pyplot as plt
import act

file = glob.glob('./data/sgpmetE13.b1/*.2010*custom*')
ds = act.io.read_arm_netcdf(file)
ds.clean.cleanup()

file = glob.glob('./data/sgpmetE13.b1/*.2010*00.cdf')
ds2 = act.io.read_arm_netcdf(file)
ds2.clean.cleanup()

# Create Plot Display
print(ds['qc_temp_mean'].attrs)
display = act.plotting.TimeSeriesDisplay({'Custom': ds, 'Original': ds2}, figsize=(10, 8), subplot_shape=(3,))

display.plot('temp_mean', subplot_index=(0,), dsname='Custom', label='Custom', marker='s')
display.plot('temp_mean', subplot_index=(0,), dsname='Original', label='Original')
display.axes[0].legend()
display.plot('qc_temp_mean', subplot_index=(1,), dsname='Custom', label='Custom')
display.plot('qc_temp_mean', subplot_index=(2,), dsname='Original', label='Original')
plt.tight_layout()
plt.show()
