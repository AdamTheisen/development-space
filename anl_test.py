import act
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Get ANL MET files from local system
files = glob.glob('./data/ANLTWR/*.data')

# Specify the header names for the data
headers = ['day','month','year','time','pasquill','wdir_60m','wspd_60m',
    'wdir_60m_std','temp_60m','wdir_10m','wspd_10m','wdir_10m_std','temp_10m',
    'temp_dp','rh','avg_temp_diff','total_precip','solar_rad','net_rad',
    'atmos_press','wv_pressure','temp_soil_10cm','temp_soil_100cm','temp_soil_10ft']

# Read in the data using the ACT CSV reader
obj = act.io.csvfiles.read_csv(files[0],sep='\s+',column_names=headers,skipfooter=2)

# Create a proper time index
obj['year'] = obj.year+2000.
hr = []
mn = []
for t in obj.time.values:
    hr.append(str(t).zfill(4)[0:2])
    mn.append(str(t).zfill(4)[2:4])
df = pd.DataFrame({'year': obj.year, 'month': obj.month,
                  'day': obj.day, 'hour': hr, 'minute': mn})
df = pd.to_datetime(df)
obj['time'] = df.to_xarray()
obj = obj.set_index({'index': 'time'})

# Clear out -9999 data so plots scale correctly
obj.temp_soil_100cm[obj.temp_soil_100cm == 99999] = np.nan

# Change index to time
obj = obj.rename({'index': 'time'})

# Plot Data
display = act.plotting.TimeSeriesDisplay(obj,figsize=(12,15),subplot_shape=(4,))
set_title = 'ANL MET TWR Temperature'
display.plot('temp_60m',color='b',set_title=set_title, subplot_index=(0,))
display.plot('temp_10m',color='g',set_title=set_title, subplot_index=(0,))

set_title = 'ANL MET TWR Radiation'
display.plot('solar_rad',color='b',set_title=set_title, subplot_index=(1,))
display.plot('net_rad',color='g',set_title=set_title, subplot_index=(1,))

set_title = 'ANL MET TWR Pressure'
display.plot('atmos_press',color='b',set_title=set_title, subplot_index=(2,))

set_title = 'ANL MET TWR Soil Temperature'
display.plot('temp_soil_10cm',color='b',set_title=set_title, subplot_index=(3,))
display.plot('temp_soil_100cm',color='g',set_title=set_title, subplot_index=(3,))
display.plot('temp_soil_10ft',color='c',set_title=set_title, subplot_index=(3,))

plt.tight_layout()
plt.savefig('./images/anl_twr_test.png')


# Plot out windrose
set_title = 'ANL MET TWR Wind Rose'
windrose = act.plotting.WindRoseDisplay(obj,figsize=(10,8),subplot_shape=(1,))
windrose.plot('wdir_10m','wspd_10m',spd_bins=np.linspace(0, 10, 5),
    set_title=set_title, subplot_index=(0,))
windrose.axes[0].legend(loc=(-0.1,0.1))

plt.tight_layout()
plt.savefig('./images/anl_twr_wrose_test.png')
