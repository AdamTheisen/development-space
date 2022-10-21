import matplotlib.pyplot as plt
import numpy as np
import act
import glob
import xarray as xr


var='rh_mean'
files = glob.glob('./gucmetM1.b1/*')
files.sort()
obj = act.io.armfiles.read_netcdf(files)
obj = obj.where(obj['qc_'+var] == 0)
obj = obj.where(obj['qc_wspd_vec_mean'] == 0)
dir_bins_mid = np.linspace(0.0, 360.0, 12 + 1)

lat = obj['lat'].values#[0]
lon = obj['lon'].values#[0]

#year = '2021'
#crop = []
#for d in dir_bins_mid:
#    lat2, lon2 = act.utils.geo_utils.destination_azimuth_distance(
#         lat, lon, d, 50.
#        obj['lat'].values[0], obj['lon'].values[0], d, 50.
#    )
#    crop.append(act.discovery.get_cropscape.croptype(lat2, lon2, year))

display = act.plotting.WindRoseDisplay(obj)
display.plot_data('wdir_vec_mean', 'wspd_vec_mean', var, num_dirs=24, plot_type='contour', contour_type='mean', num_data_bins=10, clevels=21, cmap='rainbow')

display.axes[0].set_xticks(np.deg2rad(dir_bins_mid))
#display.axes[0].xaxis.set_ticklabels(crop)
#display.axes[0].set_ylim([-5, 5])

plt.show()
