import xarray as xr
import glob
import act
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# Get data files
files = glob.glob('./data/kcgaosapsS3.b1/*20250101*')
files.sort()

# Read in with ACT
ds = act.io.read_arm_netcdf(files)

# an alternative is to use xarray which is what ACT is built on
# This shouldn't affect the APS data but there are quirks with
# other ARM datasets in how we set the time units which reqiures
# some additional work to get it correct.
#ds = xr.open_mfdataset(files)

# Plot up the data
title = 'APS Number Size Distribution'
cbar_title = 'dN/dlogD$_p$ (1/cm$^{3}$)'
display = act.plotting.TimeSeriesDisplay(ds, figsize=(10,6))
display.plot('dN_dlogDp', set_title=title, cvd_friendly=True, 
             norm=colors.LogNorm(vmin=0.1, vmax=1000.), cbar_label=cbar_title,
             ylabel='Pariticle Diameter (nm)')
display.axes[0].set_yscale('log')
plt.show()
