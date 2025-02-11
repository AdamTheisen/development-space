import glob
import act
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# Read in KAZR data, resample to 1-minute, and subtract rough bias in reflectivity
kazr_files = glob.glob('./data/bnfkazr2cfrgeM1.a1/*')
kazr_files.sort()
ds_kazr = act.io.read_arm_netcdf(kazr_files)
ds_kazr = ds_kazr.resample(time='1Min').nearest()
ds_kazr['reflectivity'].values = ds_kazr['reflectivity'].values - 3.

# Read in SMPS data
smps_files = glob.glob('./data/bnfaossmpsM1.b1/*')
smps_files.sort()
ds_smps = act.io.read_arm_netcdf(smps_files)

# Read in SIRS data
sirs_files = glob.glob('./data/bnfsirsM1.b1/*')
sirs_files.sort()
ds_sirs = act.io.read_arm_netcdf(sirs_files)

# Set up ACT plotting object
display = act.plotting.TimeSeriesDisplay({'KAZR': ds_kazr, 'SMPS': ds_smps, 'SIRS': ds_sirs},
                                          figsize=(12,12), subplot_shape=(3,))

# Plot out KAZR reflectivity factor
title = 'Ka-Band ARM Zenith Radar (KAZR) Reflectivity Factor'
cbar_title = 'Reflectivity Factor (dBZ)'
display.plot('reflectivity', dsname='KAZR', subplot_index=(0,), cvd_friendly=True, 
             vmin=-60, vmax=40, set_title=title, cbar_label=cbar_title, ylabel='Height (m)')
display.set_yrng([0, 12000])

# Plot SMPS number size distribution
title = 'Scanning Mobility Particle Sizer (SMPS) Number Size Distribution'
cbar_title = 'dN/dlogD$_p$ (1/cm$^{3}$)'
display.plot('dN_dlogDp', dsname='SMPS', subplot_index=(1,), cvd_friendly=True,
             norm=colors.LogNorm(vmin=100., vmax=10000.), set_title=title, cbar_label=cbar_title,
             ylabel='Pariticle Diameter (nm)')
display.axes[1].set_yscale('log')
display.set_yrng([10, 1000], subplot_index=(1,))

# Plot SIRS Irradiance
title = 'Solar and Infrared Radiation Stations (SIRS) Shortwave Direct Normal Irradiance'
display.plot('short_direct_normal', dsname='SIRS', subplot_index=(2,), set_title=title,
             linestyle='solid', marker=None, ylabel='Irradiance (W/m$^{2}$)')

# Add a day-night background on the SIRS plot
display.day_night_background(subplot_index=(2,), dsname='SIRS')
plt.show()
