import matplotlib
matplotlib.use('Agg')

import act
import glob
import matplotlib.pyplot as plt
import json

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for KAZR data
site = 'sgp'
kazr_ds = site+'metE13.b1'
startdate = '2019-05-29'
enddate = '2019-05-30'

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

#Download KAZR Data
files = act.tests.sample_files.EXAMPLE_MET1

# Read in KAZR data to Standard Object
obj = act.io.armfiles.read_netcdf(files)

obj = act.utils.inst_utils.decode_present_weather(obj, variable='pwd_pw_code_inst')

print(obj['pwd_pw_code_inst_decoded'].values[0])

obj.close()
