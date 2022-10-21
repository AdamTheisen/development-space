import act
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

files = glob.glob('./data/NEON/temperature.csv')
obj = act.io.csvfiles.read_csv(files[0])
obj['startDateTime'] = obj['startDateTime'].astype(np.datetime64)
obj['time'] = obj['startDateTime']
obj = obj.set_index({'index': 'startDateTime'})

files = glob.glob('./data/NEON/temperature2.csv')
obj2 = act.io.csvfiles.read_csv(files[0])
obj2['startDateTime'] = obj2['startDateTime'].astype(np.datetime64)
obj2['time'] = obj2['startDateTime']
obj2 = obj2.set_index({'index': 'startDateTime'})

files = glob.glob('./data/NEON/temperature3.csv')
obj3 = act.io.csvfiles.read_csv(files[0])
obj3['startDateTime'] = obj3['startDateTime'].astype(np.datetime64)
obj3['time'] = obj3['startDateTime']
obj3 = obj3.set_index({'index': 'startDateTime'})

files = glob.glob('./data/NEON/temperature4.csv')
obj4 = act.io.csvfiles.read_csv(files[0])
obj4['startDateTime'] = obj4['startDateTime'].astype(np.datetime64)
obj4['time'] = obj4['startDateTime']
obj4 = obj4.set_index({'index': 'startDateTime'})

files = glob.glob('./data/NEON/temperature5.csv')
obj5 = act.io.csvfiles.read_csv(files[0])
obj5['startDateTime'] = obj5['startDateTime'].astype(np.datetime64)
obj5['time'] = obj5['startDateTime']
obj5 = obj5.set_index({'index': 'startDateTime'})

files = glob.glob('./data/NEON/temperature6.csv')
obj6 = act.io.csvfiles.read_csv(files[0])
obj6['startDateTime'] = obj6['startDateTime'].astype(np.datetime64)
obj6['time'] = obj6['startDateTime']
obj6 = obj6.set_index({'index': 'startDateTime'})

new = {'site1':obj, 'site2':obj2, 'site3':obj3,'site4':obj4,'site5':obj5,'site6':obj6}

display = act.plotting.TimeSeriesDisplay(new,figsize=(12,8),subplot_shape=(1,))
set_title = 'NEON Triple Aspirated Temperature at Sites in the Great Lakes Region'
display.plot('tempTripleMean',dsname='site1',marker='.', color='b',set_title=set_title, subplot_index=(0,))
display.plot('tempTripleMean',dsname='site2',marker='.', color='k',set_title=set_title, subplot_index=(0,))
display.plot('tempTripleMean',dsname='site3',marker='.', color='r',set_title=set_title, subplot_index=(0,))
display.plot('tempTripleMean',dsname='site4',marker='.', color='g',set_title=set_title, subplot_index=(0,))
display.plot('tempTripleMean',dsname='site5',marker='.', color='y',set_title=set_title, subplot_index=(0,))
display.plot('tempTripleMean',dsname='site6',marker='.', color='c',set_title=set_title, subplot_index=(0,))
display.axes[0].legend()

#
plt.tight_layout()
plt.savefig('./images/neon_temp.png')
