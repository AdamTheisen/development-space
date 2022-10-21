import act
import glob
import matplotlib.pyplot as plt


files = glob.glob('/Users/atheisen/Code/ACT/act/tests/data/sgpmet*20190508*cdf')
time = '2019-05-08T08:00:00.000000000'
data = {}
fields = {}
for f in files:
    obj = act.io.armfiles.read_netcdf(f)
    data.update({f: obj})
    fields.update({f: ['lon','lat','temp_mean']})

display = act.plotting.ContourDisplay(data, figsize=(8,8))
display.create_contour(fields=fields, time=time, levels=50)
plt.savefig('./images/test_contour.png',dpi=1000)

