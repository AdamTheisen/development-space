import act
import matplotlib.pyplot as plt


# Use arm username and token to retrieve files.
token = 'arm_token'
username = 'arm_username'

#Specify datastream and date range for KAZR data
ds_kazr = 'guckazrcfrgeM1.a1'
startdate = '2022-08-01'
enddate = '2022-08-01'

# Download and read in the ARM KAZR data
act.discovery.download_data(username, token, ds_kazr, startdate, enddate)
kazr_files = glob.glob(''.join(['./',ds_kazr,'/*nc']))
kazr = act.io.armfiles.read_netcdf(kazr_files[-2:])

# Download and read in the corresponding doppler lidar data
ds_dl = 'gucdlppiM1.b1'
act.discovery.download_data(username, token, ds_dl, startdate, enddate)
dl_ppi_files = glob.glob(''.join(['./',ds_dl,'/*cdf']))
dl_ppi = act.io.armfiles.read_netcdf(dl_ppi_files[-9:])

# Calculate the winds from the gucdlppi dataset.
wind_obj = act.retrievals.compute_winds_from_ppi(dl_ppi, remove_all_missing=True, snr_threshold=0.002)

# Create a display object and plot out the KAZR reflectivity with Wind Bards Overlaid
display = act.plotting.TimeSeriesDisplay({"GUC DLPPI Computed Winds over KAZR": wind_obj,
                                          "guckazrcfrgeM1.a1": kazr,}, figsize=(20, 10))
display.plot('reflectivity', dsname='guckazrcfrgeM1.a1', cmap='act_HomeyerRainbow', vmin=-20, vmax=30)
display.plot_barbs_from_spd_dir('wind_speed', 'wind_direction', dsname='GUC DLPPI Computed Winds over KAZR',
                                invert_y_axis=False)
plt.show()

