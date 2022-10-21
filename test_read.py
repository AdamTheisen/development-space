import act
import glob
import xarray as xr


files = glob.glob('./mao180varanaM1.c1.20150101.000000.custom.cdf')
obj = act.io.armfiles.read_netcdf(files)
print(obj)
