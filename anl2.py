import pandas as pd
import datetime as dt
import pytz
import matplotlib.pyplot as plt

url = 'https://www.atmos.anl.gov/ANLMET/anltower.not_qc'
df = pd.read_csv(url, header=1, skipfooter=1, delimiter='\s+')
obj = df.to_xarray()

# Work magic on time
cyear = dt.datetime.now().year
jday = obj['JDA'].values
time = obj['T_LST'].values
time = [dt.datetime.strptime(''.join([str(cyear), str(jday[i]), ' ', time[i]]), '%Y%j %H:%M') for i in range(len(jday))]
local = pytz.timezone("America/Chicago")
time = [local.localize(t, is_dst=None).astimezone(pytz.utc) for t in time]

# Set up time to be the coordinate
obj['time'] = (['index'], time)
obj = obj.reset_index(['index'], drop=True)
obj = obj.assign_coords({'time': time})

# Plot out the data
obj['radW/m2'].plot()
plt.show()
