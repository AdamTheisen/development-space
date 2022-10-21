import act
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob
import xarray as xr


facs = ['E39']
datastreams = ['ecorsf', 'sebs', 'amc']

date = '20210501'
for f in facs:
    ecor = None
    sebs = None
    amc = None
    obj = []

    ecor_files = glob.glob('./sgpecorsf' + f + '.b1/*' + date + '*')
    if len(ecor_files) > 0:
        ecor =  act.io.armfiles.read_netcdf(ecor_files)
        ecor = ecor.rename({'time_bounds': 'time_bounds_ecor'})
        obj.append(ecor)

    sebs_files = glob.glob('./sgpsebs' + f + '.b1/*' + date + '*')
    if len(sebs_files) > 0:
        sebs =  act.io.armfiles.read_netcdf(sebs_files)
        obj.append(sebs)

    amc_files = glob.glob('./sgpamc' + f + '.b1/*' + date + '*')
    if len(amc_files) > 0:
        amc =  act.io.armfiles.read_netcdf(amc_files)
        amc = amc.rename({'time_bounds': 'time_bounds_amc'})
        print(list(amc))
        obj.append(amc)

    obj = xr.merge(obj, compat='override')

    ecor.close()
    sebs.close()
    amc.close()

    obj.to_netcdf('./sgpflux' + f + '.b1/sgpflux' + f + '.b1.' + date + '.000000.nc')
