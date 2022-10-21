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

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

ds1 = 'sgpsondewnpnC1.b1'
ds2 = 'sgppblhtsonde1mcfarlC1.c1'
ds3 = 'sgpceil10mC1.b1'
sdate = '2021-0'
edate = sdate
result1 = glob.glob('./'+ds1+'/*'+''.join(sdate.split('-')) + '*')
result2 = glob.glob('./'+ds2+'/*'+''.join(sdate.split('-')) + '*')
result3 = glob.glob('./'+ds3+'/*'+''.join(sdate.split('-')) + '*')
#result1 = act.discovery.download_data(username, token, ds1, sdate, edate)
#result2 = act.discovery.download_data(username, token, ds2, sdate, edate)
#result3 = act.discovery.download_data(username, token, ds3, sdate, edate)
result1 = sorted(result1)
result2 = sorted(result2)
result3 = sorted(result3)

t1 = []
pblht = []
pbl_regime = []

t2 = []
pblht_vap = []
pblht_vap_hefter = []
pblht_vap_R25 = []
pblht_vap_R5 = []
pbl_regime_vap = []
a = {0: 'NRL', 1: 'SBL', 2: 'CBL'}

regime_hit = 0
act_ht = []
vap_ht = []
for i, r in enumerate(result1):
    print(r)
    obj = act.io.armfiles.read_netcdf(r, engine='scipy')
    obj = act.retrievals.sonde.calculate_pbl_liu_liang(obj, smooth_height=1)
    t1.append(obj['time'].values[0])
    pblht.append(obj['pblht_liu_liang'].values)
    pbl_regime.append(obj['pblht_regime_liu_liang'].values)
    #print(obj['pblht_regime_liu_liang'].values, obj['pblht_liu_liang'].values)

    obj2 = act.io.armfiles.read_netcdf(result2[i])
    t2.append(obj2['time'].values[0])
    pblht_vap.append(obj2['pbl_height_liu_liang'].values)
    pblht_vap_hefter.append(obj2['pbl_height_heffter'].values)
    pblht_vap_R25.append(obj2['pbl_height_bulk_richardson_pt25'].values)
    pblht_vap_R5.append(obj2['pbl_height_bulk_richardson_pt5'].values)
    pbl_regime_vap.append(a[int(obj2['pbl_regime_type_liu_liang'].values)])
    #print('VAP:', a[int(obj2['pbl_regime_type_liu_liang'].values)], obj2['pbl_height_liu_liang'].values,
    #      obj2['level_1_liu_liang'].values, obj2['level_2_liu_liang'].values)

    act_ht.append(obj['pblht_liu_liang'].values)
    vap_ht.append(obj2['pbl_height_liu_liang'].values)
    if obj['pblht_regime_liu_liang'].values == a[int(obj2['pbl_regime_type_liu_liang'].values)]:
        regime_hit += 1

    #print(obj2['height_ss'].values[0:30], obj2['wspd_ss'].values[0:30])

print(regime_hit/len(result1))
diff = [i - j for i, j in zip(act_ht, vap_ht)]
print(diff)
print(np.nanmean(diff))
print(np.nanmedian(diff))
fig, ax = plt.subplots()
ax.plot(t1, pblht)
ax.plot(t2, pblht_vap)
plt.show()

#theta = act.utils.data_utils.convert_to_potential_temp(obj=obj, temp_var_name='tdry', press_var_name='pres') + 273.15
#atts = {'units': 'K', 'long_name': 'Potential temperature'}
#da = xr.DataArray(theta, coords=obj['tdry'].coords, dims=obj['tdry'].dims, attrs=atts)
#obj['potential_temperature'] = da
#fig, ax = plt.subplots()
##ax.plot(obj['wspd'].values, obj['pres'].values)
##ax.plot(obj2['wspd'].values, obj2['atm_pres'].values)
##ax.plot(obj2['wspd_ss'].values, obj2['atm_pres_ss'].values)
#ax.plot(obj['potential_temperature'].values, obj['alt'].values, 'k')
#ax.plot(obj['potential_temperature_ss'].values, obj['alt_ss'].values, 'r')
#ax.plot(obj['potential_temperature_ss'].values, obj['alt_ss'].values, 'r+')
#ax.plot(obj2['theta_ss'].values, obj2['height_ss'].values, 'b')
#ax.plot(obj2['theta_ss'].values, obj2['height_ss'].values, 'b+')
#ax.set_ylim([500,650])
#ax.set_xlim([292,302])
#ax.plot([285, 325], [obj['pblht_liu_liang'].values]*2)
#ax.plot([285, 325], [obj2['pbl_height_liu_liang'].values]*2)
#plt.show()


#obj3 = act.io.armfiles.read_netcdf(result3)
#obj3 = obj3.resample(time='1min').mean(keep_attrs=True)
#obj3 = act.corrections.correct_ceil(obj3)
#obj3 = act.corrections.correct_dl(obj3)
#display = act.plotting.TimeSeriesDisplay(obj3, figsize=(15, 10))
#display.plot('backscatter')
#display.axes[0].plot(t2, pblht_vap, 'k*')
#display.axes[0].plot(t2, pblht_vap_hefter, 'k*')
#display.axes[0].plot(t2, pblht_vap_R25, 'k*')
#display.axes[0].plot(t2, pblht_vap_R5, 'k*')
#display.axes[0].plot(t1, pblht, 'r*')
#plt.show()
