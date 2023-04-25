# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 15:14:32 2023

@author: matth
"""
# Import Libraries
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import act
from act.io.armfiles import read_netcdf
from act.plotting import TimeSeriesDisplay
import fsspec
from datetime import datetime, date
import pytz

# Renaming of variables and adding units to each variable.
# Ambient weather station
attrs_dict_ambient = {'tempf': {'standard_name': 'Temperature',
                                'units': 'degF'},
                      'tempinf': {'standard_name': 'Temperature',
                                  'units': 'degF'},
                      'feelsLike': {'standard_name': 'Feels Like Temperature',
                                    'units': 'degF'},
                      'dewPoint': {'standard_name': 'Dewpoint Temperature',
                                   'units': 'degF'},
                      'dewPointin': {'standard_name': 'Dewpoint Temperature',
                                     'units': 'degF'},
                      'windspeedmph': {'standard_name': 'Wind Speed',
                                       'units': 'mph'},
                      'winddir': {'standard_name': ' Wind Direction',
                                  'units': 'Degrees 0-360'},
                      'windgustmph': {'standard_name': 'Wind Gust last 10 min',
                                      'units': 'mph'},
                      'windgustdir': {'standard_name': 'Wind direction of gust',
                                      'units': 'Degrees 0-360'},
                      'hourlyrainin': {'standard_name': 'Hourly Rain Rate',
                                       'units': 'in/hr'},
                      'dailyrainin': {'standard_name': 'Daily Rain',
                                      'units': 'inches'},
                      'eventrainin': {'standard_name': 'Event Rain',
                                      'units': 'inches'},
                      'baromrelin': {'standard_name': 'Relative Pressure',
                                     'units': 'inHg'},
                      'baromabsin': {'standard_name': 'Absolute Pressure',
                                     'units': 'inHg'},
                      'solarradiation': {'standard_name': 'Solar Radiation',
                                         'units': 'W/m^2'},
                      'pm25': {'standard_name': 'PM 2.5',
                               'units': 'ug/m^3'},
                      'pm25_24h': {'standard_name': 'PM2.5 Air Quality 24 hour average',
                                   'units': 'ug/m^3'},
                      'battout': {'standard_name': 'Outdoor Battery',
                                  'units': '1=ok,0=low'},
                      'batt_25': {'standard_name': 'PM 2.5 Battery Power',
                                  'units': '1=ok,0=low'}}

variable_mapping_ambient = {'date': 'time',
                            'tempf': 'outdoor_temperature',
                            'tempinf': 'indoor_temperature',
                            'dewPoint': 'outdoor_dewpoint',
                            'dewPointin': 'indoor_dewpoint',
                            'feelsLike': 'feelslike_temperature',
                            'winddir': 'wind_direction',
                            'windspeedmph': 'wind_speed',
                            'windgustmph': 'wind_gust',
                            'windgustdir': 'wind_gust_direction',
                            'hourlyrainin': 'hourly_rain',
                            'dailyrainin': 'daily_rain',
                            'eventrainin': 'event_rain',
                            'baromrelin': 'relative_pressure',
                            'baromabsin': 'absolute_pressure',
                            'solarradiation': 'solar_radiation',
                            'pm25': 'pm25_outdoor',
                            'pm25_24h': 'pm25_24hr',
                            'battout': 'station_battery',
                            'batt_25': 'pm25_battery'
                            }

# ATMOS 60m tower
attrs_dict_tower = {'TaC_60m': {'standard_name': 'Average 60 m temperature',
                                'units': 'degC'},
                    'spd_60m': {'standard_name': 'Average 60 m wind speed',
                                'units': 'm/s'},
                    'spdv60m': {'standard_name': 'Vector-averaged 60 m wind speed',
                                'units': 'm/s'},
                    'dirV60m': {'standard_name': 'Vector-averaged 60 m wind direction',
                                'units': 'Degees 0-360'},
                    'sdir60m': {'standard_name': 'Standard deviation of 60 m wind direction',
                                'units': 'Degrees 0-360'},
                    'e_10m': {'standard_name': 'Average 10 m vapor pressure',
                              'units': 'kPa'},
                    'rh_10m': {'standard_name': 'Average 10 m relative humidity',
                               'units': 'Percent (%)'},
                    'Tdp_10m': {'standard_name': 'Average 10 m dew point temperature',
                                'units': 'degC'},
                    'TaC_10m': {'standard_name': 'Average 10 m temperature',
                                'units': 'degC'},
                    'spd_10m': {'standard_name': 'Average 10 m wind speed',
                                'units': 'm/s'},
                    'spdV10m': {'standard_name': 'Vector-averaged 10 m wind speed',
                                'units': 'm/s'},
                    'dirV10m': {'standard_name': 'Average 10 m Vector-average 10m wind direction',
                                'units': 'Degrees 0-360'},
                    'sdir10m': {'standard_name': 'Standard deviation of 10 m wind direction',
                                'units': 'Degress 0-360'},
                    'baroKPa': {'standard_name': 'Average station barometric pressure',
                                'units': 'kPa'},
                    'radW/m2': {'standard_name': 'Average global irradiation',
                                'units': 'W/m^2'},
                    'netW/m2': {'standard_name': 'Average net radiation',
                                'units': 'W/m^2'},
                    'Ta_diff': {'standard_name': 'Average temperature different per meter',
                                'units': 'degC/m'},
                    'asp_60m': {'standard_name': '60 m aspirator flow monitor',
                                'units': 'Percent (%) of time flow above minimum'},
                    'asp_10m': {'standard_name': '10 m aspirator flow monitor',
                                'units': 'Percent (%) of time flow above minimum'},
                    'battVDC': {'standard_name': 'Battery voltage monitor',
                                'units': 'V'},
                    'precpmm': {'standard_name': 'Average precipitation',
                                'units': 'mm'}}

variable_mapping_tower = {'TaC_60m': '60m_temperature',
                          'spd_60m': '60m_windspeed',
                          'spdv60m': 'Vector_avg_60m_windspd',
                          'dirV60m': 'Vector_avg_60m_winddir',
                          'sdir60m': 'StdDev_60m_winddir',
                          'e_10m': '10m_vapor_pres',
                          'rh_10m': '10m_relhumidity',
                          'Tdp_10m': '10m_dewpoint',
                          'TaC_10m': '10m_temperature',
                          'spd_10m': '10m_windspeed',
                          'spdV10m': 'vector_avg_10m_windspd',
                          'dirV10m': 'vector_avg_10m_winddir',
                          'sdir10m': 'stdDev_10m_winddir',
                          'baroKPa': 'absolute_pressure',
                          'radW/m2': 'global_irradiation',
                          'netW/m2': 'net_radiation',
                          'Ta_diff': 'temperature_diff',
                          'asp_60m': '60m_asp',
                          'asp_10m': '10m_asp',
                          'precpmm': 'precip'}


# Opens ambient weather for selected date off of CROCUS github
# To pull today's date
today = date.today()
date_format = today.strftime("%Y%m%d")
# Splice the date into the format needed to pull Ambient Data
year = date_format[0:4]
month = date_format[4:6]
day = date_format[6:8]
github_url = (
    'https://github.com/CROCUS-Urban/instrument-cookbooks/raw/main/data/surface-meteorology/'+year+'/'+month+'/'+day+'/'+'ambient.a1.'+year+month+day+'.nc#mode=bytes')

# Opens the file off of github
ncfile = fsspec.open(github_url)
ds_ambient = xr.open_dataset(ncfile.open(), engine='h5netcdf')


# Lopping through to rename variables
for variable in attrs_dict_ambient.keys():
    if variable in list(ds_ambient.variables):
        ds_ambient[variable].attrs = attrs_dict_ambient[variable]

# Lists what variables we can pull and what they provide to have a common
# name list.
theirvariables = sorted(list(ds_ambient.variables))
ourvariables = sorted(list(variable_mapping_ambient.keys()))
sharedvariables = dict()
for variable in theirvariables:
    if variable in ourvariables:
        sharedvariables[variable] = variable_mapping_ambient[variable]
# Rename variables
ds_ambient = ds_ambient.rename(sharedvariables)

# Average to match Tower's 15min data
ds_ambient = ds_ambient.resample(time='15min').mean()

# needs to be updated.
ds_ambient = ds_ambient.assign(abs_press_hPa=(
    (ds_ambient['absolute_pressure'])*33.86389))
ds_ambient['abs_press_hPa'].attrs['units'] = 'hPa'

ds_ambient = ds_ambient.assign(
    mslp_hPa=((ds_ambient['relative_pressure'])*33.86389))
ds_ambient['mslp_hPa'].attrs['units'] = 'hPa'


###############################################################################
# This section reads in the last 48 hrs of tower
# Defining the pre-determined name of columns from the tower's website.
cols = ['JDA', 'T_LST', 'TaC_60m', 'spd_60m', 'spdv60m', 'dirV60m', 'sdir60m', 'e_10m',
        'rh_10m', 'Tdp_10m', 'TaC_10m', 'spd_10m', 'spdV10m', 'dirV10m', 'sdir10m',
        'baroKPa', 'radW/m2', 'netW/m2', 'Ta_diff', 'asp_60m', 'asp_10m', 'battVDC',
        'precpmm', 'T_LST2', 'JDA2']

# Link to latest 48 hr tower data.
url = 'https://www.atmos.anl.gov/ANLMET/anltower.48'

# Reads in the tower data into pandas from the URL. This will also skips
# the extra header information on the web page and removes the last line
# which restates the column names.
df = pd.read_table(url, sep='\s+',  skiprows=[0, 1], header=None, names=cols,
                   na_values=-99999.00)

# Changing the data types from Object to float for most of the columns.
df[['TaC_60m', 'spd_60m', 'spdv60m', 'dirV60m', 'sdir60m', 'e_10m', 'rh_10m',
    'Tdp_10m', 'TaC_10m', 'spd_10m', 'spdV10m', 'dirV10m', 'sdir10m', 'baroKPa',
    'radW/m2', 'netW/m2', 'Ta_diff', 'asp_60m', 'asp_10m', 'battVDC',
    'precpmm']] = df[['TaC_60m', 'spd_60m', 'spdv60m', 'dirV60m', 'sdir60m',
                      'e_10m', 'rh_10m', 'Tdp_10m', 'TaC_10m', 'spd_10m',
                                 'spdV10m', 'dirV10m', 'sdir10m', 'baroKPa',
                                 'radW/m2', 'netW/m2', 'Ta_diff', 'asp_60m',
                                 'asp_10m', 'battVDC',
                                 'precpmm']].apply(pd.to_numeric,
                                                   errors='coerce')

# Drops the indexing column of random numbers
df = df.reset_index(drop=True)
df = df.head(-1)

# Creates an new column of the date and time in UTC.
df['time'] = ""
for i in range(len(df.JDA)):
    doy = df.JDA[i]
    merged_date = datetime.strptime(
        year + "-" + df.JDA[i], "%Y-%j").strftime("%Y-%m-%d")
    local = pytz.timezone("US/Central")
    naive = datetime.strptime(
        merged_date + ' ' + df.T_LST[i], "%Y-%m-%d %H:%M")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    utc_dt = utc_dt.replace(tzinfo=None)
    df['time'][i] = datetime.strptime(str(utc_dt), "%Y-%m-%d %H:%M:%S")

# Converts the date and time into a datetime64 type.
df['time'] = df['time'].astype('datetime64')

# Changes indexing column to date and time in UTC
df.set_index('time', inplace=True)

# Deletes the last 2 rows that contains date and time again
tower_data = df.iloc[:, :-2]

# Converts it to an xarray dataset
ds_tower = tower_data.to_xarray()

# Lopping through to rename variables
for variable in attrs_dict_tower.keys():
    if variable in list(ds_tower.variables):
        ds_tower[variable].attrs = attrs_dict_tower[variable]

# Rename the variables
ds_tower = ds_tower.rename(variable_mapping_tower)

# Convert tower variables and adding them to ds_tower
# 60m temperature
ds_tower = ds_tower.assign(degF_60m_temperature=(
    (ds_tower['60m_temperature'] * 9/5)+32))
ds_tower['degF_60m_temperature'].attrs['units'] = 'degF'

# 10m temperature
ds_tower = ds_tower.assign(degF_10m_temperature=(
    (ds_tower['10m_temperature'] * 9/5)+32))
ds_tower['degF_10m_temperature'].attrs['units'] = 'degF'

# 60m wind speed
ds_tower = ds_tower.assign(windspdmph_60m=((ds_tower['60m_windspeed'])*2.237))
ds_tower['windspdmph_60m'].attrs['units'] = 'mph'

# 10m wind speed
ds_tower = ds_tower.assign(windspdmph_10m=((ds_tower['10m_windspeed'])*2.237))
ds_tower['windspdmph_10m'].attrs['units'] = 'mph'

# Converting absolute pressure into hPa form kPa
ds_tower = ds_tower.assign(abs_press_hPa=(
    (ds_tower['absolute_pressure'])*10.0))
ds_tower['abs_press_hPa'].attrs['units'] = 'hPa'

# Converting precip from mm to inch
ds_tower = ds_tower.assign(precipin=ds_tower['precip']/25.4)
ds_tower['precipin'].attrs['units'] = 'inches'

# Creating a running total for rainfall in inches
ds_tower = ds_tower.assign(total_precipin=ds_tower.precipin.cumsum("time"))
ds_tower['total_precipin'].attrs['units'] = 'inches'

##############################################################################
# Transpose the data to be usable within ACT. Commented out for now 
# since data is reading without the .transpose
#act_ambient = ds_ambient.transpose()
#act_ambient = act_ambient.load()
#act_tower = ds_tower.transpose()


# Plotting the data using ACT

display = act.plotting.TimeSeriesDisplay(
    {'ds_ambient': ds_ambient, 'ds_tower': ds_tower})

display.plot('total_precipin', 'ds_tower', force_line_plot=True,
             labels='Tower Tipping Bucket', set_title=('Daily Rain for '+year+month+day))
display.plot('daily_rain', 'ds_ambient', force_line_plot=True,
             labels=True)
# display.plot('degF_60m_temperature', 'ds_tower',force_line_plot=True,
#             labels='60m Temperature')

plt.show()
