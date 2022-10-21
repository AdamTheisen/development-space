import sys
sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')
import act
print(act.__file__)
import os

token = os.getenv("AIRNOW_API")

results = act.discovery.get_AirNow_forecast(token, '2022-05-01', zipcode=60108, distance=50)
assert results['CategoryName'].values[0] == 'Good'
assert results['AQI'].values[2] == -1
assert results['ReportingArea'][3] == 'Chicago'


results = act.discovery.get_AirNow_forecast(token, '2022-05-01', distance=50, latlon=[41.958, -88.12])
assert results['CategoryName'].values[3] == 'Good'
assert results['AQI'].values[2] == -1
assert results['ReportingArea'][3] == 'Aurora and Elgin'


results = act.discovery.get_AirNow_obs(token, date='2022-05-01', zipcode=60108, distance=50)
assert results['AQI'].values[0] == 31
assert results['ParameterName'].values[1] == 'PM2.5'
assert results['CategoryName'].values[0] == 'Good'

results = act.discovery.get_AirNow_obs(token, date='2022-05-01', distance=50, latlon=[41.958, -88.12])
assert results['AQI'].values[0] == 30
assert results['ParameterName'].values[1] == 'PM2.5'
assert results['CategoryName'].values[0] == 'Good'

lat_lon = '-88.245401,41.871346,-87.685099,42.234359'
results = act.discovery.get_AirNow_bounded_obs(token, '2022-05-01T00', '2022-05-01T12', lat_lon,
    'OZONE,PM25', data_type='B')
assert results['PM2.5'].values[-1, 0] == 1.8
assert results['OZONE'].values[0, 0] == 37.0
assert len(results['time'].values) == 13
