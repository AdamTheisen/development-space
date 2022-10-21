import matplotlib
matplotlib.use('Agg')

import sys
sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')

import act
print(act.__file__)
import glob
import matplotlib.pyplot as plt
import json

#Read in KAZR data to Standard Object
sirs_object = act.io.armfiles.read_netcdf(act.tests.sample_files.EXAMPLE_SIRS)
met_object = act.io.armfiles.read_netcdf(act.tests.sample_files.EXAMPLE_MET1)

obj = act.retrievals.radiation.calculate_dsh_from_dsdh_sdn(sirs_object)

obj = act.retrievals.radiation.calculate_irradiance_stats(obj,
    variable='derived_down_short_hemisp', variable2='down_short_hemisp',
    threshold=60)

obj = act.retrievals.radiation.calculate_net_radiation(obj, smooth=30)

obj = act.retrievals.radiation.calculate_longwave_radiation(obj,
    temperature_var='temp_mean', vapor_pressure_var='vapor_pressure_mean',
    met_obj=met_object)

#Display data using plotting methods
#new = {kazr_ds: kazr, site+'ceilC1.b1':ceil, site+'mplpolfsC1.b1':mpl}
display = act.plotting.TimeSeriesDisplay(obj,figsize=(15,10))
display.plot('down_long_hemisp_shaded', label='SIRS')
display.plot('monteith_clear', label='Monteith Clear')
display.plot('monteith_cloudy', label='Monteith Cloudy')
display.plot('prata_clear', label='Prata Clear')
display.day_night_background()
display.axes[0].legend()
plt.savefig('./images/sirs.png')
plt.clf()
