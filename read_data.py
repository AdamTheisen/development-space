import glob

import sys
#sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')
import act
import radtraq
print(act.__file__)

import xarray as xr
import matplotlib.pyplot as plt
#files = glob.glob('./corkazrcfrgeM1.a1/*20190401.2*')
#obj = xr.open_mfdataset(files)
#print(obj['time'])

files = glob.glob('./data/epckazrcfrgeM1.a1/*20230516.19*')
print(files)
obj = act.io.armfiles.read_netcdf(files, engine='netcdf4')
obj = obj.resample(time='1min').nearest()
obj = radtraq.proc.cloud_mask.calc_cloud_mask(obj, 'reflectivity')
obj = obj.where(obj['cloud_mask_2'] == 1)

display = act.plotting.TimeSeriesDisplay(obj)
#display.plot('reflectivity', cb_friendly=True)
display.plot('linear_depolarization_ratio', cb_friendly=True)
#display.plot('mean_doppler_velocity', cb_friendly=True)
#display.plot('reflectivity_crosspolar_v', cb_friendly=True)
display.set_yrng([0,4000])
plt.show()

#obj.close()
#obj = act.io.armfiles.read_netcdf(files, combine='nested', use_cftime=True)
#time = obj['base_time'].values + obj['time_offset'].values
#time = time.astype('datetime64[s]')
#obj['time'].values = time
#obj = act.io.armfiles.read_netcdf('./test.nc', combine='nested')


