import act
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


ax = plt.axes(projection=ccrs.PlateCarree())
print(dir(ax))
ax.coastlines()
plt.show()

#obj = act.io.armfiles.read_netcdf(act.tests.sample_files.EXAMPLE_SONDE1)
#geodisplay = act.plotting.GeographicPlotDisplay({'sgpsondewnpnC1.b1': obj})
#geodisplay.geoplot('tdry', marker='.')
obj.close()
