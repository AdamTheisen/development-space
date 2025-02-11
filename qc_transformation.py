import act
import xarray as xr

# Additionally, one might want to screen out averages if a certain
# percentage of that avereage are failing QC.  To do that, we can
# create a function and map it through xarray's resample
def qc_50(ds):
    print(ds)
    return(ds)

# Read in some sample MFRSR data and clean up the QC
ds = act.io.armfiles.read_netcdf(act.tests.sample_files.EXAMPLE_MFRSR, cleanup_qc=True)

ds = ds.resample(time='10min').map(qc_50)
