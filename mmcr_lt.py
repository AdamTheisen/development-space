import matplotlib
matplotlib.use('Agg')

import datetime as dt
import act
import glob
import matplotlib.pyplot as plt
import netCDF4
import numpy as np

#Specify datastream and date range for MET data
datastream = 'sgpmmcrC1.b1'

#Download MET Data
#files = glob.glob('/Volumes/Thunder/MMCR/*cdf')
files = glob.glob('./sgpmmcrmomC1.b1/*cdf')
files.sort()

#Read in MET data to Standard Object
#obj = act.io.armfiles.read_netcdf(files[0],decode_coords=False)

vavg=[]
vmin=[]
vmax=[]
egate = []
time = []

ct=1
for f in files:
    print(ct,':',len(files),'  ',f)
    try:
        nc = netCDF4.MFDataset(f)
    except:
        ct+=1
        continue
    zh = nc.variables['Reflectivity'][:]
    mode = nc.variables['ModeNum'][:]
    idx = np.where((mode == 3))[0]
    vavg.append(np.nanmean(zh[idx,:]))
    vmin.append(np.nanmin(zh[idx,:]))
    vmax.append(np.nanmax(zh[idx,:]))

    egate.append(zh[idx[0],-1])
    time.append(dt.datetime.utcfromtimestamp(nc.variables['base_time'][0].data.tolist()))
    nc.close()
    ct+=1

#Plot out background and MET LCL Overlay
fig, ax = plt.subplots(4,figsize=(18,10))
ax[0].plot(time,vmin)
ax[0].set(xlabel='Time (UTC)',title=''.join([datastream,' Minimum Zh']))
ax[1].plot(time,vmax)
ax[1].set(xlabel='Time (UTC)',title=''.join([datastream,' Maximum Zh']))
ax[2].plot(time,vmax)
ax[2].set(xlabel='Time (UTC)',title=''.join([datastream,' Average Zh']))

ax[3].plot(time,egate)
ax[3].set(xlabel='Time (UTC)',title=''.join([datastream,' Last Gate Zh']))

plt.tight_layout()
fig.savefig('./images/mmcr_timeline.png')
