import sys
#sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')

import act
import matplotlib.pyplot as plt
import glob
import pyart
import numpy as np

files = glob.glob('/Users/atheisen/Code/test_codes/mpl_data/20150902*.mpl')

files.sort()

ap = '/Users/atheisen/Code/test_codes/mpl_data/cal_files/MMPL5005_Afterpulse_201503312000.bin'
dt = '/Users/atheisen/Code/test_codes/mpl_data/cal_files/MMPL5005_SPCM23721_Deadtime11.bin'
op = '/Users/atheisen/Code/test_codes/mpl_data/cal_files/MMPL5005_Overlap_SigmaMPL_201504041700.bin'

#mpl_ds = act.io.mpl.read_sigma_mplv5(files)
mpl_cor = act.io.mpl.read_sigma_mplv5(files, afterpulse=ap, dead_time=dt, overlap=op)
radar = act.utils.create_pyart_obj(mpl_cor, azimuth='azimuth_angle', elevation='elevation_angle',
                                   range_var='range')

#display = act.plotting.TimeSeriesDisplay(mpl_cor)
#display.plot('nrb_copol', cmap='jet', vmin=0, vmax=1)
#plt.show()

display = pyart.graph.RadarDisplay(radar)
display.plot('nrb_copol', sweep=1, title_flag=False, vmin=0, vmax=1.0,cmap='jet')
plt.show()

mpl_cor.close()
