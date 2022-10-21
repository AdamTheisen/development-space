import act
import json
import glob
import matplotlib.pyplot as plt
import datetime as dt

ds = 'mossrgM1.b1'
files = glob.glob(''.join(['./data/',ds,'/*nc']))
files.sort()

# Read in KAZR data to Standard Object
files = files[0:2]
print(files)
obj = act.io.armfiles.read_netcdf(files)

date = '20191122'
days = 7
xrng = [(dt.datetime.strptime(date,'%Y%m%d') -
    dt.timedelta(days=days)),
    (dt.datetime.strptime(date,'%Y%m%d') +
    dt.timedelta(days=1))]


display = act.plotting.TimeSeriesDisplay(obj)
display.plot('battery_voltage_min', time_rng=xrng)
#display.axes[0].set_xlim(xrng)

plt.show()

obj.close()
