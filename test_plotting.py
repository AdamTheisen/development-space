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

file = glob.glob('/Users/atheisen/Code/ARM-Climatologies/data/sgpmetE13.b1/*b1.2016*.cdf')
ds = act.io.read_arm_netcdf(file, coords='minimal')
print(ds['qc_temp_mean'].values)
#ds = ds.resample(time='1min').nearest()
ds = act.qc.arm.add_dqr_to_qc(ds)
ds = ds.where(ds['qc_temp_mean'] == 0)

# Create Plot Display
display = act.plotting.TimeSeriesDisplay(ds, figsize=(16,6))

display.plot('temp_mean')
plt.show()
