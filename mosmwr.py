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
site = 'mos'
kazr_ds = site+'mwrlosM1.b1'
startdate = '2020-01-01'
enddate = '2020-10-01'

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

#Download KAZR Data
files = glob.glob(''.join(['./',kazr_ds,'/*'+'202004*cdf']))

#Read in KAZR data to Standard Object
ds = act.io.armfiles.read_netcdf(files)

#Display data using plotting methods
display = act.plotting.TimeSeriesDisplay(ds,figsize=(15,10))
display.plot('vap')
display.axes[0].set_ylim([0,2])
plt.savefig('./images/mosmwr_pwv.png')
plt.clf()
