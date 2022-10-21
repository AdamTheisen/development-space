import glob
import act
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

files = glob.glob('./gucmetM1.b1/*')
obj = act.io.armfiles.read_netcdf(files)

xr.plot.hist(obj['tbrg_precip_total_corr'])
plt.show()
