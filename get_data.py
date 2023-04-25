import matplotlib
matplotlib.use('Agg')

import act
import glob
import matplotlib.pyplot as plt
import json
import sys

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for KAZR data
site = 'sgp'
startdate = '2022-08-15'
enddate = '2022-08-15'

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))


datastream = 'guckazrcfrgeM1.a1'
result = act.discovery.download_data(username, token, datastream, startdate, enddate)
