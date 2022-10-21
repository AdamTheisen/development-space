import urllib.request, json 
import xarray as xr
import numpy as np
import sys

def create_obj_from_arm_dod(ds, version=None):

    base_url = 'https://pcm.arm.gov/pcmserver/dods/'

    with urllib.request.urlopen(base_url+ds) as url:
        data = json.loads(url.read().decode())

    keys = list(data['versions'].keys())
    if version not in keys:
        print(' '.join(['Version:', version, 'not available. Using Version:', keys[-1]]))
        version = keys[-1]

    variables = data['versions'][version]['vars']

    obj = xr.Dataset()

    atts = {}
    for a in data['versions'][version]['atts']:
        if a['name'] == 'string':
            continue
        if a['value'] is None:
            a['value'] = ''
        atts[a['name']] = a['value']

    obj.attrs = atts

    

    for v in variables:
        dims = v['dims']
        data_na = np.full(np.ones(np.shape(dims), dtype=int), np.nan)
        if np.size(data_na) == 0:
            data_na = np.nan 

        atts = {}
        for a in  v['atts']:
            if a['name'] == 'string':
                continue
            if a['value'] is None:
                a['value'] = ''
            atts[a['name']] = a['value']

        da = xr.DataArray(data=data_na, dims=v['dims'], name=v['name'], attrs=atts)

        obj[v['name']] = da

    obj.to_netcdf('./pcm_test.nc')


if __name__ == "__main__":
    ds = 'vdis.b1'
    ver = '1.5'
    create_obj_from_arm_dod(ds, version=ver)

