# Constants
T0 = 273.15  # Standard temperature at sea level in Kelvin
g = 9.81     # Gravitational acceleration in m/s^2
Lv = 2.5e6   # Latent heat of vaporization in J/kg

# Surface conditions
T = 25 + T0  # Surface temperature in Kelvin
Td = 15 + T0 # Surface dew point temperature in Kelvin
p = 1013.25  # Surface pressure in hPa

# Calculate the lifting condensation level (LCL)
e = 6.112 * pow(10, (7.5*(Td-T)/(Td-T+237.3)))  # Vapor pressure at surface temperature
q = 0.622 * e / (p - 0.378 * e)                # Specific humidity at surface
L = -Lv*q/g                                   # Lifting condensation level temperature lapse rate
Tlcl = T - (Td - T) / ((1/L) + 0.00115)         # Lifting condensation level temperature in Kelvin
h = 125*(T - Tlcl)                             # Lifting condensation level height in meters (approximate)

print("The lifting condensation level is at a height of", round(h), "meters.")
