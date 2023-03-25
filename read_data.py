import glob

import sys
#sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')
import act
print(act.__file__)

import xarray as xr
#files = glob.glob('./corkazrcfrgeM1.a1/*20190401.2*')
#obj = xr.open_mfdataset(files)
#print(obj['time'])

files = glob.glob('./Data/sgpmfrsr7nchE38.b1/*')[0]
obj = act.io.armfiles.read_netcdf(files, decode_times=False)
#obj.close()
#obj = act.io.armfiles.read_netcdf(files, combine='nested', use_cftime=True)
#time = obj['base_time'].values + obj['time_offset'].values
#time = time.astype('datetime64[s]')
#obj['time'].values = time
#obj = act.io.armfiles.read_netcdf('./test.nc', combine='nested')


