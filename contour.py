import matplotlib
#matplotlib.use('Agg')

import sys
sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')

import act
import glob
import matplotlib.pyplot as plt
from matplotlib import cm

import json
import xarray as xr
import numpy as np
from scipy.interpolate import griddata,bisplrep, Rbf
import sys

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

startdate = '2020-05-21'
enddate = '2020-05-21'
time = '2020-05-21T12:10:00.000000000'
date = '20200521'

#Specify datastream and date range for MET data
facs = ['E9','E13','E15','E31','E32','E33','E34','E35','E36',
       'E37','E38','E39','E40']
#facs = ['E11','E12','E13','E15','E31','E32','E33','E34','E35','E36',
#       'E37','E38','E39','E40','E41']
base = 'sgpmet'

test = {}
fields = {}
wind_fields = {}
station_fields = {}
for fac in facs:
    datastream=base+fac+'.b1'
    files = glob.glob(''.join(['./',datastream,'/*',date,'*cdf']))
    if len(files) == 0:
        act.discovery.download_data(username, token, datastream, startdate, enddate)
        files = glob.glob(''.join(['./',datastream,'/*',date,'*cdf']))

    obj = act.io.armfiles.read_netcdf(files)

    #obj = obj.sel(time=slice(time,'2019-05-08T04:05:00.000000000'))
    #obj.to_netcdf('./'+datastream+'.'+date+'.000000.cdf')
    #obj = obj.where(obj['depth'] == 5., drop=True)

 
    test.update({datastream: obj})
    fields.update({datastream: ['lon', 'lat', 'temp_mean']})
    wind_fields.update({datastream: ['lon', 'lat', 'wspd_vec_mean', 'wdir_vec_mean']})
    station_fields.update({datastream: ['lon', 'lat', 'atmos_pressure']})

display = act.plotting.ContourDisplay(test, figsize=(8,8))
display.create_contour(fields=fields, time=time, levels=50)
display.plot_vectors_from_spd_dir(fields=wind_fields, time=time, mesh=True, grid_delta=(0.1, 0.1))
display.plot_station(fields=station_fields, time=time, markersize=7,color='red')

plt.tight_layout()
plt.savefig('./images/met_contour.png',dpi=1000)

