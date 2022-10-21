import act
import glob
import matplotlib.pyplot as plt
import json

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for MET data
datastream = 'sgpmetE13.b1'
startdate = '2019-08-30'
enddate = '2019-08-30'

#Download MET Data
act.discovery.download_data(username, token, datastream, startdate, enddate)
files = glob.glob(''.join(['./',datastream,'/*cdf']))

#Read in MET data to Standard Object
met = act.io.armfiles.read_netcdf(files)

#Display data using plotting methods
display = act.plotting.TimeSeriesDisplay(met,figsize=(10,8))
display.plot('temp_mean',color='b', label='SGP MET E13')
display.day_night_background()
plt.savefig('./images/dev_ex.png')
plt.clf()
