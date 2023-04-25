import numpy as np
from scipy.interpolate import interp1d

def calc_lcl(ta, td, p):
    """Calculate the lifting condensation level (LCL) from the starting point.

    Args:
        ta (float): The ambient temperature in degrees Celsius.
        td (float): The dew point temperature in degrees Celsius.
        p (float): The barometric pressure in millibars.

    Returns:
        float: The LCL in meters.
    """

    # Calculate the dry adiabatic lapse rate.
    gamma_d = 9.80665 / 287.04 * (1 - 0.0065 * ta)

    # Calculate the saturated adiabatic lapse rate.
    gamma_s = 9.80665 / 287.04 * (1 - 0.0065 * ta) * (1 + 0.622 * td / ta)

    # Calculate the LCL.
    lcl = p * (gamma_s / gamma_d) ** (ta / td)

    return lcl

def main():
    """Calculate the LCL for a given set of surface conditions."""

    # Get the surface temperature and dew point from the user.
    ta = float(input("Enter the ambient temperature (°C): "))
    td = float(input("Enter the dew point temperature (°C): "))
    p = float(input("Enter the barometric pressure (mb): "))

    # Calculate the LCL.
    lcl = calc_lcl(ta, td, p)

    # Print the LCL.
    print("The LCL is {} meters.".format(lcl))

if __name__ == "__main__":
    main()

