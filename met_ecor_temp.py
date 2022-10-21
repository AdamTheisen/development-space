import matplotlib
matplotlib.use('Agg')
import act
import glob
import matplotlib.pyplot as plt
import json
import numpy as np

#Read in ARM Live Data Webservice Token and Username
with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

date = '2021'

for i in range(1,13):
    d = date + str(i).zfill(2)
    ds = 'sgpmetE13.b1'
    files = glob.glob(''.join(['./',ds,'/*.'+d+'*']))
    met = act.io.armfiles.read_netcdf(files)

    ds = 'sgpecorsfE14.b1'
    files = glob.glob(''.join(['./',ds,'/*.'+d+'*']))
    ecor = act.io.armfiles.read_netcdf(files)

    try:
        ecor_t = ecor['sonic_temperature'].resample(time='30min').mean() - 273.15
        met_t = met['temp_mean'].resample(time='30min').mean()

        print(d, len(ecor_t.values), len(met_t.values), np.nanmean(ecor_t.values - met_t.values))
        met.close()
        ecor.close()
    except:
        pass
