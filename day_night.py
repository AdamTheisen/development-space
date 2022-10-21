import sys
#sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')
import act
import glob
import matplotlib.pyplot as plt
import json
import xarray as xr
import numpy as np

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for MET data
datastream = 'sgpmetE13.b1'
datastream = 'mosgndirtS3.b1'
startdate = '2019-12-15'
enddate = '2019-12-15'

#Download MET Data
files = glob.glob(''.join(['./',datastream,'/*20191215*c*']))

#Read in MET data to Standard Object
obj = act.io.armfiles.read_netcdf(act.tests.EXAMPLE_IRTSST)
obj = obj.fillna(0)

result = act.utils.geo_utils.add_solar_variable(obj, dawn_dusk=False)

print(list(result['sun_variable'].values))
print(np.sum(result['sun_variable'].values))

obj.close()
