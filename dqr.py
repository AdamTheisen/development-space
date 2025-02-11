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
site = 'anx'
ds = site+'metM1.b1'
startdate = '2019-06-01'
enddate = '2020-06-30'

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

files = glob.glob(''.join(['./data/',ds,'/*cdf']))

# Read in KAZR data to Standard Object
obj = act.io.arm.read_arm_netcdf(files)

variable = 'temp_mean'
assessment = 'incorrect,suspect'
obj = act.qc.arm.add_dqr_to_qc(obj, variable=variable)

# Creat Plot Display
display = act.plotting.TimeSeriesDisplay(obj,figsize=(15,10),subplot_shape=(2,))
# Plot first_cbh data in top plot
display.plot(variable,subplot_index=(0,))
# Plot QC data
display.qc_flag_block_plot(variable,subplot_index=(1,))
#plt.show()
# Save figure
plt.savefig('./images/dqr_qc.png')
plt.clf()

#obj.close()
