import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import act
import glob

#files = glob.glob('./data/sgpmetE13.b1/*202010*')
files = act.tests.sample_files.EXAMPLE_MET_WILDCARD
ds = act.io.read_arm_netcdf(files)
ds = ds.resample(time='1H').mean()

reference_period = ['2019-01-01', '2019-10-02']

display = act.plotting.TimeSeriesDisplay(ds, figsize=(10, 2))
display.plot_stripes('temp_mean', reference_period=reference_period)
plt.show()
sys.exit()

time = ds['time']
temp = ds['temp_mean']

start = int(mdates.date2num(time.values[0]))
yend = int(mdates.date2num(time.values[-1]))

reference = temp.sel(time=slice(reference_period[0], reference_period[1])).mean('time')
anomaly = temp.values - reference.values

fig, ax = plt.subplots(figsize=(10, 2))


col = PatchCollection([
    Rectangle((y, 0), 1, 1)
    for y in range(start, end + 1)
])

# set data, colormap and color limits

col.set_array(anomaly)
col.set_cmap('seismic')
#col.set_clim(reference - LIM, reference + LIM)
col.set_clim(np.min(anomaly), np.max(anomaly))
ax.add_collection(col)

locator = mdates.AutoDateLocator(minticks=3)
formatter = mdates.AutoDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

ax.set_ylim(0, 1)
ax.set_yticks([])
ax.set_xlim(start, end + 1)
ax.set_title('Climate Stripes')

plt.show()
