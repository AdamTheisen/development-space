import act

site = 'tbl'
#results = act.discovery.get_surfrad.get_surfrad_data(site, startdate='20230601', enddate='20230601')
results = ['https://gml.noaa.gov/aftp/data/radiation/surfrad/Boulder_CO/2023/tbl23007.dat', 'https://gml.noaa.gov/aftp/data/radiation/surfrad/Boulder_CO/2023/tbl23008.dat']

ds = act.io.noaagml.read_surfrad(results)
print(ds['qc_temperature'].attrs)
