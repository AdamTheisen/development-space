import act
import matplotlib.pyplot as plt

result = act.discovery.download_noaa_psl_data(
    site='ctd', instrument='Radar S-band Moment',
    startdate='20211225', hour='06'
)
obj = act.io.noaapsl.read_psl_radar_sband_moment([result[-1]])
display = act.plotting.TimeSeriesDisplay(obj)
display.plot('reflectivity_uncalibrated')
plt.show()
