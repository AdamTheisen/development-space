import matplotlib.pyplot as plt
import numpy as np
import act
import glob
import xarray as xr


files = glob.glob('./gucaossmpsS2.b1/*')
files.sort()
obj = act.io.armfiles.read_netcdf(files)
#obj = obj.where(obj['qc_co2_flux'] == 0)
dir_bins_mid = np.linspace(0.0, 360.0, 12 + 1)

lat = obj['lat'].values[0]
lon = obj['lon'].values[0]

files = glob.glob('./gucaosmetS2.a1/*')
files.sort()
obj2 = act.io.armfiles.read_netcdf(files)
obj2 = obj2.where(obj2['qc_wind_speed'] == 0)
obj2 = obj2.where(obj2['qc_wind_direction'] == 0)

obj = obj.resample(time='1min').nearest()
obj2 = obj2.resample(time='1min').nearest()

obj = xr.merge([obj, obj2],  compat='override')

year = '2021'
crop = []
for d in dir_bins_mid:
    lat2, lon2 = act.utils.geo_utils.destination_azimuth_distance(
         lat, lon, d, 50.
#        obj['lat'].values[0], obj['lon'].values[0], d, 50.
    )
    crop.append(act.discovery.get_cropscape.croptype(lat2, lon2, year))

display = act.plotting.WindRoseDisplay(obj)
display.plot_data('wind_direction', 'wind_speed', 'total_N_conc', num_dirs=24, plot_type='contour', contour_type='mean', num_data_bins=10, clevels=21, cmap='rainbow')

display.axes[0].set_xticks(np.deg2rad(dir_bins_mid))
display.axes[0].xaxis.set_ticklabels(crop)
#display.axes[0].set_ylim([-5, 5])

plt.show()
