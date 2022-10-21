import sys
sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')
import act
import glob
import xarray as xr
import matplotlib.pyplot as plt

files = glob.glob('./sgpmetE13.b1/*')
obj = act.io.armfiles.read_netcdf(files)#, combine='nested')#, decode_cf=False)

#Display data using plotting methods
display = act.plotting.TimeSeriesDisplay(obj,figsize=(10,8))
display.plot('temp_mean',color='b', label='SGP MET E13')
display.day_night_background()
plt.show()
