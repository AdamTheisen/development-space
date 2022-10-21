import urllib.request, json
import datetime
import numpy as np

import act
import matplotlib.pyplot as plt
import glob

web = 'https://adc.arm.gov/arm-pmreport-api/report/search/spec?params=reportInstrumentClass~precipmet&pageInt=0&pageSize=20&sort=reportId&sortDir=DESC'

with urllib.request.urlopen(web) as url:
    data = json.loads(url.read().decode())

temp = []
date = []
time = []
for d in data['content']:
    if d['reportFacilityCode'] != 'I10':
        continue
    report = json.loads(d['reportData'])
    d = report['date']
    t = report['time']
    if 'tempValue' in report:
        temp.append(float(report['tempValue']))
        date.append(np.datetime64(datetime.datetime.utcfromtimestamp(d/1000)+datetime.timedelta(hours=int(t[0:2]), minutes=int(t[2:]))))


#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for MET data
datastream = 'sgpprecipmetI10.b1'
startdate = '2020-08-01'
enddate = '2020-08-09'

#Download MET Data
act.discovery.download_data(username, token, datastream, startdate, enddate)
files = glob.glob(''.join(['./',datastream,'/*nc']))
    
#Read in MET data to Standard Object
obj = act.io.armfiles.read_netcdf(files)

obj['pm_temp'] = ('pmtime', np.array(temp), {'long_name': 'PM Reported Temperature', 'units': 'C'})
obj['pmtime'] = ('pmtime', np.array(date), {'long_name': 'Date'})

display = act.plotting.TimeSeriesDisplay(obj, figsize=(8,5))
display.plot('temp_mean', label='sgpprecipmetI10.b1')
title = 'SGP PRECIPMET I10 Mean Temperature'
display.plot('pm_temp', color='r', marker='s',markersize=8, set_title=title, label='PM Report')
display.day_night_background()
display.axes[0].legend()
plt.show()

obj.close()
