import matplotlib
matplotlib.use('Agg')

import act.io.armfiles as arm
from act.corrections.ceil import correct_ceil
from act.plotting import common
import act.plotting.plot as armplot
import act.utils.data_utils as arm_du
import glob
import matplotlib.pyplot as plt
import numpy as np
import sys

#files = sorted(glob.glob('/Users/atheisen/Desktop/DATA/*met*'))
#test = arm.read_netcdf(files)

#Plot Temp Data
#display = armplot.display(test)
#fig = plt.figure(figsize=(15,8))
#fig.subplots_adjust(0.05,0.05,0.93,0.96,0.25,0.25)
#ax = plt.subplot(2,1,1)
#display.plot('temp_mean',ax=ax)
#xrng = display.xrng

#Plot CEIL Data
files = sorted(glob.glob('/Users/atheisen/Desktop/DATA/*ceil*'))
ceil = arm.read_netcdf(files)
ceil = correct_ceil(ceil)
plt.subplot(2,1,1)
display = armplot.display(ceil)
display.set_yrng([0,500])
display.set_xrng(xrng)
display.plot('backscatter',cbmin=0,cbmax=4,cmap='gist_ncar',add_nan=True)
display.plot('first_cbh')

#Plot CPC data
files = sorted(glob.glob('/Users/atheisen/Desktop/DATA/*cpc*'))
test = arm.read_netcdf(files)
display = armplot.display(test)
ax = plt.subplot(2,1,2)
display.set_yrng([0,50000])
#display.set_xrng(xrng)
display.plot('concentration',ax=ax)

fig.savefig('./test.png')
