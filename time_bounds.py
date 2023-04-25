import act
import xarray as xr
import glob
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt


#files = glob.glob('./Data/sgpecorsfE14.b1/*2019*')
files = glob.glob('./Data/sgp30ecorE14.b1/*2019*')
ds_ecor = act.io.armfiles.read_netcdf(files)
ds_ecor = act.qc.arm.add_dqr_to_qc(ds_ecor)
ds_ecor['lv_e'].values = ds_ecor['lv_e'].values * -1.
ds_ecor = ds_ecor.rename({'lv_e': 'latent_heat_flux_ecor'})

# Switch some QC
qc = ds_ecor['qc_lv_e'].values
qc[10:20] = 2
ds_ecor['qc_lv_e'].values = qc

time_bounds = []
for t in ds_ecor['time'].values:
    t1 = t
    t2 = t + np.timedelta64(30, 'm')
    time_bounds.append([t1, t2])


files = glob.glob('./Data/sgp30ebbrE13.b1/*2019*')
ds_ebbr = act.io.armfiles.read_netcdf(files)
ds_ebbr = act.qc.arm.add_dqr_to_qc(ds_ebbr)

ds_ebbr = act.utils.datetime_utils.adjust_timestamp(ds_ebbr, offset=-30*60)




#ebbr_tb = ds_ebbr['time_bounds'].values
#ecor_tb = time_bounds

# Get the start time to align with
#ecor_start = [t[0] for t in ecor_tb] 
#ebbr_start = [np.datetime64(t[0]) for t in ebbr_tb] 
#ecor_interval = (ecor_tb[0][1] - ecor_tb[0][0]) /  np.timedelta64(1, 's')
#ebbr_interval = (ecor_tb[0][1] - ecor_tb[0][0]) /  np.timedelta64(1, 's')

#ds_ecor = ds_ecor.assign_coords({'time': ecor_start})
#ds_ebbr2 = ds_ebbr.assign_coords({'time': ebbr_start})

ds = xr.merge([ds_ecor, ds_ebbr], compat='override')

ds.qcfilter.datafilter(del_qc_var=False, rm_assessments=['Bad', 'Incorrect', 'Indeterminate', 'Suspect'])

# Set output grid to be hourly
#ds_hourly = ds.resample(time='H').mean(keep_attrs=True)
#ds_hourly.to_netcdf('./sgpecor_ebbr.nc')


display = act.plotting.TimeSeriesDisplay(ds, figsize=(15, 10), subplot_shape=(3,))
display.plot('latent_heat_flux_ecor', label='ECOR', subplot_index=(0,))
display.plot('latent_heat_flux', label='EBBR', subplot_index=(0,))
plt.legend()
display.qc_flag_block_plot('latent_heat_flux_ecor', subplot_index=(1,))
display.qc_flag_block_plot('latent_heat_flux', subplot_index=(2,))
plt.show()
