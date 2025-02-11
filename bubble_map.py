import cartopy.crs as crs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd

#df = pd.read_csv('./mentor_counts.csv')
df = pd.read_csv('./mentor_locations.csv')

fig = plt.figure(figsize=(16,10))

ax = fig.add_subplot(1,1,1, projection=crs.PlateCarree())
ax.stock_img()
ax.coastlines()
ax.add_feature(cfeature.STATES)

ax.set_extent([-170, -66.5, 20, 80],
              crs=crs.PlateCarree()) ## Important

colors = ['orange', 'orange', 'orange', 'blue', 'orange', 'purple', 'orange',
          'orange', 'orange', 'orange', 'orange', 'blue']
print(df)
plt.scatter(x=df.Lon, y=df.Lat,
            color=colors,
            #s=df.Instruments*10,
            s=df.Mentors*100,
            alpha=0.8,
            transform=crs.PlateCarree()) ## Important
plt.plot(df.Lon, df.Lat, 'k+')
x_ct = [-1.5, 0.25, -3.5, 1, 0.5, 1, 0.25, 0.25, 0.25, 0.25, -0.25, -0.75]
y_ct = [-1.5, -1.5, -0.5, 0.75, 0.25, -1.25, 0.25,0.25, 0.25, 0.25, 0.25, 1]

for i in range(len(df.Mentors)):
    print(df.Name[i], df.Lon[i],x_ct[i])
    plt.text(df.Lon[i] + x_ct[i], df.Lat[i] + y_ct[i], df.Name[i])

plt.show()
