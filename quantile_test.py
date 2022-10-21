import act
import numpy as np
import matplotlib.pyplot as plt

obj = act.io.armfiles.read_netcdf(act.tests.sample_files.EXAMPLE_MET1)
obj.clean.cleanup()

quantile = obj['temp_mean'].quantile(0.999).values

scale = 3

lower = np.nanmedian(obj['temp_mean'].values) - scale * abs(quantile)
upper = np.nanmedian(obj['temp_mean'].values) + scale * abs(quantile)

print(lower, upper)
result = obj.qcfilter.add_outside_test('temp_mean',lower, upper)
print(result)

# Creat Plot Display
display = act.plotting.TimeSeriesDisplay(obj, figsize=(15, 10), subplot_shape=(2,))

# Plot temperature data in top plot
display.plot('temp_mean', subplot_index=(0,))

# Plot QC data
display.qc_flag_block_plot('temp_mean', subplot_index=(1,))
plt.show()

#np.nanmedian(precip_df[precip_var].sum()/60.) + 2. * np.nanstd(precip_df[precip_var].quantile(0.999, axis=1))/60.
#upper = np.nanmedian(precip_df[precip_var].sum()/60.) + 3. * np.nanstd(precip_df[precip_var].quantile(0.999, axis=1))/60.
