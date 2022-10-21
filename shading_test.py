import act
from scipy.fftpack import fft, rfft,rfftfreq
import numpy as np
import glob
import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import sys
import dask


if __name__ == '__main__':
    #Read in ARM Live Data Webservice Token and Username
    with open('./token.json') as f:
        data = json.load(f)
    username = data['username']
    token = data['token']

    #Specify datastream and date range for KAZR data
    site = 'sgp'
    ds = site+'mfrsr7nchE38.b1'
    startdate = '2019-05-01'
    enddate = '2019-05-14'

    sdate = ''.join(startdate.split('-'))
    edate = ''.join(enddate.split('-'))

    #Download KAZR Data
    files = glob.glob(''.join(['./',ds,'/*'+edate+'*nc']))
    if len(files) == 0:
        act.discovery.download_data(username, token, ds, startdate, enddate)
        files = glob.glob(''.join(['./',ds,'/*'+'*nc']))

    #Read in KAZR data to Standard Object
    obj = act.io.armfiles.read_netcdf(files)

    obj = obj.sel(time=slice('2019-05-14 00:00:00', '2019-05-14 23:59:59'))
    obj.clean.cleanup()

    variable = 'diffuse_hemisp_narrowband_filter4'
    obj = act.qc.radiometer_tests.fft_shading_test(obj, variable=variable)

    # Set up plot information
    nrows = 6
    ncols = 4
    x = 0
    y = 0
    fig, ax = plt.subplots(nrows, ncols, figsize=(15,10))
    sdate = pd.to_datetime(obj['time'].values[0])
    # Get upper and lower frequencies to look for shading
    upper = obj['fft'].attrs['upper_freq']
    lower = obj['fft'].attrs['lower_freq']
    #Plots data up in hourly increments
    for i in range(24):
        dummy = obj.sel({'time': slice(sdate.replace(hour=i, minute=0, second=0),
                                       sdate.replace(hour=i, minute=0, second=0) +
                                       pd.Timedelta(1,'hours'))})

        # Shades the background of where to look for spikes
        # Plots FFT if available
        ax[x,y].set_xlim([np.nanmin(obj['fft_freq']), np.nanmax(obj['fft_freq'])])
        ax[x, y].axvspan(lower[0], upper[0], color='red', alpha=0.25)
        ax[x, y].axvspan(lower[1], upper[1], color='red', alpha=0.25)
        ax[x, y].set_title(str(i).zfill(2) + '00')
        if len(dummy['time'].values) > 1:
            ax[x, y].plot(np.transpose(dummy['fft_freq'].values), np.transpose(dummy['fft'].values),
                         'k', linestyle='solid')
        y += 1
        if y == ncols:
            y = 0
            x += 1
    plt.tight_layout()
    plt.show()


    print(obj['qc_'+variable].values)
    print(obj['qc_'+variable].attrs)

    # Creat Plot Display
    display = act.plotting.TimeSeriesDisplay(obj, figsize=(15, 10), subplot_shape=(2,))

    # Plot temperature data in top plot
    display.plot(variable, subplot_index=(0,))
    display.day_night_background()

    # Plot QC data
    display.qc_flag_block_plot(variable, subplot_index=(1,))
    plt.show()

    obj.close()
