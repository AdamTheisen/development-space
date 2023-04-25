# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:09:27 2023

@author: matth
"""

import numpy as np
import pandas as pd
import xarray as xr
from datetime import datetime, date
import act
import matplotlib.pyplot as plt

# Read in the data
fd70 = pd.read_csv('fd70_testdata.csv')
# Converts the date and time into a datetime64 type.
fd70['time'] = fd70['time'].astype('datetime64')
fd70 = fd70.reset_index(drop=True)

fd70.set_index('time', inplace=True)


# Converts it to an xarray dataset
ds_fd70 = fd70.to_xarray()

# Add a long name to the 15 minute code.
ds_fd70['present_wx2'].attrs["long_name"] = "Present weather 15 min (SYNOP)"

# Decode the WMO 4680 codes
ds_fd70 = act.utils.decode_present_weather(ds_fd70, variable='present_wx2')
#ds_fd70 = ds_fd70.assign(precip_codes=act.utils.decode_present_weather
#                         (ds_fd70, variable='present_wx2'))

print(ds_fd70)
# Create snowfall accumulation total as the instrument does a running total.
ds_fd70 = ds_fd70.assign(snowfall_total=ds_fd70.snowfall_accumulation -
                         ds_fd70.snowfall_accumulation[0])
ds_fd70['snowfall_total'].attrs['units'] = 'mm'
