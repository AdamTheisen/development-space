import numpy as np
from thermofeel import thermofeel

t = 37.7778
rh = 45.
global_wet_bulb_simple = thermofeel.calculate_wbgt_simple((t + 273.15), rh)
print((global_wet_bulb_simple - 273.15) * 9./5. + 32.)

Tw = t * np.arctan(0.151977 * np.sqrt((rh + 8.313659))) +\
     np.arctan(t + rh) - np.arctan(rh - 1.676331) +\
     0.00391838 * pow(rh, 3./2.) * np.arctan(0.023101 * rh) - 4.686035

print(Tw * 9./5. + 32)

ea = 6.11 * pow(10, (7.5 * t) / (237.3 + t))
es = (ea * 100 / rh)
tw2 = 0.567 * (t) + 0.393 * es + 3.94

print(tw2)
