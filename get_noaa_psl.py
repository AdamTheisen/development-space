try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

import json
from datetime import datetime
import pandas as pd
import numpy as np
import os


site = 'ctd'
instrument = 'Datalogger'
sdate = '20211231'
edate = '20220101'
datastream = site+instrument
output = None

s_doy = datetime.strptime(sdate,'%Y%m%d').timetuple().tm_yday
year = datetime.strptime(sdate,'%Y%m%d').year
e_doy = datetime.strptime(edate,'%Y%m%d').timetuple().tm_yday


url = 'https://downloads.psl.noaa.gov/psd2/data/realtime/'

met_ds = ['Pressure', 'Datalogger', 'Temp', 'RH', 'Net Radiation', 'Temp/RH',
          'Solar Radiation', 'Tipping Bucket', 'TBRG', 'Wind', 'Wind Speed',
          'Wind Direction', 'Wind Speed and Direction']

if 'Parsivel' in instrument:
    url += 'DisdrometerParsivel/Stats/'
elif any([d in instrument for d in met_ds]):
    url += 'CsiDatalogger/SurfaceMet/'
elif 'GpsTrimble' in instrument:
    url += 'GpsTrimble/WaterVapor/'
elif 'Radar S-band Moment' in instrument:
    url += 'Radar3000/PopMoments/'
elif 'Radar S-band Bright Band' in instrument:
    url += 'Radar3000/BrightBand/'
elif '449RWP Bright Band' in instrument:
    url += 'Radar449/BrightBand/'
elif '449RWP Wind' in instrument:
    url += 'Radar449/WwWind/'
elif '449RWP Sub-Hour Wind' in instrument:
    url += 'Radar449/WwWindSubHourly/'
elif '449RWP Sub-Hour Temp' in instrument:
    url += 'Radar449/WwTempSubHourly/'
elif '915RWP Wind' in instrument:
    url += 'Radar915/WwWind/'
elif '915RWP Temp' in instrument:
    url += 'Radar915/WwTemp/'
elif '915RWP Sub-Hour Wind' in instrument:
    url += 'Radar915/WwWindSubHourly/'
elif '915RWP Sub-Hour Temp' in instrument:
    url += 'Radar915/WwTempSubHourly/'
elif 'Radar FMCW Moment' in instrument:
    url += 'RadarFMCW/PopMoments/'
elif 'Radar FMCW Bright Band' in instrument:
    url += 'RadarFMCW/BrightBand/'

# construct output directory
if output:
    # output files to directory specified
    output_dir = os.path.join(output)
else:
    # if no folder given, add datastream folder
    # to current working dir to prevent file mix-up
    output_dir = os.path.join(os.getcwd(), datastream)

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

prev_doy = 0
if e_doy < s_doy:
    r = list(range(s_doy, 366)) + list(range(1, e_doy + 1))
else:
    r = list(range(s_doy, e_doy + 1))

filenames = []
for doy in r:
    if prev_doy > doy:
        year += 1
    new_url = url + site + '/' + str(year) + '/' + str(doy).zfill(3) +'/'
    files = pd.read_html(new_url, skiprows=[1])[0]['Name']
    files = list(files[1:-1])

    for f in files:
        output_file = os.path.join(output_dir, f)
        try:
            print('Downloading ' + f)
            with open(output_file, 'wb') as open_bytes_file:
                open_bytes_file.write(urlopen(new_url + f).read())
            filenames.append(output_file)
        except Exception:
            pass
    prev_doy = doy
print(filenames)
