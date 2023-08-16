import matplotlib
#matplotlib.use('Agg')
import act
import glob
import matplotlib.pyplot as plt
import json
import numpy as np

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

# We're going to use some test data that already exists within ACT
# Let's set a longer time period
startdate = '2022-07-16T21:00:00'
enddate = '2022-07-16T22:00:00'

# SONDE
datastream = 'houdlppiM1.b1'
result = act.discovery.download_data(username, token, datastream, startdate, enddate)
result.sort()


ds = act.io.armfiles.read_netcdf(result)
ds
# Returns the wind retrieval information in a new object by default
# Note that the default snr_threshold of 0.008 was too high for the first profile
# Reducing it to 0.002 makes it show up but the quality of the data is likely suspect.
ds_wind = act.retrievals.compute_winds_from_ppi(ds, snr_threshold=0.0001)

ds_wind = ds_wind.fillna(0)

# Plot it up
display = act.plotting.TimeSeriesDisplay(ds_wind)
display.plot_barbs_from_spd_dir('wind_speed', 'wind_direction', invert_y_axis=False, num_barbs_x=8, num_barbs_y=30)

#Update the x-limits to make sure both wind profiles are shown
display.axes[0].set_xlim([np.datetime64('2022-07-16T20:45:00'), np.datetime64('2022-07-16T22:15:00')])

plt.show()
