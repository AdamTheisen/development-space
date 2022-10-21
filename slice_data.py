import act
import glob
import numpy as np

files = glob.glob('./sgpstampE*b1/sgpstampE*nc')


time = '2020-01-01T01:00:00.000000000'
fields = ['plant_water_availability_east', 'lat', 'lon']
for f in files:
    obj = act.io.armfiles.read_netcdf(f)

    for var in obj:
        if var not in fields:
            obj = obj.drop_vars(var)

    idx = obj['time'] < np.datetime64(time)
    obj = obj.isel(time=idx)
    obj.to_netcdf(f.split('/')[0-1])
