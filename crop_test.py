import act
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

lon, lat = (-97.1709, 36.8172)
year = 2018
fac = ['E31','E32','E33','E34','E35']
lat = [37.1509,36.819,36.9255,37.0694,35.8615]
lon = [-98.362,-97.8199,-97.0817,-96.7606,-97.0695]
arm_type=['Pasture','Pasture','Field to South, Grass','Pasture','Pasture']

fac = [fac[0]]
for i,f in enumerate(fac):
    crop = act.discovery.get_cropscape.croptype(lat[i],lon[i],year)

    print(f,' ',crop,'; ARM: ',arm_type[i])
