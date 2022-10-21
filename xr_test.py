import act
import numpy as np
import xarray as xr
import datetime as dt
import matplotlib.pyplot as plt


time = np.arange(dt.datetime(2022, 1, 1), dt.datetime(2022, 1, 2), dt.timedelta(minutes=1))[0:100]
data = np.random.randint(0,100,100)
data2 = np.random.randint(0,50,100)
obj = xr.Dataset({'z': (['time'], data), 'zdr': (['time'], data2), 'time': (['time'], time)}) 

display = act.plotting.TimeSeriesDisplay(obj)
display.plot('z')
display.plot('zdr')
plt.show()
