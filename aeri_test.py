import matplotlib
#matplotlib.use('Agg')

import sys
#sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')

import act
import glob
import matplotlib.pyplot as plt
import json
import xarray as xr

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for MET data
datastream = 'sgpaerich1C1.b1'
startdate = '2019-02-15'
enddate = '2019-02-21'

#Download MET Data
files = glob.glob(''.join(['./',datastream,'/*201902*cdf']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*cdf']))
#Read in MET data to Standard Object
aeri = act.io.armfiles.read_netcdf(files)
aeri = act.retrievals.aeri.aeri2irt(aeri)
print(aeri.attrs['act_history'])

#Specify datastream and date range for MET data
datastream = 'sgpirtE13.b1'
#Download MET Data
files = glob.glob(''.join(['./',datastream,'/*cdf']))
if len(files) == 0:
    act.discovery.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*201902*cdf']))
#Read in MET data to Standard Object
irt = act.io.armfiles.read_netcdf(files)


#Display data using plotting methods
new = {'sgpaerich1C1.b1': aeri, 'sgpirtC1.b1': irt}
display = act.plotting.TimeSeriesDisplay(new,figsize=(15,10))
display.plot('aeri_irt_equiv_temperature',dsname='sgpaerich1C1.b1',color='b')
display.plot('sky_ir_temp',dsname='sgpirtC1.b1',color='g')

plt.show()

aeri.close()
irt.close()
