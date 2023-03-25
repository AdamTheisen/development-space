import act

import glob
import xarray as xr
import pandas as pd
from datetime import datetime, timedelta
from datetime import datetime
import numpy as np
from netCDF4 import Dataset
import os
import matplotlib.pyplot as plt
from scipy import ndimage


def convert_to_hours_minutes_seconds(decimal_hour, initial_time):
    delta = timedelta(hours=decimal_hour)
    return datetime(initial_time.year, initial_time.month, initial_time.day) + delta

def read_as_netcdf(file):
    field_dict = hpl2dict(file)
    initial_time = pd.to_datetime(field_dict['start_time'])

    time = pd.to_datetime([convert_to_hours_minutes_seconds(x, initial_time) for x in field_dict['decimal_time']])

    ds = xr.Dataset(coords={'time': time,
                            'range':field_dict['center_of_gates'],
                            'azimuth': ('time', field_dict['azimuth'])},
                    data_vars={'radial_velocity':(['time', 'range'],
                                                  field_dict['radial_velocity']),
                               'beta': (('time', 'range'), 
                                        field_dict['beta']),
                               'intensity': (('time', 'range'),
                                             field_dict['intensity'])
                              }
                   )
    return ds

def convert_to_preferred_format(secs):
   secs = secs % (24 * 3600)
   hour = secs // 3600
   secs %= 3600
   mins = secs // 60
   secs %= 60
   #print("seconds value in hours:",hour)
   #print("seconds value in minutes:",mins)
   return "%02d:%02d:%02d" %(hour, mins, secs)


def hpl2dict(file_path):
    #import hpl files into intercal storage
    with open(file_path, 'r') as text_file:
        lines=text_file.readlines()

    #write lines into Dictionary
    data_temp=dict()

    header_n=17 #length of header
    data_temp['filename']=lines[0].split()[-1]
    data_temp['system_id']=int(lines[1].split()[-1])
    data_temp['number_of_gates']=int(lines[2].split()[-1])
    data_temp['range_gate_length_m']=float(lines[3].split()[-1])
    data_temp['gate_length_pts']=int(lines[4].split()[-1])
    data_temp['pulses_per_ray']=int(lines[5].split()[-1])
    data_temp['number_of_waypoints_in_file']=int(lines[6].split()[-1])
    rays_n=(len(lines)-header_n)/(data_temp['number_of_gates']+1)

    '''
    number of lines does not match expected format if the number of range gates 
    was changed in the measuring period of the data file (especially possible for stare data)
    '''
    if not rays_n.is_integer():
        print('Number of lines does not match expected format')
        return np.nan

    data_temp['no_of_rays_in_file']=int(rays_n)
    data_temp['scan_type']=' '.join(lines[7].split()[2:])
    data_temp['focus_range']=lines[8].split()[-1]
    data_temp['start_time']=pd.to_datetime(' '.join(lines[9].split()[-2:]))
    data_temp['resolution']=('%s %s' % (lines[10].split()[-1],'m s-1'))
    data_temp['range_gates']=np.arange(0,data_temp['number_of_gates'])
    data_temp['center_of_gates']=(data_temp['range_gates']+0.5)*data_temp['range_gate_length_m']

    #dimensions of data set
    gates_n=data_temp['number_of_gates']
    rays_n=data_temp['no_of_rays_in_file']

    # item of measurement variables are predefined as symetric numpy arrays filled with NaN values
    data_temp['radial_velocity'] = np.full([rays_n, gates_n],np.nan) #m s-1
    data_temp['intensity'] = np.full([rays_n, gates_n],np.nan) #SNR+1
    data_temp['beta'] = np.full([rays_n, gates_n],np.nan) #m-1 sr-1
    data_temp['spectral_width'] = np.full([rays_n, gates_n],np.nan)
    data_temp['elevation'] = np.full(rays_n,np.nan) #degrees
    data_temp['azimuth'] = np.full(rays_n,np.nan) #degrees
    data_temp['decimal_time'] = np.full(rays_n,np.nan) #hours
    data_temp['pitch'] = np.full(rays_n,np.nan) #degrees
    data_temp['roll'] = np.full(rays_n,np.nan) #degrees

    for ri in range(0,rays_n): #loop rays
        lines_temp = lines[header_n+(ri*gates_n)+ri+1:header_n+(ri*gates_n)+gates_n+ri+1]
        header_temp = np.asarray(lines[header_n+(ri*gates_n)+ri].split(),dtype=float)
        data_temp['decimal_time'][ri] = header_temp[0]
        data_temp['azimuth'][ri] = header_temp[1]
        data_temp['elevation'][ri] = header_temp[2]
        data_temp['pitch'][ri] = header_temp[3]
        data_temp['roll'][ri] = header_temp[4]
        for gi in range(0,gates_n): #loop range gates
            line_temp=np.asarray(lines_temp[gi].split(),dtype=float)
            data_temp['radial_velocity'][ri, gi] = line_temp[1]
            data_temp['intensity'][ri, gi] = line_temp[2]
            data_temp['beta'][ri, gi] = line_temp[3]
            if line_temp.size>4:
                data_temp['spectral_width'][ri, gi] = line_temp[4]

    return data_temp


files = sorted(glob.glob('./*hpl'))
datasets = [read_as_netcdf(file) for file in files]

ds = xr.concat(datasets, dim='time')

ds = ds[['time', 'range', 'intensity', 'beta']]

ds['beta'].attrs['units'] = 'unknown'
ds['intensity'].attrs['units'] = 'unknown'
ds['range'].attrs['units'] = 'm'
ds = act.corrections.correct_dl(ds, var_name='beta')
ds = act.retrievals.generic_sobel_cbh(ds, variable='beta', height_dim='range', var_thresh=-5.5)

display = act.plotting.TimeSeriesDisplay(ds)
display.plot('intensity')
display.plot('cbh_sobel', color='k', linestyle='-', marker=None)
plt.show()
