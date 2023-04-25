import glob
import act
import xarray as xr
import matplotlib.pyplot as plt

files = glob.glob('./Data/sgpmmcrmomC1.b1/*2010*')

ds = act.io.armfiles.read_mmcr(files)

display = act.plotting.TimeSeriesDisplay(ds, subplot_shape=(4,), figsize=(8, 10))
display.plot('Reflectivity_GE', subplot_index=(0,), cmap='act_HomeyerRainbow')
display.plot('Reflectivity_BL', subplot_index=(1,), cmap='act_HomeyerRainbow')
display.plot('Reflectivity_CI', subplot_index=(2,), cmap='act_HomeyerRainbow')
display.plot('Reflectivity_PR', subplot_index=(3,), cmap='act_HomeyerRainbow')
plt.show()


sys.exit()
nc = Dataset(files[0], 'a')
# Change heights name to range to read appropriately to xarray
#nc.renameDimension('heights', 'range')
obj = xr.open_dataset(xr.backends.NetCDF4DataStore(nc))


obj = obj.sel(time=slice('2009-01-01T23:55', '2009-01-01T23:59:59'))
#obj = obj.sel(time=slice('2009-01-02T00', '2009-01-02T0:05'))

obj.to_netcdf('./sgpmmcrmomC1.b1/sgpmmcrC1.b1.1.cdf')


file2 = glob.glob('./sgpmmcrmomC1.b1/sgpmmcrC1.b1.1.cdf')
nc = Dataset(file2[0], 'a')
nc.renameDimension('range', 'heights')
nc.close()
