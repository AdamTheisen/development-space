import xarray as xr
import act
import glob
import matplotlib.pyplot as plt

files = glob.glob('./sgpceil10mC1.b1/*20110827*')

xds = xr.open_dataset(files[0])
fig, ax = plt.subplots(1,1)
xds['first_cbh'].plot(ax=ax)
plt.show()


ads = act.io.armfiles.read_netcdf(files)
display = act.plotting.TimeSeriesDisplay(xds)
display.plot('first_cbh')
plt.show()
