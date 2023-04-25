from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from act.io.csvfiles import read_csv
from act.plotting import GeographicPlotDisplay
import re

filename = Path('./data/', 'data_12-02_16-07-59.csv')
ds = read_csv(filename, parse_dates={'time': [0,1]})

print(ds)
sys.exit()
ds['time'].values = ds['time'].values + np.timedelta64(5, 'h')
ds = ds.assign_coords(time=ds['time'])
ds = ds.swap_dims({'index': 'time'})
ds = ds.drop('index')
ds = ds.rename({'Latitude': 'latitude', 'Longitude': 'longitude'})
display = GeographicPlotDisplay({'pocketLab': ds})
display.geoplot('Particulate Matter-PM10 (ug/m&#179;)', lat_field='latitude', 
                lon_field='longitude', cartopy_feature=['LAKES', 'RIVERS', 'LAND', 'COASTLINE', 'OCEANS'], stamen='terrain')

plt.tight_layout()
plt.subplots_adjust(hspace=0.4)
plt.show()
