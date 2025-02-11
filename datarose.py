import matplotlib.pyplot as plt
import numpy as np
import act
import glob
import xarray as xr


year = '*'
#files = glob.glob('./sgpaoscpcuf1mE13.b1/*' + year + '*')
files = glob.glob('./data/sgpecorsfE14.b1/*' + year + '*')
#files = glob.glob('./sgpco2flx4mC1.b1/*')

obj = act.io.arm.read_arm_netcdf(files)
obj = obj.where(obj['qc_co2_flux'] == 0)
dir_bins_mid = np.linspace(0.0, 360.0, 12 + 1)

lat = obj['lat'].values[0]
lon = obj['lon'].values[0]

#files = glob.glob('./sgpmetE13.b1/*' + year + '*')
#obj2 = act.io.arm.read_arm_netcdf(files)

#obj = obj.resample(time='1min').nearest()
#obj2 = obj2.resample(time='1min').nearest()

#obj = xr.merge([obj, obj2],  compat='override')
# ECOR Lat/Lon
lat=36.605274
lon=-97.48767

# CO2FLX
#lat= 36.605730
#lon= -97.488808

crop = []
year = '2023'
for d in dir_bins_mid:
    lat2, lon2 = act.utils.geo_utils.destination_azimuth_distance(
         lat, lon, d, 50.
#        obj['lat'].values[0], obj['lon'].values[0], d, 50.
    )
    crop.append(act.discovery.cropscape.get_crop_type(lat2, lon2, year))

display = act.plotting.WindRoseDisplay(obj)
#display.plot_data('wdir_vec_mean', 'wspd_vec_mean', 'concentration', num_dirs=24, plot_type='contour', contour_type='mean', num_data_bins=10, clevels=21, cmap='rainbow')
display.plot_data('wind_direction_from_north', 'mean_wind', 'sensible_heat_flux', num_dirs=24, plot_type='contour', contour_type='mean', num_data_bins=10, clevels=21, cmap='rainbow', vmin=-50, vmax=150)
#display.plot_data('wind_direction_from_north', 'mean_wind', 'co2_flux', num_dirs=24, plot_type='Line', line_plot_calc='Mean', color='white')
#display.plot_data('wind_direction', 'wind_speed', 'co2_flux', num_dirs=12, plot_type='Line', line_plot_calc='Median')

display.axes[0].set_xticks(np.deg2rad(dir_bins_mid))
display.axes[0].xaxis.set_ticklabels(crop)
#display.axes[0].set_ylim([-5, 5])

plt.show()
