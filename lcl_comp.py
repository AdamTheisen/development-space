import act
import glob
import matplotlib.pyplot as plt
import math
import numpy as np


def bard_lcl(ta, td, p):
    """Calculate the lifting condensation level (LCL) from the starting point.

    Args:
        ta (float): The ambient temperature in degrees Celsius.
        td (float): The dew point temperature in degrees Celsius.
        p (float): The barometric pressure in millibars.

    Returns:
        float: The LCL in meters.
    """
    #print(ta, td, p)
    # Calculate the dry adiabatic lapse rate.
    gamma_d = 9.80665 / 287.04 * (1 - 0.0065 * ta)

    # Calculate the saturated adiabatic lapse rate.
    gamma_s = 9.80665 / 287.04 * (1 - 0.0065 * ta) * (1 + 0.622 * td / ta)

    # Calculate the LCL.
    lcl = p * (gamma_s / gamma_d) ** (ta / td)

    return lcl


def chatgpt_lcl(T, Td, p):
    # Constants
    T0 = 273.15  # Standard temperature at sea level in Kelvin
    g = 9.81     # Gravitational acceleration in m/s^2
    Lv = 2.5e6   # Latent heat of vaporization in J/kg

    # Surface conditions
    T = T + T0  # Surface temperature in Kelvin
    Td = Td + T0 # Surface dew point temperature in Kelvin
    p = p  # Surface pressure in hPa

    # Calculate the lifting condensation level (LCL)
    e = 6.112 * pow(10, (7.5*(Td-T)/(Td-T+237.3)))  # Vapor pressure at surface temperature
    q = 0.622 * e / (p - 0.378 * e)                # Specific humidity at surface
    L = -Lv*q/g                                   # Lifting condensation level temperature lapse rate
    Tlcl = T - (Td - T) / ((1/L) + 0.00115)         # Lifting condensation level temperature in Kelvin
    h = 125.*(T - Tlcl)                             # Lifting condensation level height in meters (approximate)

    return h

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
    files = glob.glob('./data/sgplclC1.c1/*')
    ds = act.io.read_netcdf(files[0])

    ds = ds.isel(stations=[0])
    ds.utils.change_units(variables='temperature', desired_unit='degC')
    t = ds['temperature'].values[:, 0]
    rh = ds['relative_humidity'].values[:, 0]
    td = t - ((100. - rh)/5.)

    ds.utils.change_units(variables='pressure', desired_unit='millibar')
    p_mb = ds['pressure'].values [:, 0]
    ds.utils.change_units(variables='pressure', desired_unit='hPa')
    p_hPa = ds['pressure'].values [:, 0]

    td_bard = []
    td_chatgpt = []
    lcl_bard = []
    lcl_chatgpt = []
    for i in range(len(t)):
        td_bard.append(bard_td(t[i], rh[i]))
        td_chatgpt.append(chatgpt_td(t[i], rh[i]))
        lcl_bard.append(bard_lcl(t[i], td_bard[i], p_mb[i]))
        lcl_chatgpt.append(chatgpt_lcl(t[i], td_chatgpt[i], p_hPa[i]))
        print(lcl_bard[-1], lcl_chatgpt[-1])


    #lcl_aprox = 125. * (t - td)
    time = ds['time'].values
    display = act.plotting.TimeSeriesDisplay(ds)
    display.plot('lcl', force_line_plot=True, label='LCL VAP')
    display.axes[0].plot(time, lcl_bard, label='LCL Bard')
    display.axes[0].plot(time, lcl_chatgpt, label='LCL ChatGPT')
    plt.legend()
    plt.show()
