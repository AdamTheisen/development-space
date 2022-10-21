"""
Example on how to plot out a corner reflector raster
----------------------------------------------------

This example shows how to plot out a corner reflector
raster scan which also analyzes the data and returns
the corner reflector location information

"""


import radtraq
from act.io.armfiles import read_netcdf
import matplotlib.pyplot as plt
import glob

files = glob.glob('./raster/*225730*')

# Read in sample data using ACT
for f in files:
    obj = read_netcdf(f)

    print(obj['range'].values)
    # Process and plot raster file
    data = radtraq.plotting.corner_reflector.plot_cr_raster(obj, target_range=489,
                                                        el_limits=[-0.5, 2.5], noplot=False)
    plt.show()
    plt.clf()
    obj.close()
    sys.exit()
