import matplotlib
#matplotlib.use('Agg')
import act
import glob
import matplotlib.pyplot as plt
import json
import pyart

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for KAZR data
site = 'sgp'
ceil_ds = site+'dlppiC1.b1'
startdate = '2019-05-29'
enddate = '2019-05-29'

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

#Download KAZR Data
files = glob.glob(''.join(['./',ceil_ds,'/*cdf']))
if len(files) == 0:
    files = act.discovery.download_data(username, token, ceil_ds, startdate, enddate)

# Read in KAZR data to Standard Object
obj = act.io.armfiles.read_netcdf(files)

#radar = act.utils.create_pyart_obj(obj, azimuth='azimuth', elevation='elevation',
#                                   range_var='range', sweep_az_thresh=360)

#display = pyart.graph.RadarDisplay(radar)
#display.plot('radial_velocity', sweep=0, title_flag=False, vmin=-10., vmax=10., cmap='jet')
#plt.show()

wind_obj = act.retrievals.compute_winds_from_ppi(obj, snr_threshold=1.005)
display = act.plotting.TimeSeriesDisplay(wind_obj)
display.plot_barbs_from_spd_dir('wind_direction', 'wind_speed', invert_y_axis=False)
plt.show()
