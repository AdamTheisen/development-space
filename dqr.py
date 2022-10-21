import matplotlib
matplotlib.use('Agg')
import act
import glob
import matplotlib.pyplot as plt
import json
import requests
import datetime as dt
import numpy as np

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for KAZR data
site = 'sgp'
ds = site+'30ebbrE13.b1'
startdate = '2020-01-27'
enddate = '2020-01-29'

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

#Download KAZR Data
files = glob.glob(''.join(['./',ds,'/*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, ds, startdate, enddate)
    files = glob.glob(''.join(['./',ds,'/*nc']))

# Read in KAZR data to Standard Object
obj = act.io.armfiles.read_netcdf(files)

variable = 'latent_heat_flux'
assessment = 'incorrect,suspect'
obj = act.qc.arm.add_dqr_to_qc(obj, variable=variable)

# Creat Plot Display
display = act.plotting.TimeSeriesDisplay(obj,figsize=(15,10),subplot_shape=(2,))
# Plot first_cbh data in top plot
display.plot(variable,subplot_index=(0,))
# Plot QC data
display.qc_flag_block_plot(variable,subplot_index=(1,))
# Save figure
plt.savefig('./images/dqr_qc.png')
plt.clf()

obj.close()
