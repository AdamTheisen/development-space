#! /usr/bin/env python3
import act
import glob
import json
import numpy as np
import dask
import sys
import time
from scipy.optimize import brent, brentq
import matplotlib.pyplot as plt


if __name__ == '__main__':
    #Read in ARM Live Data Webservice Token and Username
    with open('./token.json') as f:
        data = json.load(f)
    username = data['username']
    token = data['token']

    #Specify datastream and date range for KAZR data
    site = 'mar'
    kazr_ds = site+'irtsstM1.b1'
    startdate = '2018-03-01'
    enddate = '2018-03-30'

    sdate = ''.join(startdate.split('-'))
    edate = ''.join(enddate.split('-'))

    #Download KAZR Data
    files = glob.glob(''.join(['./',kazr_ds,'/*nc']))

    if len(files) == 0:
        act.discovery.download_data(username, token, kazr_ds, startdate, enddate)
        files = glob.glob(''.join(['./',kazr_ds,'/*nc']))

    # Read in KAZR data to Standard Object
    obj = act.io.armfiles.read_netcdf(files)
    obj = obj.resample(time='1h').mean()
    t = time.time()
    #obj = sst_from_irt(obj)
    obj = act.retrievals.irt.sst_from_irt(obj)
    print(obj['sea_surface_temperature'])
    print(obj)
    display = act.plotting.TimeSeriesDisplay(obj,figsize=(8,5))
    display.plot('sky_ir_temp',color='m', label='Sky Infrared Temperature')
    display.plot('sfc_ir_temp',color='c', label='Surface Infrared Temperature', marker='s')
    display.plot('sea_surface_temperature',color='b', label='Sea Surface Temperature')
    display.axes[0].legend()
    plt.show()
    obj.close()
