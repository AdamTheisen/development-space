import act
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

files = glob.glob('./data/ANLTWR/*.data')

headers = ['day','month','year','time','pasquill','wdir_60m','wspd_60m',
    'wdir_60m_std','temp_60m','wdir_10m','wspd_10m','wdir_10m_std','temp_10m',
    'temp_dp','rh','avg_temp_diff','total_precip','solar_rad','net_rad',
    'atmos_press','wv_pressure','temp_soil_10cm','temp_soil_100cm','temp_soil_10ft']
obj = act.io.csvfiles.read_csv(files[0],sep='\s+',column_names=headers)

assert 'temp_60m' in obj.variables.keys()

assert obj['temp_60m'].values[10] == -1.7
