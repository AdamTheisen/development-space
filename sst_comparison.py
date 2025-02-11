import act
import glob
import matplotlib.pyplot as plt
import sys
import datetime as dt
import xarray as xr
import numpy as np


files = glob.glob('./marmaeriM1.b1/17121*')
files.sort()
names = ['doy', 'hour', 'air_temp', 'air_temp_std', 'air_temp_unc',
         'sst', 'sst_std', 'sst_unc', 'lat', 'lon']
maeri = act.io.read_csv(files, column_names=names, skiprows=range(0,13), sep='\s+')

time = []
for d in maeri['doy'].values:
    if d > 200:
        time.append(dt.datetime(2017,1,1,) + dt.timedelta(days=d-1))
    else:
        time.append(dt.datetime(2018,1,1,) + dt.timedelta(days=d-1))

#maeri = maeri.reset_index(['index'], drop=True)
#maeri = maeri.assign(time=time)
maeri['time'] = xr.DataArray(time, dims='index', coords=maeri.coords)
maeri = maeri.swap_dims({'index': 'time'})
maeri = maeri.sortby('time')

files = glob.glob('./marirtsstM1.b1/*2017121*')
files.sort()
irt = act.io.read_arm_netcdf(files)
irt = irt.resample(time='1min').mean()
irt = act.retrievals.sst_from_irt(irt)

#files = glob.glob('./marnavM1.a1/*2017121*')
#files.sort()
#nav = act.io.read_netcdf(files)
#nav = nav.resample(time='30min').mean()

_, index = np.unique(maeri['time'], return_index=True)
maeri = maeri.isel(time=index)
maeri = maeri.resample(time='20min').nearest()
irt = irt.resample(time='20min').nearest()
ds = xr.merge([maeri, irt])

ds = ds[['sst', 'sea_surface_temperature']]

# Create a DistributionDisplay object to compare fields
display = act.plotting.DistributionDisplay(ds)

# Compare aircraft ground speed with indicated airspeed
display.plot_scatter(
    'sea_surface_temperature',
    'sst',
)
display.set_xrng((270, 320))
display.set_yrng((270, 320))
display.set_ratio_line()

plt.show()
#display = act.plotting.TimeSeriesDisplay({'maeri': maeri, 'irt': irt, 'nav': nav}, figsize=(15,10), subplot_shape=(2,))
#display = act.plotting.TimeSeriesDisplay({'maeri': maeri, 'irt': irt}, figsize=(15,10))
#display.plot('sea_surface_temperature', 'irt', marker=',', label='IRT', set_title='SST', subplot_index=(0,))
#display.plot('sst', 'maeri', marker='.', linestyle='none', label='MAERI', subplot_index=(0,))
#display.plot('lat', 'nav', label='NAV', subplot_index=(1,))
#plt.legend()
#plt.show()
