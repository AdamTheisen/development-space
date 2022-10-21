import act
import glob
import matplotlib.pyplot as plt
import xarray as xr

files = glob.glob('./sgpmetE13.b1/*cdf')[0]

#obj = xr.open_mfdataset(files, decode_times=False)
#print(obj['time'])
nc_data = act.io.armfiles.read_netcdf(files,decode_times=False, cftime_to_datetime64=False)
nc_data.clean.cleanup()

#nc_data['time'].plot()
#plt.show()
#nc_data = act.io.armfiles.read_netcdf(files)
ts_display = act.plotting.TimeSeriesDisplay(nc_data)
ts_display.plot('time')
plt.show()
