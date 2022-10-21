import pyart
import matplotlib.pyplot as plt

files = './enaxsaprsecD1.00/enaxsaprsecD1.00.20170526.085907.raw.sec_XSAPR2_20170526085907_00.h5'
radar =pyart.aux_io.read_gamic(files)
display = pyart.graph.RadarDisplay(radar)
fig = plt.figure()
ax = fig.add_subplot(111)
display.plot('reflectivity', 0, vmin=-32, vmax=64., mask_tuple=['cross_correlation_ratio', 0.95])
#display.plot('differential_reflectivity', 0, vmin=-4, vmax=4.)
#display.plot('cross_correlation_ratio', 0, vmin=0.9, vmax=1)
display.plot_range_rings([40,80])
display.plot_cross_hair(5.)
plt.show()
