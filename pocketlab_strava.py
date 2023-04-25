import act
import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
import datetime
import xarray as xr
import sys

gpx_file = open('./Data/pocketlab/20221109_strava.gpx', 'r')
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

start = datetime.datetime(2022, 11, 9, 21, 14, 00)
obj = act.io.read_csv('./Data/pocketlab/20221109.csv')
pocketlab_time = []
for s in obj['Elapsed Seconds'].values:
    pocketlab_time.append(start + datetime.timedelta(seconds=s*3))

obj['time'] = xr.DataArray(data=pocketlab_time, dims=['index'])
obj = obj.swap_dims({'index': 'time'})
obj2 = xr.Dataset({'latitude': xr.DataArray(data=lat, dims=['time'], coords={'time': time}),
                  'longitude': xr.DataArray(data=lon, dims=['time'], coords={'time': time})})


new_obj = xr.merge([obj, obj2])
display = act.plotting.GeographicPlotDisplay(new_obj)
display.geoplot('Particulate Matter-PM2.5 (ug/m&#179;)', lat_field='latitude',
                lon_field='longitude', cartopy_feature=['LAKES', 'RIVERS', 'LAND', 'COASTLINE', 'OCEANS'],
                stamen='terrain')
plt.show()

#display = act.plotting.TimeSeriesDisplay(new_obj)
#display.plot('Particulate Matter-PM2.5 (ug/m&#179;)')
#plt.show()
