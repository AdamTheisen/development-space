import glob
import xarray as xr

filepath = './houaosapsM1.b1/*'
files = glob.glob(filepath)

print('Outputing to one file')
# If you want them all in one csv
ds = xr.open_mfdataset(files)

# Can't write out to csv with multiple dimensions so have to drop some
ds = ds.drop_dims(['diameter_aerodynamic', 'bound'])
df = ds.to_dataframe(dim_order=['time'])
df.to_csv('output_all_in_one.csv')

# Or if you want them all in separate files
print('Outputing to multiple files')
for f in files:
    ds = xr.open_mfdataset(files)
    ds = ds.drop_dims(['diameter_aerodynamic', 'bound'])
    df = ds.to_dataframe()
    df.to_csv(f+'.csv')
    ds.close()
