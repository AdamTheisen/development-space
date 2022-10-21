import act
import glob
import numpy as np
import matplotlib.pyplot as plt


files =  glob.glob('./sgpecorsfE33.b1/*')
obj = act.io.armfiles.read_netcdf(files)
var_affected = ['momentum_flux', 'sensible_heat_flux', 'latent_flux', 'co2_flux']
obj = act.qc.arm.add_dqr_to_qc(obj, variable=var_affected)

files = glob.glob('./sgpmetE33.b1/*')
met = act.io.armfiles.read_netcdf(files)

obj['tbrg_precip_total'] = met['tbrg_precip_total'].resample(time='30min').sum()
obj.clean.cleanup()

# Flag fluxes if wind speeds < 1 m/s
idx = np.where(obj['mean_wind'].values < 1)
name = 'Wind < 1 m/s'
for  var in var_affected:
    obj.qcfilter.add_test(var, idx[0], test_meaning=name)

# Wind fetches for E33
wd = obj['wind_direction_from_north'].values
idx = np.where(((wd > 80) & (wd < 100)) | (wd < 40) | (wd > 300))
name = 'Fetch not sufficient'
for  var in var_affected:
    obj.qcfilter.add_test(var, idx[0], test_meaning=name)

# Rainfall from MET
idx = np.where(obj['tbrg_precip_total'].values > 0.)
name = 'Precipitation may affect CO2 flux'
obj.qcfilter.add_test('co2_flux', idx[0], test_meaning=name)

variable = var_affected[-1]
obj['co2_flux'] = obj['co2_flux'].where(obj['qc_co2_flux'] == 0)

display = act.plotting.TimeSeriesDisplay(obj, figsize=(15, 10), subplot_shape=(2,))
display.plot(variable, subplot_index=(0,))
display.qc_flag_block_plot(variable, subplot_index=(1,))
plt.show()

