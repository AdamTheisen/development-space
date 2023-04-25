import act
import glob
import matplotlib.pyplot as plt
import math
import numpy as np


def bard_td(temperature, relative_humidity):
    """Calculate the dewpoint temperature from the temperature and relative humidity.

    Args:
        temperature (float): The ambient temperature in degrees Celsius.
        relative_humidity (float): The relative humidity in percent.

    Returns:
        float: The dewpoint temperature in degrees Celsius.
    """

    A = 17.27
    B = 237.7
    alpha = ((A * temperature) / (B + temperature)) + math.log(relative_humidity/100.0)
    return (B * alpha) / (A - alpha)

def chatgpt_td(temperature, relative_humidity):
    """
    Calculates the dewpoint temperature in Celsius given the temperature in Celsius and the relative humidity.
    """
    a = 17.27
    b = 237.7
    alpha = ((a * temperature) / (b + temperature)) + math.log(relative_humidity/100.0)
    dewpoint = (b * alpha) / (a - alpha)
    return dewpoint


if __name__ == "__main__":
    files = glob.glob('./data/nsatwrC1.b1/*')
    files.sort()
    print(files[0])
    ds = act.io.read_netcdf(files[0])

    files = glob.glob('./data/nsamawsC1.b1/*')
    files.sort()
    print(files[0])
    ds_maws = act.io.read_netcdf(files[0])

    ds = ds.isel(height=[0])
    ds.utils.change_units(variables='temp_mean', desired_unit='degC')
    t = ds['temp_mean'].values[:, 0]
    rh = ds['rh_mean'].values[:, 0]
    td = t - ((100. - rh)/5.)

    td_bard = []
    td_chatgpt = []
    for i in range(len(t)):
        td_bard.append(bard_td(t[i], rh[i]))
        td_chatgpt.append(chatgpt_td(t[i], rh[i]))
        #print(t[i], rh[i], td[i], td_bard[-1], td_chatgpt[-1])

    time = ds['time'].values
    display = act.plotting.TimeSeriesDisplay({'TWR': ds, 'MAWS': ds_maws})
    display.plot('dew_point_mean',label='Tower', dsname='TWR', force_line_plot=True)
    display.plot('atmospheric_dew_point',label='MAWS', dsname='MAWS')
    display.axes[0].plot(time, td_bard, '.', label='Bard')
    display.axes[0].plot(time, td_chatgpt, label='ChatGPT')
    display.axes[0].plot(time, td, label='Quick Calc')
    #display.axes[0].set_ylim([-38, -26])
    plt.legend()
    plt.show()
