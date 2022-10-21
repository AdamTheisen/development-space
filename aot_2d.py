import act
import glob
import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np
import pandas as pd
from scipy.interpolate import griddata,bisplrep, Rbf
import cartopy
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.feature import NaturalEarthFeature


files = glob.glob('./data/AOT/data.csv')
obj = act.io.csvfiles.read_csv(files[0],sep=',')

time = obj['timestamp']
time = pd.to_datetime(time)

obj['timestamp'].values = time
obj = obj.set_index({'index': 'timestamp'})

#test = obj.where(obj['sensor'] == 'tmp122', drop=True)
test = obj.where(obj['parameter'] == 'temperature', drop=True)
test = test.where(test['value_raw'] != '65535', drop=True)

time = test['index']
node_id = test['node_id']
temp = test['value_hrf']

time_thresh = pd.to_datetime('2019-04-16T00:01:00.000000000')

files = glob.glob('./AOT/nodes.csv')
node_meta = act.io.csvfiles.read_csv(files[0],sep=',')

test['lat'] = test['value_hrf'].astype(float).values*0
test['lon'] = test['value_hrf'].astype(float).values*0

lat = []
lon = []
data = []
time = []

for n in set(node_id.values):
    dummy = test.where(test['node_id'] == n,drop=True)
    if np.isnan(float(dummy['value_hrf'].values[100])):
        continue

    a = node_meta.where(node_meta['node_id'] == n,drop=True)
    lat.append(a.lat.values[0])
    lon.append(a.lon.values[0])


    data.append(float(dummy['value_hrf'].values[100]))
    time.append(dummy['index'].values[100])


xs = np.arange(min(lon)-0.02,max(lon)+0.02,0.01)
ys = np.arange(min(lat)-0.02,max(lat)+0.02,0.01)

xi,yi = np.meshgrid(xs,ys)

rbf = Rbf(lon,lat,data,function='thin_plate')
zi = rbf(xi,yi)

title = 'Array of Things Data from 4/16/2019'

projection = ccrs.PlateCarree(central_longitude=np.mean(lon))

fig = plt.figure(figsize=(20,15))
#ax = fig.add_subplot(111,projection=projection)
ax = plt.axes(projection=projection)

#ax.contourf(xi,yi,zi,100,vmin=10,vmax=20,cmap=cm.jet)
ax.contourf(xi,yi,zi,100,cmap=cm.jet,transform=projection)

plt.title=title

plt.plot(lon,lat,'k.')

for i,l in enumerate(lon):
    plt.text(lon[i],lat[i],str(data[i]))

plt.show()

#display = act.plotting.TimeSeriesDisplay(test,figsize=(12,6),subplot_shape=(1,))
#set_title = 'AOT Temperature'
#display.plot('value_hrf',color='b',set_title=set_title, subplot_index=(0,))
#display.axes[0].legend()
#
#plt.tight_layout()
#plt.savefig('./images/aot.png')
