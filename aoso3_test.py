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

    # Specify datastream and date range for AOSO3 data
    site = 'sgp'
    ds = site+'aosnephdry1mE13.b1' # Could easily change this to aosnephE13.b1
    startdate = '2020-02-01'
    enddate = '2020-02-07'

    # Download AOSNEPH Data
    files = glob.glob(''.join(['./',ds,'/*nc']))
    if len(files) == 0:
        result = act.discovery.download_data(username, token, ds, startdate, enddate)
        files = glob.glob(''.join(['./',ds,'/*nc']))
    files.sort()


    # Read in data to Standard Object
    obj = act.io.armfiles.read_netcdf(files)

    # Add the solar variable, including dawn/dusk to variable
    obj = act.utils.geo_utils.add_solar_variable(obj, dawn_dusk=True)

    print(np.sum(obj['sun_variable'].values))

    # Using the sun variable, only analyze nighttime data
    obj = obj.where(obj['sun_variable'] == 0)

    # This line will resample the data to 1 day means
    obj = obj.resample(time='1d', skipna=True, keep_attrs=True).mean()
    print(obj['Bs_B_Dry_Neph3W'].values)

    # Creat Plot Display
    display = act.plotting.TimeSeriesDisplay(obj, figsize=(15, 10))
    display.plot('Bs_B_Dry_Neph3W', linestyle='solid')
    display.day_night_background()
    plt.show()
    display.close()
    obj.close()
