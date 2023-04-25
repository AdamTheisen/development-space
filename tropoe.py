import sys
sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')

import act
import xarray as xr
import matplotlib.pyplot as plt

file = './tropoe20msnaoss.20230127.002010.nc'
obj = act.io.armfiles.read_netcdf(file, decode_times=False, use_base_time=True)

display = act.plotting.TimeSeriesDisplay(obj)
display.plot('temperature')
plt.show()
