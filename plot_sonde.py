import act
import numpy as np

from matplotlib import pyplot as plt
import glob
import json

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for KAZR data
site = 'ena'
kazr_ds = site+'sondewnpnC1.b1'
startdate = '2021-12-12'
enddate = '2021-12-12'

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

#Download SONDE Data
files = glob.glob(''.join(['./',kazr_ds,'/*'+sdate+'*cdf']))
if len(files) == 0:
    act.discovery.download_data(username, token, kazr_ds, startdate, enddate)
    files = glob.glob(''.join(['./',kazr_ds,'/*'+sdate+'*cdf']))

test = {}
for i, f in enumerate(files):
    time = f.split('.')[-2]
    sonde_ds = act.io.armfiles.read_netcdf(f)
    test.update({time: sonde_ds})
#skewt = act.plotting.SkewTDisplay(test, figsize=(6,8),subplot_shape=(2,2))
skewt = act.plotting.SkewTDisplay(sonde_ds, figsize=(8,10))#,subplot_shape=(2,2))
skewt.plot_from_u_and_v('u_wind', 'v_wind', 'pres', 'tdry', 'dp')
plt.show()
sys.exit()

i=0
j=0
for f in files:
    print(i,j)
    time = f.split('.')[-2]
    skewt.plot_from_u_and_v('u_wind', 'v_wind', 'pres', 'tdry', 'dp',
                            subplot_index=(j, i), dsname=time, p_levels_to_plot=np.arange(10.,1000.,25))
    if j== 1:
        i += 1
        j = 0
    elif j == 0:
        j += 1
plt.tight_layout()
plt.show()

#display = act.plotting.GeographicPlotDisplay(sonde_ds)
#display.geoplot(data_field='pres', title='SGP Radiosonde Atmospheric Pressure')
#plt.show()
sonde_ds.close()
