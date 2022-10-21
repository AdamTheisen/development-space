import matplotlib
matplotlib.use('Agg')

import act.io.armfiles as arm
import act.plotting.plot as armplot
import act.discovery.get_files as get_data

import glob
import matplotlib.pyplot as plt
import os
import numpy as np
import json

with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Set up initial data request
datastream = 'sgpxsaprcfrvptI5.a1'
startdate = '2019-01-11'
enddate = '2019-01-11'

#Use ADC example script to get the data
files = glob.glob(''.join(['./',datastream,'/*',''.join(startdate.split('-')),'*']))
if len(files) == 0:
    get_data.download_data(username, token, datastream, startdate, enddate)
    files = glob.glob(''.join(['./',datastream,'/*',''.join(startdate.split('-')),'*']))

#Process MET data to get simple LCL
files.sort()
sapr = arm.read_netcdf(files)

zh = sapr.reflectivity.values
dr = sapr.differential_reflectivity.values
rh = sapr.cross_correlation_ratio_hv.values
height = sapr.range.values/1000.

idx = (zh < 20.) | (zh > 45.)
ix,iy = np.where(idx)
zh[ix,iy] = np.nan
dr[ix,iy] = np.nan
rh[ix,iy] = np.nan

idx = (rh < 0.98)
ix,iy = np.where(idx)
zh[ix,iy] = np.nan
dr[ix,iy] = np.nan
rh[ix,iy] = np.nan

idx = (height < 1.) | (height > 10.)
iy = np.where(idx)
zh[:,iy] = np.nan
dr[:,iy] = np.nan
rh[:,iy] = np.nan

fig, ax = plt.subplots(1,3,figsize=(12,5))
plt.subplots_adjust(top=0.9, bottom=0.2, left=0.05, right=0.95, hspace=0.3,wspace=0.35)

ax[0].plot(np.nanmean(zh,axis=0),height)
ax[0].set_xlim(20,45)
ax[0].set_title(' '.join([datastream,'\nAverage Zh Profile on',startdate]))
ax[0].set_xlabel('Zh (dBZ)')
ax[0].set_ylabel('Height (km)')
ax[0].text(0.0,-0.1,'Zh='+str(round(np.nanmean(zh),2)), color='red',transform=ax[0].transAxes,
    horizontalalignment='left')

ax[1].plot(np.nanmean(dr,axis=0),height)
ax[1].set_xlim(-6,4)
ax[1].set_title(' '.join([datastream,'\nAverage Zdr Profile on',startdate]))
ax[1].set_xlabel('Zdr (dB)')
ax[1].set_ylabel('Height (km)')
ax[1].text(0.0,-0.1,'Zdr='+str(round(np.nanmean(dr),2)), color='red',transform=ax[1].transAxes,
    horizontalalignment='left')

ax[2].plot(np.nanmean(rh,axis=0),height)
ax[2].set_xlim(0.98,1)
ax[2].set_title(' '.join([datastream,'\nAverage RhoHV Profile on',startdate]))
ax[2].set_xlabel('RhoHV ()')
ax[2].set_ylabel('Height (km)')
ax[2].text(0.0,-0.1,'RhoHV='+str(round(np.nanmean(rh),2)), color='red',transform=ax[2].transAxes,
    horizontalalignment='left')

fig.savefig('./zdr'+startdate+'.png')
print(np.nanmean(dr),np.nanmean(zh),np.nanmean(rh))
