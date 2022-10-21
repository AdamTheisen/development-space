import matplotlib
#matplotlib.use('Agg')

import act
import glob
import matplotlib.pyplot as plt
from matplotlib import cm

import json
import xarray as xr
import numpy as np
from scipy.interpolate import griddata,bisplrep, Rbf
import pyart
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

startdate = '2019-05-08'
enddate = '2019-05-08'
time = '2019-05-08T04:00:00.000000000'
date = '20190508'

#Specify datastream and date range for MET data
facs = ['E9','E13','E15','E31','E32','E33','E34','E35','E36',
       'E37','E38','E39','E40']
base = 'sgpmet'

test={}
temp = []
rh = []
pres=[]
wspd = []
wdir = []
lat = []
lon = []
for fac in facs:
    datastream=base+fac+'.b1'
    files = glob.glob(''.join(['./',datastream,'/*',date,'*cdf']))
    if len(files) == 0:
        act.discovery.download_data(username, token, datastream, startdate, enddate)
        files = glob.glob(''.join(['./',datastream,'/*',date,'*cdf']))

    obj = act.io.armfiles.read_netcdf(files)
    temp.append(obj['temp_mean'].sel(time=time).values.tolist())
    rh.append(obj['rh_mean'].sel(time=time).values.tolist())
    pres.append(obj['atmos_pressure'].sel(time=time).values.tolist())
    wspd.append(obj['wspd_vec_mean'].sel(time=time).values.tolist())
    wdir.append(obj['wdir_vec_mean'].sel(time=time).values.tolist())
 
    lat.append(obj['lat'].sel(time=time).values.tolist())
    lon.append(obj['lon'].sel(time=time).values.tolist())

temp = np.array(temp)
rh = np.array(rh)
pres = np.array(pres)
wspd = np.array(wspd)
wdir = np.array(wdir)
lat = np.array(lat)
lon = np.array(lon)

# Setting projection and ploting the second tilt
projection = ccrs.PlateCarree(central_longitude=-97.485)
#projection = ccrs.Mercator(central_longitude=-97.485,min_latitude=yi.min(),max_latitude=yi.max())


xs = np.arange(min(lon)-0.1,max(lon)+0.1,0.01)
ys = np.arange(min(lat)-0.1,max(lat)+0.1,0.01)

xi,yi = np.meshgrid(xs,ys)

rbf = Rbf(lon,lat,temp,function='cubic')
zi = rbf(xi,yi)

#Radar Plotting
rfile = './sgpxsaprppiI4.00/XSE190508040007.RAW5CWS'
radar =pyart.io.read(rfile)

gatefilter = pyart.correct.GateFilter(radar)
gatefilter.exclude_below('reflectivity', 10)
gatefilter.exclude_below('normalized_coherent_power', 0.45)

display = pyart.graph.RadarMapDisplay(radar)

fig = plt.figure(figsize=(20,15))
ax = fig.add_subplot(111)#,projection=projection)

title='SGP I4 XSAPR Reflectivity Overlaid \n on MET Surface Data'
display.plot_ppi_map('reflectivity', 1, vmin=-20, vmax=60,
                     min_lon=min(xs), max_lon=max(xs), min_lat=min(ys), max_lat=max(ys),
                     resolution='10m',gatefilter=gatefilter,
                     projection=projection,fig=fig,ax=ax,lat_0=36.605,
                     lon_0=-97.485,title=title)

xi = xi + 97.485
tlon = lon + 97.485
display.ax.contourf(xi,yi,zi,100,transform=projection,zorder=0,vmin=10,vmax=30,cmap=cm.jet)

display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0],label_text='I4')
rad = 4.0*np.arctan(1.0)/180.
for i, txt in enumerate(facs):
    display.plot_point(lon[i], lat[i],'.k', label_text=txt)
    display.plot_point(lon[i], lat[i],'.k', label_text=round(rh[i]),label_offset=(-0.055,-0.025))
    display.plot_point(lon[i], lat[i],'.k', label_text=round(pres[i],1),label_offset=(-0.055,0.01))
    u = 0-wspd[i]*np.sin(rad*wdir[i])
    v = 0-wspd[i]*np.cos(rad*wdir[i])
    display.ax.barbs(tlon[i], lat[i], u,v)


plt.tight_layout()
plt.savefig('./act_pyart.png',dpi=1000)

