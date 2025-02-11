import act
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
import glob
import os
from act.plotting import TimeSeriesDisplay, WindRoseDisplay
from act.tests import sample_files
from act.utils.data_utils import accumulate_precip


if __name__ == "__main__":
    ds = act.io.arm.read_arm_netcdf(sample_files.EXAMPLE_CEIL1)
    display = TimeSeriesDisplay(ds)
    display.plot('backscatter', y_rng=[0, 5000], use_var_for_y='range')
    plt.show()
