# Import libraries
import sys
sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')

import act
import matplotlib.pyplot as plt
import glob

# Read in Data
obj = act.io.armfiles.read_netcdf(glob.glob('./sgpmfrsr7nchE11.b1/*'))

# Convert data to cf-standards
obj.clean.cleanup()

# Set Variable and add new maximum test
variable = 'diffuse_hemisp_narrowband_filter4'
obj.qcfilter.add_greater_test(variable, 0.4)

# Query ARM's DQR webservice and add to the qc variable
obj = act.qc.arm.add_dqr_to_qc(obj, variable=variable)

# Filter variable based on qc variable and remove data flagged by test 2, 3, and 4
obj.qcfilter.datafilter(variable, rm_tests=[2, 3, 4], del_qc_var=False)

# Set up the ACT TimeSeries Plot to hold 2 plots
display = act.plotting.TimeSeriesDisplay(obj, figsize=(15, 10), subplot_shape=(2,))

# Plot variable in the first plot, adding a day/night background
display.plot(variable, subplot_index=(0,))
display.day_night_background(subplot_index=(0,))

# Plot the QC Flag block plot in the second plot
display.qc_flag_block_plot(variable, subplot_index=(1,))

# Tighten the margins and display it
plt.tight_layout()
plt.show()
