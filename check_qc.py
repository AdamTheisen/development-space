import act
import glob

files = glob.glob('./data/sgpmetE13.b1/*custom*')

for f in files:
    ds = act.io.read_arm_netcdf(f)
    qc_vars = [var for var in ds if 'qc_' in var]
    for var in qc_vars:
        if ds[var].max() > 0:
            print(f, var)
