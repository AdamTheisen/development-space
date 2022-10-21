import sys
sys.path.insert(0,'/Users/atheisen/Code/sandbox/ACT')
import act
import matplotlib.pyplot as plt

obj = act.io.noaagml.read_gml(act.tests.sample_files.EXAMPLE_GML_RADIATION, datatype='RADIATION')
obj2 = act.io.noaagml.read_gml(act.tests.sample_files.EXAMPLE_GML_OZONE, datatype='OZONE')

print(list(obj2.keys()))
print(obj2['time'].values)
new = {'radiation': obj, 'ozone': obj2}
display = act.plotting.TimeSeriesDisplay(new, subplot_shape=(2,))
display.plot('air_temperature_10m', dsname='radiation', subplot_index=(0,))
display.plot('ozone', dsname='ozone', color='k', subplot_index=(1,))
display.set_yrng([-30, -20])
plt.show()
