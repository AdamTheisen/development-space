import act
import os
import glob
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 22})

# Grab EPA Ozone data using EPA API token
# Need to register with EPA airnow.gov site
token = os.getenv('AIRNOW_API')
lat_lon = '-106.994245,38.9504,-106.959845,38.97245'
results = act.discovery.get_airnow_bounded_obs(
    token, '2021-09-15T00', '2021-09-20T23', lat_lon, 'OZONE,PM25', data_type='B'
)

# Grab M1 ARM ozone data and remove the operational tests
files = glob.glob('./gucaoso3M1.b1/*2021*')
obj = act.io.armfiles.read_netcdf(files)
obj.clean.cleanup()
obj.qcfilter.datafilter('o3', rm_tests=[2,19,20], del_qc_var=False)

# Resample ARM data to 1 hour
obj = obj.resample(time='1H').mean()
results = results.squeeze(dim='sites', drop=False)

# Plot data
title = 'SAIL ARM(S2) and EPA(M1) Ozone Measurements'
display = act.plotting.TimeSeriesDisplay({'ARM': obj, 'EPA': results})
display.plot('o3', dsname='ARM', label='ARM')
display.plot('OZONE', dsname='EPA', label='EPA', set_title=title)
display.day_night_background(dsname='ARM')
display.set_yrng([0,80])
plt.legend()
plt.show()
