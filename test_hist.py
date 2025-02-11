import sys
sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')
import act
import matplotlib.pyplot as plt
import numpy as np

sonde_ds = act.io.armfiles.read_netcdf(act.tests.sample_files.EXAMPLE_SONDE1)
    
histdisplay = act.plotting.HistogramDisplay({'sgpsondewnpnC1.b1': sonde_ds})
histdisplay.plot_stairstep_graph('tdry', bins=np.arange(-60, 10, 1))
sonde_ds.close()
plt.show()
