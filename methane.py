import glob
import act
import matplotlib.pyplot as plt
import datetime as dt
import xarray as xr
import matplotlib.dates as mdates
myFmt = mdates.DateFormatter('%m/%Y')


files = glob.glob('./data/nsaamcmethaneC1.c1/ARM-barrow-b1*ARM*txt')
files.sort()

ds_all=[]
for f in files:
    print(f)
    ds = act.io.read_csv(f, index_col=1)
    ds = ds.rename({'time_stamp': 'time'})
    ds['time'].attrs['units'] = 'UTC'
    time = ds['time'].values
    dates = []
    for t in time:
        dates.append(dt.datetime(int(str(t)[0:4]), 1, 1) + dt.timedelta(days=int(str(t)[4:7]), hours=int(str(t)[7:9]), minutes=int(str(t)[9:11])))

    ds = ds.assign_coords(time=dates)
    ds = ds.where(ds['ch4_flux'] != -9999, drop=True)
    ds = ds.where(ds['qc_ch4_flux'] == 0, drop=True)

    ds_all.append(ds)

ds = xr.merge(ds_all)

print(ds.time.size)

print('Reading netcdf files')
files = glob.glob('./data/nsaamcmethaneC1.c1/*nc')
files.sort()
ds_nc = act.io.read_arm_netcdf(files)
ds_nc = ds_nc.where(ds_nc['qc_ch4_flux'].compute() == 0, drop=True)
print(ds_nc['ch4_flux'].size)


display = act.plotting.TimeSeriesDisplay({'new': ds, 'old': ds_nc})
display.plot('ch4_flux', linestyle='', dsname='new')
display.plot('ch4_flux', linestyle='', dsname='old')
display.set_yrng([-200, 200])
display.set_xrng([ds_nc['time'].values[0], ds['time'].values[-1]])
display.axes[0].xaxis.set_major_formatter(myFmt)

plt.show()
