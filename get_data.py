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
startdate = '2024-12-01'
enddate = '2024-12-10'

sdate = ''.join(startdate.split('-'))
edate = ''.join(enddate.split('-'))

datastream = 'bnfsirsM1.b1'
data_dir = './data/' + datastream
result = act.discovery.download_arm_data(username, token, datastream, startdate, enddate, output=data_dir)
