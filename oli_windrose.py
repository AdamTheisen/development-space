import act
import glob
import matplotlib.pyplot as plt
import json
import numpy as np

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Specify datastream and date range for MET data
datastream = 'sgpmetE13.b1'
startdate = '2020-05-01'
enddate = '2020-05-31'

#Download MET Data
act.discovery.download_data(username, token, datastream, startdate, enddate)
files = glob.glob(''.join(['./',datastream,'/*']))

#Read in MET data to Standard Object
obj = act.io.armfiles.read_netcdf(files)

windrose = act.plotting.WindRoseDisplay(obj,figsize=(10,8))
title = 'SGP MET Wind Rose for May 2020'
windrose.plot('wdir_vec_mean','wspd_vec_mean',spd_bins=np.linspace(0, 10, 5), set_title=title)
windrose.axes[0].legend(loc=(-0.1,0.1))
plt.show()
obj.close()
