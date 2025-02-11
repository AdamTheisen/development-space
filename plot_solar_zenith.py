import act
import pandas as pd
import matplotlib.pyplot as plt


time_range = pd.date_range('2024-01-01T00:00:00.000Z', '2024-12-31T23:59:59.000Z', freq='min')

result = act.utils.get_solar_azimuth_elevation(
    latitude=34.3437,
    longitude=-87.3504, 
    time=list(time_range)
)

fig, ax = plt.subplots()
ax.plot(list(time_range), result[0])
plt.show()

