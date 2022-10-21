import act
import glob
import matplotlib.pyplot as plt

files = glob.glob('./sgptbsimetC1.b1/*')[-1]

obj = act.io.armfiles.read_netcdf(files)

display = act.plotting.TimeSeriesDisplay(obj, figsize=(15, 10))
display.time_height_scatter(data_field='air_temperature', alt_field='imet_altitude')
plt.show()

