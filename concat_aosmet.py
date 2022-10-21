import glob
import xarray as xr
files = glob.glob('./data/coraosmetM1.a1/*')
obj = xr.open_mfdataset(files)
obj['temperature_ambient'].to_netcdf('./coraosmet_temperature.nc')
