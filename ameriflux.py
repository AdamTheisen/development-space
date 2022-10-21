import act
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Set format for date on plot
years_fmt = mdates.DateFormatter('%Y-%m-%d')

# Read data into ACT object and set index to reformatted time
files = './data/AMERIFLUX/AMF_US-ARM_BASE_HH_8-5.csv'
obj = act.io.csvfiles.read_csv(files,header=2)
time = obj['TIMESTAMP_START'].values
time = pd.to_datetime(time,format='%Y%m%d%H%M%S')

obj = obj.assign_coords({'index': (time)})
#obj['index'].values = time

# Remove all missing values from object
var = 'TS_1_1_1'
name = 'TempSoil'
obj = obj.where(obj[var].values != -9999.)

# Calculate daily means and add back to object
co = obj[var].resample(index='1D').mean()
co = co.rename({'index':name+'_index'})
obj[name+'_daily_mean'] = co

# Calculate yearly means and add back to object
co = obj[var].resample(index='1Y').mean()
co = co.rename({'index':name+'_year_index'})
obj[name+'_yearly_mean'] = co

# Write out to netcdf
obj.to_netcdf('./data/AMERIFLUX/AMF_US-ARM_BASE_HH.nc')

# Plot CO2 data, daily averages, and yearly averages
display = act.plotting.TimeSeriesDisplay(obj,figsize=(12,8),subplot_shape=(1,))
set_title = 'Ameriflux '+name+' Data For SGP'
display.plot(var,marker='.',markersize=1, color='b',set_title=set_title, subplot_index=(0,))
display.plot(name+'_daily_mean',marker='.', color='r',set_title=set_title, subplot_index=(0,))
display.plot(name+'_yearly_mean',markersize=20, color='y',set_title=set_title, subplot_index=(0,))
#display.set_yrng([300,650])
display.axes[0].legend()
display.axes[0].xaxis.set_major_formatter(years_fmt)
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.savefig('./images/ameriflux_'+var+'.png')
