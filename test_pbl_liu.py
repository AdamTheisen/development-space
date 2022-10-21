import matplotlib
import act
import glob
import matplotlib.pyplot as plt
import json
import xarray as xr
import sys
import datetime as dt
import pandas as pd
import numpy as np

files = glob.glob(act.tests.sample_files.EXAMPLE_TWP_SONDE_20060121)
files2 = glob.glob(act.tests.sample_files.EXAMPLE_SONDE1)
files += files2

pblht = []
pbl_regime = []
for i, r in enumerate(files):
    obj = act.io.armfiles.read_netcdf(r)
    obj['tdry'].attrs['units'] = 'degree_Celsius'
    obj = act.retrievals.sonde.calculate_pbl_liu_liang(obj, smooth_height=10)
    pblht.append(float(obj['pblht_liu_liang'].values))
    pbl_regime.append(obj['pblht_regime_liu_liang'].values)
    print(obj['pblht_regime_liu_liang'].values, obj['pblht_liu_liang'].values)

assert pbl_regime == ['NRL', 'NRL', 'NRL', 'NRL', 'NRL']
np.testing.assert_array_almost_equal(pblht, [197.7, 184.8, 858.2, 443.2, 847.5], decimal=1)
