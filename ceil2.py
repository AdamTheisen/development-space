import matplotlib
matplotlib.use('Agg')

#import sys
#sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')

import act
print(act.__file__)
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
ceil_ds = site+'ceil10mC1.b1'
startdate = '2019-05-29'
enddate = '2019-05-29'

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

#Download KAZR Data
files = glob.glob(''.join(['./',ceil_ds,'/*2020050*nc']))
if len(files) == 0:
    act.discovery.download_data(username, token, ceil_ds, startdate, enddate)
    files = glob.glob(''.join(['./',ceil_ds,'/*nc']))

# Read in KAZR data to Standard Object
ceil = act.io.armfiles.read_netcdf(files)

# Clean up QC to conform to CF conventions
uncor_ceil = ceil.copy()
print(uncor_ceil['backscatter'].attrs['units'])
cor_ceil = act.corrections.correct_ceil(ceil)
print(uncor_ceil['backscatter'].attrs['units'])


# Creat Plot Display
display = act.plotting.TimeSeriesDisplay({'Uncorrected': uncor_ceil, 'Corrected': cor_ceil}, figsize=(15,10),subplot_shape=(2,))

# Plot first_cbh data in top plot
display.plot('backscatter',dsname='Uncorrected',subplot_index=(0,))
display.plot('backscatter',dsname='Corrected',subplot_index=(1,))


# Save figure
plt.savefig('./images/ceil_cor.png')
plt.clf()
