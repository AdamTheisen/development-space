import matplotlib
import act
import glob
import matplotlib.pyplot as plt
import json
import xarray as xr
import sys
import datetime as dt
import pandas as pd
import numpy as np

files = ['./enasondewnpnC1.b1/enasondewnpnC1.b1.20211212.113000.cdf']

obj = act.io.armfiles.read_netcdf(files)

skewt = act.plotting.SkewTDisplay(obj, figsize=(15, 10))
skewt.plot_from_u_and_v('u_wind', 'v_wind', 'pres', 'tdry', 'dp')
plt.show()
