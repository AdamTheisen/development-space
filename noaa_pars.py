import pandas as pd
import act
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt


names = ['time', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12',
         'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B22','B23','B24',
         'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 'blackout', 'good', 'bad',
         'number_detected_particles', 'precip_rate', 'precip_amount', 'precip_accumulation', 
         'equivalent_radar_reflectivity', 'number_in_error', 'dirty', 'very_dirty', 'damaged',
         'laserband_amplitude', 'laserband_amplitude_stdev', 'sensor_temperature', 'sensor_temperature_stdev',
         'sensor_voltage', 'sensor_voltage_stdev', 'heating_current', 'heating_current_stdev', 'number_rain_particles',
         'number_non_rain_particles',' number_ambiguous_particles', 'precip_type']

vol_equiv_diam = [0.062, 0.187, 0.312, 0.437, 0.562, 0.687, 0.812, 0.937, 1.062, 1.187, 1.375,
                  1.625, 1.875, 2.125, 2.375, 2.75, 3.25, 3.75, 4.25, 4.75, 5.5, 6.5, 7.5, 8.5,
                  9.5, 11.0, 13.0, 15.0, 17.0, 19.0, 21.5, 24.5]
class_size_width = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125,
                         0.250, 0.250, 0.250, 0.250, 0.250, 0.5, 0.5, 0.5, 0.5, 0.5,
                         1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0]

url = ['https://downloads.psl.noaa.gov/psd2/data/realtime/DisdrometerParsivel/Stats/ctd/2022/002/ctd2200200_stats.txt',
       'https://downloads.psl.noaa.gov/psd2/data/realtime/DisdrometerParsivel/Stats/ctd/2022/002/ctd2200201_stats.txt',
       'https://downloads.psl.noaa.gov/psd2/data/realtime/DisdrometerParsivel/Stats/ctd/2022/002/ctd2200202_stats.txt']

data = []

if isinstance(url, list):
    for u in url:
        df = pd.read_table(u, skiprows=[0,1,2], names=names, index_col=0, sep='\s+')
        date = pd.read_table(u, nrows=0).to_string().split(' ')[-3]
        year = date[0:2]
        jday = date[2:5]
        hour = date[5:7]

        time = df.index
        start_time = []
        end_time = []
        form = '%y%j%H:%M:%S:%f'
        for t in time:
            start_time.append(pd.to_datetime(date + ':' + t.split('-')[0], format=form))
            end_time.append(pd.to_datetime(date + ':' + t.split('-')[1], format=form))
        df.index = start_time
        data.append(df)

    df = pd.concat(data)

dsd = []
for n in names:
    if 'B' not in n:
        continue

    dsd.append(list(df[n]))

obj = df.to_xarray()
obj = obj.rename({'index': 'time'})
long_name = 'Drop Size Distribution'
attrs = {'long_name': long_name, 'units': 'count'}
da = xr.DataArray(np.transpose(dsd), dims=['time', 'particle_size'], coords=[obj['time'].values, vol_equiv_diam])
obj['number_density_drops'] = da

attrs = {'long_name': 'Particle class size average', 'units': 'mm'}
da = xr.DataArray(class_size_width, dims=['particle_size'], coords=[vol_equiv_diam], attrs=attrs)
obj['class_size_width'] = da

attrs = {'long_name': 'Class size width', 'units': 'mm'}
da = xr.DataArray(vol_equiv_diam, dims=['particle_size'], coords=[vol_equiv_diam], attrs=attrs)
obj['particle_size'] = da

attrs = {'blackout': {'long_name': 'Number of samples excluded during PC clock sync', 'units': 'count'},
         'good': {'long_name': 'Number of samples that passed QC checks', 'units': 'count'},
         'bad': {'long_name': 'Number of samples that failed QC checks', 'units': 'count'},
         'number_detected_particles': {'long_name': 'Total number of detected particles', 'units': 'count'},
         'precip_rate': {'long_name': 'Precipitation rate', 'units': 'mm/hr'},
         'precip_amount': {'long_name': 'Interval accumulation', 'units': 'mm'},
         'precip_accumulation': {'long_name': 'Event accumulation', 'units': 'mm'},
         'equivalent_radar_reflectivity': {'long_name': 'Radar Reflectivity', 'units': 'dB'},
         'number_in_error': {'long_name': 'Number of samples that were reported dirt, very dirty, or damaged', 'units': 'count'},
         'dirty': {'long_name': 'Laser glass is dirty but measurement is still possible', 'units': 'unitless'},
         'very_dirty': {'long_name': 'Laser glass is dirty, partially covered no further measurements are possible', 'units': 'unitless'},
         'damaged': {'long_name': 'Laser damaged', 'units': 'unitless'},
         'laserband_amplitude': {'long_name': 'Average signal amplitude of the laser strip', 'units': 'unitless'},
         'laserband_amplitude_stdev': {'long_name': 'Standard deviation of the signal amplitude of the laser strip', 'units': 'unitless'},
         'sensor_temperature': {'long_name': 'Average sensor temperature', 'units': 'degC'},
         'sensor_temperature_stdev': {'long_name': 'Standard deviation of sensor temperature', 'units': 'degC'},
         'sensor_voltage': {'long_name': 'Sensor power supply voltage', 'units': 'V'},
         'sensor_voltage_stdev': {'long_name': 'Standard deviation of the sensor power supply voltage', 'units': 'V'},
         'heating_current': {'long_name': 'Average heating system current', 'units': 'A'},
         'heating_current_stdev': {'long_name': 'Standard deviation of heating system current', 'units': 'A'},
         'number_rain_particles': {'long_name': 'Number of particles detected as rain', 'units': 'unitless'},
         'number_non_rain_particles': {'long_name': 'Number of particles detected not as rain', 'units': 'unitless'},
         'number_ambiguous_particles': {'long_name': 'Number of particles detected as ambiguous', 'units': 'unitless'},
         'precip_type': {'long_name': 'Precipitation type (1=rain; 2=mixed; 3=snow)', 'units': 'unitless'},
         'number_density_drops': {'long_name': 'Drop Size Distribution', 'units': 'count'},
}

for v in obj:
    if v in attrs:
        obj[v].attrs = attrs[v]

display = act.plotting.TimeSeriesDisplay(obj)
display.plot('number_density_drops')
plt.show()
