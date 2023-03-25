import act
import glob
import matplotlib.pyplot as plt
import numpy as np

# Get files
files = ['./sgpsondewnpnC1.b1/sgpsondewnpnC1.b1.20190521.202900.cdf']

# Read files into Xarray Dataset
obj = act.io.armfiles.read_netcdf(files)

# Calculate stability information using MetPy
obj = act.retrievals.calculate_stability_indicies(
    obj, temp_name='tdry', td_name='dp', p_name='pres', rh_name='rh'
)

# Create Skew-T Display Object
mos = [['A', 'B'], ['A', 'C']]
skewt = act.plotting.SkewTDisplay(obj, figsize=(10, 10))
skewt.plot_from_u_and_v('u_wind', 'v_wind', 'pres', 'tdry', 'dp', set_title='Your Title')
#skewt.plot_from_spd_and_dir('wspd', 'deg', 'pres', 'tdry', 'dp', set_title='Your Title')

print(list(obj))
# Add room at bottom of the plot
skewt.fig.subplots_adjust(bottom=0.2, top=0.95)

# Set the variables to add to the plot
# Note: Dictionary key is the name to display and value is
# the variable name in the object
variables_to_add = {
    'CAPE': 'surface_based_cape',
    'CIN': 'surface_based_cin',
    'LCL (Pressure)': 'lifted_condensation_level_pressure',
    'LFC': 'level_of_free_convection'
}

# For each variable, add value to the plot
ct = 0
ctx = 0
for v in variables_to_add:
    xcoord = 0.15 + ctx * 0.2
    plt.text(xcoord, 0.14 - ct * 0.025, v + ': ' + str(np.round(obj[variables_to_add[v]].values, 2)),
             transform=plt.gcf().transFigure)
    ct += 1
    if ct == 2:
        ct = 0
        ctx += 1

# Show plot
plt.show()
