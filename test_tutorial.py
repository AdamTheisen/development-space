import sys
sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')

import act
print(act.__file__)
import matplotlib.pyplot as plt
import numpy as np

# Set your own username and token if you have it
username = 'armlive_training'
token = '5ab7d814ae1297c5'

# ACT module for downloading data from the ARM web service
results = act.discovery.download_data(username, token, 'sgpmfrsr7nchE11.b1', '2021-03-29', '2021-03-29')
print(act.__version__)
obj = act.io.armfiles.read_netcdf(results)

obj.clean.cleanup()
obj

variable = 'diffuse_hemisp_narrowband_filter4'

# Now lets remove some of these outliers
obj.qcfilter.datafilter(variable, rm_tests=[2, 3], del_qc_var=False)

# And plot the data again
# Create a plotting display object with 2 plots
display = act.plotting.TimeSeriesDisplay(obj, figsize=(15, 10), subplot_shape=(2,))

# Plot up the diffuse variable in the first plot
display.plot(variable, subplot_index=(0,))

# Plot up a day/night background
display.day_night_background(subplot_index=(0,))

# Plot up the QC variable in the second plot
#display.qc_flag_block_plot(variable, subplot_index=(1,))

plt.show()
