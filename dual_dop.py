import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.io.img_tiles import Stamen


fac=['Cullman','Courtland', 'Bill Pugh Field']
lat=[34.26274649951493, 34.658302981847655, 34.453899]
lon=[-86.85874523934974, -87.34389529761859, -87.710284]
#fac=['Bill Pugh Field','Courtland']
#lat=[34.453899, 34.658302981847655]
#lon=[-87.710284, -87.34389529761859]

fac=['Courtland','UAH ARMOR']
lat=[34.658302981847655, 34.6461459004804]
lon=[-87.34389529761859, -86.77145475793658]

fac=['CSAPR','Courtland']
lat=[34.631230059709516, 34.658302981847655]
lon=[-87.13441618858165, -87.34389529761859]


main_site = [34.337843810067426, -87.33666190651223]

theta = 20.
theta_r = np.radians(theta)

if lon[1] > lon[0]:
    dy = lat[1] - lat[0]
    dx = lon[1] - lon[0]
else:
    dy = lat[0] - lat[1]
    dx = lon[0] - lon[1]

phi = np.arctan(dy / dx)

realX_midpoint = (lon[0] + lon[1]) / 2.
realY_midpoint = (lat[0] + lat[1]) / 2.

midpoint = np.sqrt((lon[1] - lon[0]) ** 2. + (lat[1] - lat[0]) ** 2.) / 2.

h = midpoint / np.tanh(theta_r / 2.)
h2 = midpoint * np.tanh(theta_r / 2.)
radius = (h + h2) / 2.

ycenter = radius - h2
ycenter2 = -1. * radius + h2

trueCenterX = -1 * ycenter * np.sin(phi)
trueCenterY = ycenter * np.cos(phi)

trueCenterX2 = ycenter * np.sin(phi)
trueCenterY2 = ycenter2 * np.cos(phi)

trueCenterX = trueCenterX + realX_midpoint
trueCenterY = trueCenterY + realY_midpoint

trueCenterX2 = trueCenterX2 + realX_midpoint
trueCenterY2 = trueCenterY2 + realY_midpoint

t = np.arange(-3.5, 3.5, 0.1)

x1vals = trueCenterX + radius * np.cos(t)
y1vals = trueCenterY + radius * np.sin(t)
x2vals = trueCenterX2 + radius * np.cos(t)
y2vals = trueCenterY2 + radius * np.sin(t)
mp1 = [trueCenterX, trueCenterY]
mp2 = [trueCenterX2, trueCenterY2]

midpoint = [mp1, mp2]

tiler = Stamen('terrain-background')
mercator = tiler.crs

minx = np.min([x1vals, x2vals])
miny = np.min([y1vals, y2vals])
maxx = np.max([x1vals, x2vals])
maxy = np.max([y1vals, y2vals])

delta = np.max([maxx - minx, maxy-miny]) / 2.

#extent = [np.min([x1vals, x2vals]), np.max([x1vals, x2vals]), np.min([y1vals, y2vals]), np.max([y1vals, y2vals])]
extent = [realX_midpoint - delta, realX_midpoint + delta, realY_midpoint - delta, realY_midpoint + delta]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=mercator)
ax.set_extent(extent, crs=ccrs.PlateCarree())
ax.add_image(tiler, 8)
ax.coastlines('10m')
ax.plot(x1vals, y1vals, 'k.', transform=ccrs.PlateCarree())
ax.plot(x2vals, y2vals, 'r.', transform=ccrs.PlateCarree())
ax.plot(lon[0], lat[0], 'k*', ms=14, transform=ccrs.PlateCarree())
ax.plot(lon[1], lat[1], 'r*', ms=14, transform=ccrs.PlateCarree())
plt.text(lon[0], lat[0], fac[0], transform=ccrs.PlateCarree())
plt.text(lon[1], lat[1], fac[1], transform=ccrs.PlateCarree())

ax.plot(main_site[1], main_site[0], 'r*', ms=14, transform=ccrs.PlateCarree())
plt.text(main_site[1], main_site[0], 'BWWC', transform=ccrs.PlateCarree())
plt.show()
