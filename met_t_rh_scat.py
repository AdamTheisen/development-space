import act
import glob
import matplotlib.pyplot as plt

sites = ['sgp']
inst = 'met'
fac = ['E13']
lev = 'b1'

data_dir = '/Users/atheisen/Code/ARM-Climatologies/data/'

for i, s in enumerate(sites):
    ds = s + inst + fac[i] + '.' + lev
    print(data_dir + ds)
    files = glob.glob(data_dir + ds + '/*b1.20*')
    files.sort()
    ds = act.io.arm.read_arm_netcdf(files)
    ds = ds.where(ds['temp_mean'].compute() > 25., drop=True)
    ds = ds.where(ds['temp_mean'].compute() < 50., drop=True)
    ds = ds.where(ds['rh_mean'].compute() <= 100., drop=True)

    fig, ax = plt.subplots()
    plt.scatter(ds['temp_mean'] * 9. / 5. + 32., ds['rh_mean'])
    ax.set_xlabel('Temperature (F)')
    ax.set_ylabel('Relative Humidity (%)')

    ds2 = ds.where(ds['temp_mean'].compute() >= 29., drop=True)
    ds2 = ds2.where(ds2['rh_mean'].compute() >= 80, drop=True)
    plt.scatter(ds2['temp_mean'] * 9. / 5. + 32., ds2['rh_mean'], c='red')

    ds2 = ds.where(ds['temp_mean'].compute() >= 32.2, drop=True)
    ds2 = ds2.where(ds2['rh_mean'].compute() >= 57.5, drop=True)
    plt.scatter(ds2['temp_mean'] * 9. / 5. + 32., ds2['rh_mean'], c='red')

    ds2 = ds.where(ds['temp_mean'].compute() >= 35., drop=True)
    ds2 = ds2.where(ds2['rh_mean'].compute() >= 40, drop=True)
    plt.scatter(ds2['temp_mean'] * 9. / 5. + 32., ds2['rh_mean'], c='red')

    ds = ds.where(ds['temp_mean'].compute() >= 37.8, drop=True)
    ds = ds.where(ds['rh_mean'].compute() >= 27.5, drop=True)
    plt.scatter(ds['temp_mean'] * 9. / 5. + 32., ds['rh_mean'], c='red')

    ds2 = ds.where(ds['temp_mean'].compute() >= 40.5, drop=True)
    ds2 = ds2.where(ds2['rh_mean'].compute() >= 17.5, drop=True)
    plt.scatter(ds2['temp_mean'] * 9. / 5. + 32., ds2['rh_mean'], c='red')

    ds2 = ds.where(ds['temp_mean'].compute() >= 43.3, drop=True)
    ds2 = ds2.where(ds2['rh_mean'].compute() >= 10, drop=True)
    plt.scatter(ds2['temp_mean'] * 9. / 5. + 32., ds2['rh_mean'], c='red')


    plt.show()
