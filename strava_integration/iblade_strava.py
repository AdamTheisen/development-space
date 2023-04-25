import act
import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
import datetime
import xarray as xr
import sys
import pandas as pd

gpx_file = open('./data/strava_20221202.gpx', 'r')
gpx = gpxpy.parse(gpx_file)

time = []
lat = []
lon = []
alt = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            time.append(datetime.datetime(point.time.year, point.time.month, point.time.day, point.time.hour, point.time.minute, point.time.second))
            lat.append(point.latitude)
            lon.append(point.longitude)
            alt.append(point.elevation)

obj = act.io.read_csv('./data/data_12-02_16-07-59.csv')

iblade_time = []
for i, t in enumerate(obj[' Time'].values):
    iblade_time.append(pd.to_datetime(obj['Date'].values[i] + 'T' + t) + datetime.timedelta(hours=6))

obj['time'] = xr.DataArray(data=iblade_time, dims=['index'])
obj = obj.swap_dims({'index': 'time'})
obj = obj.where(obj['time'] > pd.to_datetime('2022/12/02'), drop=True)
obj2 = xr.Dataset({'latitude': xr.DataArray(data=lat, dims=['time'], coords={'time': time}),
                  'longitude': xr.DataArray(data=lon, dims=['time'], coords={'time': time})})

print(obj)
new_obj = xr.merge([obj2, obj])
display = act.plotting.GeographicPlotDisplay(new_obj)
#display.geoplot(' AQI', lat_field='latitude',
display.geoplot(' Temperature (C)', lat_field='latitude',
                lon_field='longitude', cartopy_feature=['LAKES', 'RIVERS', 'LAND', 'COASTLINE', 'OCEANS'],
                stamen='terrain')
plt.show()

#display = act.plotting.TimeSeriesDisplay(new_obj)
#display.plot('Particulate Matter-PM2.5 (ug/m&#179;)')
#plt.show()
