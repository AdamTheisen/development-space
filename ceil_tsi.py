# You can install ACT by cloning from github which is recommended
# and then installing using "python setup.py develop" from the base ACT directory
import sys
import act
import glob
import json
import matplotlib.pyplot as plt
import sys
import datetime
import numpy as np


if __name__ == '__main__':
    # Read in ARM Live Data Webservice Token and Username
    # https://adc.arm.gov/armlive/
    # Assumes credentials are stored in token.json file in the format:
    #{
    #   "username": "name",
    #   "token":"tokenvalue"
    #}
    with open('./token.json') as f:
        data = json.load(f)
    username = data['username']
    token = data['token']

    # Specify datastream and date range for CEIL data
    site = 'sgp'
    ds = site+'ceil10mC1.b1'
    startdate = '2020-05-05'
    enddate = '2020-05-06'

    # Download CEIL Data
    files = glob.glob(''.join(['./',ds,'/*nc']))
    if len(files) == 0:
        result = act.discovery.download_data(username, token, ds, startdate, enddate)
        files = glob.glob(''.join(['./',ds,'/*nc']))
    files.sort()

    # Read in data to Standard Object
    ceil = act.io.armfiles.read_netcdf(files)

    # Correct CEIL data for easier visualization
    ceil = act.corrections.ceil.correct_ceil(ceil, -9999)

    # Get TSI data
    ds = site + 'tsiskycoverC1.b1'
    files = glob.glob(''.join(['./',ds,'/*cdf']))
    if len(files) == 0:
        result = act.discovery.download_data(username, token, ds, startdate, enddate)
        files = glob.glob(''.join(['./',ds,'/*cdf']))
    files.sort()

    # Read in data to Standard Object
    tsi = act.io.armfiles.read_netcdf(files)

    # Creat Plot Display
    display = act.plotting.TimeSeriesDisplay({'CEIL': ceil, 'TSI': tsi},
        figsize=(15, 10), subplot_shape=(3,))
    display.plot('backscatter', dsname='CEIL', subplot_index=(0,))
    display.plot('count_opaque', dsname='TSI', subplot_index=(1,), label='Opaque Counts')
    display.plot('count_thin', dsname='TSI', subplot_index=(1,), label='Thin Counts')
    display.axes[1].legend()
    display.plot('percent_opaque', dsname='TSI', subplot_index=(2,), label='Percent Opaque')
    display.plot('percent_thin', dsname='TSI', subplot_index=(2,), label='Percent Thin')
    display.axes[2].set_ylim([0, 100])
    display.axes[2].legend()
    plt.show()
    display.close()
    obj.close()
