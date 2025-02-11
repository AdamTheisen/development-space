import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.img_tiles import Stamen
import matplotlib.pyplot as plt

# Set projection and lat/lon extent
projection = ccrs.PlateCarree()
ax = plt.axes(projection=projection)
plt.subplots_adjust(left=0.01, right=0.99, bottom=0.05, top=0.93)
ax.set_extent([-65.38219661712647, -63.99097232818603, -33.219947052001956, -31.828722763061524], crs=projection)

# Set up tiles
tiler = Stamen('terrain')
ax.add_image(tiler, 8)

plt.show()
