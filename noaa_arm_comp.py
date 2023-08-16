import act
import json
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# Download NOAA moments data
result = act.discovery.download_noaa_psl_data(
    site='bck', instrument='Radar FMCW Moment',
    startdate='20220815', enddate='20220820'
)
print(result)
sys.exit()

files = glob.glob('./kps_Radar_FMCW_Moment/kps22227*.raw')
files.sort()
obj = act.io.noaapsl.read_psl_radar_fmcw_moment(files)

files = glob.glob('./bck_Radar_FMCW_Moment/bck22227*.raw')
files.sort()
bck = act.io.noaapsl.read_psl_radar_fmcw_moment(files)
#display = act.plotting.TimeSeriesDisplay(obj)
#display.plot('reflectivity_uncalibrated', cmap='jet', vmin=-20, vmax=40)
#plt.show()

# Download KAZR Data
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for KAZR data
ds = 'guckazrcfrgeM1.a1'
startdate = '2022-08-15'
enddate = '2022-08-15'

#act.discovery.download_data(username, token, ds, startdate, enddate)
files = glob.glob(''.join(['./',ds,'/*nc']))
kazr = act.io.armfiles.read_netcdf(files)
#kazr = kazr.resample(time='1Min').nearest()

#print(obj)
display = act.plotting.TimeSeriesDisplay({'KPS': obj, 'BCK': bck, 'KAZR': kazr}, subplot_shape=(3,), figsize=(12,8))
display.plot('reflectivity', dsname='KAZR', subplot_index=(0,), vmin=-40, vmax=40)
display.axes[0].set_ylim([0,10000.])
display.plot('reflectivity_uncalibrated', dsname='KPS', subplot_index=(1,), vmin=-40, vmax=40)
display.axes[1].set_ylim([0,10000.])
display.plot('reflectivity_uncalibrated', dsname='BCK', subplot_index=(2,), vmin=-40, vmax=40, add_nan=True)
display.axes[2].set_ylim([0,10000.])
plt.subplots_adjust(hspace=0.3, left=0.1)
plt.savefig('./images/arm_noaa_comparison.png')
