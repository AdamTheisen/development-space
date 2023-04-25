import act
import xarray as xr
import glob
import json


dod = act.io.armfiles.create_obj_from_arm_dod('vdis.b1', {'time': 1440}, scalar_fill_dim='time')

files = glob.glob('./sgpvdisC1.b1/*')
obj = act.io.armfiles.read_netcdf(files)

diff = {}
for v in dod:
    if v not in obj:
        diff[v] = ['Missing Variable ' + v]
        continue
    for a in dod[v].attrs:
        if a not in obj[v].attrs:
            if a not in obj[v].encoding:
                if v in diff:
                    diff[v].append('Missing attribute ' + a)
                else:
                    diff[v] = ['Missing attribute ' + a]

for v in obj:
    if v not in dod:
        diff[v] = ['Additional Variable ' + v]
        continue
    for a in obj[v].attrs:
        if a not in dod[v].attrs:
            if a not in dod[v].encoding:
                if v in diff:
                    diff[v].append('AAdditional attribute ' + a)
                else:
                    diff[v] = ['Additional attribute ' + a]

for a in dod.attrs:
    if a not in obj.attrs:
        if 'Global Attributes' not in diff:
            diff['Global Attributes'] = ['Missing global attribute ' + a]
        else:
            diff['Global Attributes'].append('Missing global attribute ' + a)

if len(diff) == 0:
    diff = 'No differences found'

print(json.dumps(diff, indent=4))
