import act
import glob
import matplotlib.pyplot as plt

#Specify datastream and date range for KAZR data
site = 'sgp'
kazr_ds = site+'kazrgeC1.a1'
sdate = '20190817'
files = glob.glob(''.join(['./',kazr_ds,'/*'+sdate+'*cdf']))

#Read in KAZR data to Standard Object
kazr = act.io.armfiles.read_netcdf(files)
kazr = kazr.resample(time='1min').nearest()
kazr = act.retrievals.cbh.generic_sobel_cbh(kazr,variable='reflectivity_copol',
                                            height_dim='range', var_thresh=-10.)

#Display data using plotting methods
display = act.plotting.TimeSeriesDisplay(kazr,figsize=(15,10))
display.plot('reflectivity_copol', cmap='jet')
display.plot('cbh_sobel',color='k')
plt.savefig('./images/dev_cbh_ex.png')
plt.clf()
