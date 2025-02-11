import act
import glob
import matplotlib.pyplot as plt
import xarray as xr
from sklearn.metrics import root_mean_squared_error
import numpy as np

date = '2022'
files = glob.glob('./data/sgpco2flx4mC1.b1/*.' + date + '*')
ds_c = act.io.read_arm_netcdf(files)
ds_c.clean.cleanup()
ds_c = act.qc.arm.add_dqr_to_qc(ds_c)
ds_c.qcfilter.datafilter(rm_assessments=['Bad', 'Indeterminate'], del_qc_var=False)

# Get ECOR Data
files = glob.glob('./data/sgpecorsfE14.b1/*.' + date + '*')
ds_e = act.io.read_arm_netcdf(files)
ds_e.clean.cleanup()
ds_e = act.qc.arm.add_dqr_to_qc(ds_e)
ds_e.qcfilter.datafilter(rm_assessments=['Bad', 'Indeterminate'], del_qc_var=False)
ds_e = ds_e.rename({'co2_flux': 'co2_flux_ecor'})

ds_c = act.utils.datetime_utils.adjust_timestamp(ds_c, offset=15 * 60)

ds = xr.merge([ds_c['co2_flux'], ds_e[['co2_flux_ecor', 'wind_direction_from_north', 'mean_wind']]], compat='override')
ds = ds.dropna(dim='time', how='any')
ds = ds.where(ds['mean_wind'].compute() > 2., drop=True)
ds['diff'] = ds['co2_flux'] - ds['co2_flux_ecor']


result = root_mean_squared_error(ds['co2_flux'], ds['co2_flux_ecor'])
print(result)
#display = act.plotting.TimeSeriesDisplay(ds)
#display.plot('co2_flux')
#display.plot('co2_flux_ecor')
#plt.show()

#display = act.plotting.WindRoseDisplay(ds)
#display.plot_data('wind_direction_from_north', 'mean_wind', 'co2_flux', num_dirs=24, plot_type='line', label='CO2FLX')
#display.plot_data('wind_direction_from_north', 'mean_wind', 'co2_flux_ecor', num_dirs=24, plot_type='line', label='ECOR')
#display.axes[0].text(0.05, 0.95, 'RMSE= ' + str(round(result,2)), fontsize=9,
#            transform=display.axes[0].transAxes, horizontalalignment='right')
#plt.legend()
#plt.savefig('./images/' + date + '_ecor_co2flx.png')
#plt.show()
sectors = np.arange(0, 361, 30)
rmse = []
for i in range(len(sectors) - 1):
    ds_new = ds.where((ds['wind_direction_from_north'].compute() >= sectors[i]) &
                      (ds['wind_direction_from_north'].compute() < sectors[i+1]), drop=True).copy()
    result = root_mean_squared_error(ds_new['co2_flux'], ds_new['co2_flux_ecor'])
    rmse.append(result)

print(rmse)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(np.deg2rad(sectors[0:-1] + 15), rmse)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_ylim([0, 20])
#ax.set_rmax(2)
#ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
#ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
#ax.grid(True)

plt.show()
