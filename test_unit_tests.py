import act
import glob
import matplotlib.pyplot as plt
import numpy as np

sonde_ds = act.io.armfiles.read_netcdf(
    act.tests.sample_files.EXAMPLE_TWP_SONDE_WILDCARD)

WindDisplay = act.plotting.WindRoseDisplay(sonde_ds, figsize=(10, 10))
WindDisplay.plot('deg', 'wspd',
                 spd_bins=np.linspace(0, 20, 10), num_dirs=30,
                 tick_interval=2, cmap='viridis')

plt.tight_layout()
plt.show()
