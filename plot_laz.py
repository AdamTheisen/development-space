import numpy as np
import glob
import laspy as lp
from scipy.interpolate import griddata 
import matplotlib.pyplot as plt
import tifffile as tiff
import rasterio
import utm
import pyproj

#f = glob.glob('/Users/atheisen/Code/test_codes/SEUS/beam_blockage/*las')[0]
#f = glob.glob('/Users/atheisen/Code/test_codes/SEUS/beam_blockage/*2012*laz')[0]
f = glob.glob('/Users/atheisen/Code/test_codes/SEUS/beam_blockage/USGS_LPC_AL_LawrenceCo_2012_46800_37995_LAS_2018.laz')[0]
site = [-87.350278, 34.343611]
site_xy = utm.from_latlon(site[1], site[0])
data = lp.read(f)

#idx = np.where((data.y < 3800000) & (data.x > 467538))[0]
#idx = np.where((data.x > 467622) & (data.y  > 3800211) & (data.y < 3800450))[0]
#x = np.array(data.x)[idx]
#y = np.array(data.y)[idx]
#z = np.array(data.z)[idx]
#points = np.vstack((x, y, z)).transpose()
points = np.vstack((data.x, data.y, data.z)).transpose()
laz_w = np.nanmin(data.x)
laz_e = np.nanmax(data.x)
laz_s = np.nanmin(data.y)
laz_n = np.nanmax(data.y)

factor = 1
d = points[::factor]

#import open3d as o3d
#pcd = o3d.geometry.PointCloud()
#pcd.points = o3d.utility.Vector3dVector(d)
#o3d.visualization.draw_geometries([pcd])
#sys.exit()

x_lim = [int(min(d[:,0])), int(max(d[:,0]))]
y_lim = [int(min(d[:,1])), int(max(d[:,1]))]

grid_x, grid_y = np.meshgrid(np.linspace(x_lim[0],x_lim[1], 100), np.linspace(y_lim[0], y_lim[1], 100))
grid = griddata(d[:,0:2], d[:,2], (grid_x, grid_y), method='linear')


#plt.contourf(grid_x, grid_y, grid)
#plt.scatter(site_xy[0], site_xy[1], c='r')
#plt.show()
#sys.exit()

#f = glob.glob('/Users/atheisen/Code/test_codes/SEUS/beam_blockage/USGS_NED_OPR_AL_LawrenceCo_2012_46950_37995_TIFF_2018/*tif')
#f = glob.glob('/Users/atheisen/Code/test_codes/SEUS/beam_blockage/USGS_13_n35w088.tif')
f = glob.glob('/Users/atheisen/Code/test_codes/SEUS/beam_blockage/USGS_13_n35w088_20200312.tif')


with rasterio.open(f[0]) as dataset:
    data = dataset.read()
    extent = dataset.bounds
    crs = dataset.crs

bl = utm.from_latlon(extent.bottom, extent.left)
tr = utm.from_latlon(extent.top, extent.right)
extent = [extent.left, extent.right, extent.bottom, extent.top]

#fig, ax = plt.subplots()
#ax = plt.imshow(data[0, :, :], extent=extent)
#plt.scatter(-87.350278, 34.343611, c='r')
#plt.scatter(-87.33830729558571, 34.343992089323095) 
#plt.scatter(-87.34798206270708, 34.34121686121582)
#plt.colorbar(ax)
#plt.show()
w = bl[0]
e = tr[0]
s = bl[1]
n = tr[1]

dem_size = np.shape(data)
dem_x = np.linspace(w,e,dem_size[1])
dem_y = np.linspace(s,n,dem_size[2])

data = data[0, :, :]
#fig, ax = plt.subplots()
#ax.imshow(data, extent=[w, e, s, n])
#ax.contour(dem_x, dem_y, data)
#plt.show()
#sys.exit()

dem_x, dem_y = np.meshgrid(dem_x, dem_y)
dem_x = dem_x.flatten()
dem_y = np.flipud(dem_y).flatten()
data = data.flatten()

#n = 3800450
#w = 467622
#s = 3800211
#e = max(x)

idx = np.where((dem_x > laz_w) & (dem_x < laz_e) & (dem_y < laz_n) & (dem_y > laz_s))[0]

dem_x = dem_x[idx]
dem_y = dem_y[idx]
data = data[idx]

dem_grid = griddata((dem_x, dem_y), data, (grid_x, grid_y), method='nearest')
tree = grid - dem_grid
fig, ax = plt.subplots(1,3, figsize=(15,6))
im = ax[0].imshow(np.flipud(dem_grid), extent=[laz_w, laz_e, laz_s, laz_n], vmin=0)
#im = ax.imshow(dem_grid)
#ax.contourf(grid_x, grid_y, dem_grid, extent=[laz_w, laz_e, laz_s, laz_n])
#ax.contour(grid_x, grid_y, grid, extent=[w, e, s, n])
ax[0].scatter(site_xy[0], site_xy[1], c='r')
ax[0].set_title('DEM Data')
#plt.title('Tree Height (m)')
#cax = plt.axes([0.85, 0.1, 0.075, 0.8])
#plt.colorbar(im, cax=cax)
im = ax[1].imshow(np.flipud(grid), extent=[laz_w, laz_e, laz_s, laz_n], vmin=0)
ax[1].scatter(site_xy[0], site_xy[1], c='r')
ax[1].set_title('Lidar Data')
im = ax[2].imshow(np.flipud(tree), extent=[laz_w, laz_e, laz_s, laz_n], vmin=0)
ax[2].scatter(site_xy[0], site_xy[1], c='r')
ax[2].set_title('Tree Height (Lidar - DEM)')
plt.show()
plt.tight_layout()

#plt.hist(tree.flatten(), range=[0, 40], bins=20)
#plt.show()
