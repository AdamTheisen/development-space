import act
import radtraq
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.io.img_tiles import Stamen
import numpy as np


d = {
     #'Cullman': {'lat': 34.26274649951493, 'lon': -86.85874523934974},
     #'Courtland': {'lat': 34.658302981847655, 'lon': -87.34389529761859},
     'ARMOR': {'lat': 34.6461459004804, 'lon': -86.77145475793658},
     'Field': {'lat': 34.631230059709516, 'lon': -87.13441618858165},
#         'Pugh Field': {'lat': 34.45388818906293, 'lon': -87.71028434099281}}
}

# SGP
d = {
    'I4': {'lat': 36.578650, 'lon': -97.363834},
    'I5': {'lat': 36.491178, 'lon': -97.593936},
    'I6': {'lat': 36.767569, 'lon': -97.547446},
}

data = radtraq.utils.calculate_dual_dop_lobes(d)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for l in data:
    ax.plot(data[l]['lon'], data[l]['lat'], 'k', linestyle='solid')
for s in d:
    ax.plot(d[s]['lon'], d[s]['lat'], 'k*', ms=14)
    plt.text(d[s]['lon'], d[s]['lat'], s)

#result = [act.utils.destination_azimuth_distance(d['Field']['lat'], d['Field']['lon'], i, 100, dist_units='km') for i in range(0, 360)]

#print(result[0])
#ax.plot(result[:, 1], result[:, 0])
plt.show()

