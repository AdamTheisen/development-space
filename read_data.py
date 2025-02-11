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

files = glob.glob('./data/nsamawsC1.b1/*')

ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(ds)
print(ds['lon'].attrs)
#time = obj['base_time'].values + obj['time_offset'].values
#time = time.astype('datetime64[s]')
#obj['time'].values = time
#obj = act.io.armfiles.read_netcdf('./test.nc', combine='nested')


