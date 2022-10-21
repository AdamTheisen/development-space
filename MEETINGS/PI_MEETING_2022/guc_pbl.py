import glob
import act
import matplotlib.pyplot as plt


files = glob.glob('./gucsondewnpnM1.b1/*2022090*')
files.sort()
time = []
act_ht = []
vap_ht = []
br25_ht = []
br5_ht = []

vap_files = glob.glob('./gucpblhtsonde1mcfarlM1.c1/*2022090*')
vap_files.sort()
for i, f in enumerate(files):
    obj = act.io.armfiles.read_netcdf(f)
    obj = act.retrievals.sonde.calculate_pbl_liu_liang(obj, smooth_height=3, llj_max_alt=4000)

    time.append(obj['time'].values[0])
    act_ht.append(obj['pblht_liu_liang'].values)

    obj2 = act.io.armfiles.read_netcdf(vap_files[i])
    vap_ht.append(obj2['pbl_height_liu_liang'].values)
    br25_ht.append(obj2['pbl_height_bulk_richardson_pt25'].values)
    br5_ht.append(obj2['pbl_height_bulk_richardson_pt5'].values)


    obj.close()
    obj2.close()

#fig, ax = plt.subplots()
#ax.plot(time, act_ht, '.', linestyle='-')
#ax.plot(time, vap_ht, '.', linestyle='-')
#plt.show()

files = glob.glob('./gucceil10mM1.b1/*2022090*')
files.sort()
obj3 = act.io.armfiles.read_netcdf(files)

ceil_range = obj3['range'].values + obj3['alt'].values[0]
obj3 = obj3.assign_coords({'range': ceil_range})
obj3 = act.corrections.correct_ceil(obj3)


#files = glob.glob('./gucceilpblhtM1.a0/*2022090*')
#files.sort()
#obj4 = act.io.armfiles.read_netcdf(files)

#display = act.plotting.TimeSeriesDisplay({'ceil': obj3, 'ceilpbl': obj4}, figsize=(10, 8))
display = act.plotting.TimeSeriesDisplay(obj3, figsize=(10, 8))
display.plot('backscatter')
display.axes[0].plot(time, act_ht, 'k*', markersize=20, label='ACT')
display.axes[0].plot(time, vap_ht, 'm*', markersize=20, label='VAP')
#display.axes[0].plot(time, br25_ht, 'r*', markersize=10, label='VAP')
#display.axes[0].plot(time, br5_ht, 'ro', markersize=10, label='VAP')
plt.show()
