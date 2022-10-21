"""
===========================================
Example on plotting timeseries of ASOS data
===========================================

This example shows how to plot timeseries of ASOS data from
Chicago O'Hare airport.

"""

# Import the necessary libraries
# act can be installed through pip install act-atmos
import act
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Set station id and time range to pull data
station = "1M4"
time_window = [datetime(2020, 1, 1, 0, 0), datetime(2020, 12, 31, 23, 59)]

# Library will go get data and return it in an xarray object
my_asoses = act.discovery.get_asos(time_window, station=station)

# Note, s function's actual return is a dictionary so you could do multiple sites
obj = my_asoses[station]

# Examples on using ACT to plot, otherwise you could easily do your analysis
# and plot using matplotlib
my_disp = act.plotting.TimeSeriesDisplay(obj)
title = ' '.join([station, 'Temperature for', time_window[0].strftime('%m/%d/%y'),
        '-', time_window[-1].strftime('%m/%d/%y')])
my_disp.plot('temp', set_title=title)
plt.show()

# Remove all winds where speed is 0
obj = obj.where(obj['spdms'] > 0, drop=True)

# Plots up a windrose using ACT
windrose = act.plotting.WindRoseDisplay(obj, figsize=(10,8))
title = ' '.join([station, 'Wind Rose for', time_window[0].strftime('%m/%d/%y'),
        '-', time_window[-1].strftime('%m/%d/%y')])
windrose.plot('drct','spdms',spd_bins=np.linspace(0, 10, 5), set_title=title)
windrose.axes[0].legend(loc=(-0.1,0.1))
plt.show()
