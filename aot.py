import act
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

files = glob.glob('./data/AOT/data.csv')

obj = act.io.csvfiles.read_csv(files[0],sep=',')

time = obj['timestamp']
time = pd.to_datetime(time)

obj['timestamp'].values = time
obj = obj.set_index({'index': 'timestamp'})

#test = obj.where(obj['node_id'].astype(str) == '001e0610ee5d', drop=True)
#test = obj.where(obj['sensor'] != 'tsys01', drop=True)
test = obj.where(obj['parameter'] == 'temperature', drop=True)
test = test.where(test['value_raw'] != 65535, drop=True)



test['value_hrf'] = test['value_hrf'].astype(float)

test = test.where(test['value_hrf'] > -10,drop=True)
test = test.where(test['value_hrf'] < 60,drop=True)

display = act.plotting.TimeSeriesDisplay(test,figsize=(12,6),subplot_shape=(1,))
set_title = 'AOT Temperature Data from All Sensors Across the Chicago Metro'
display.plot('value_hrf',marker=',', color='b',set_title=set_title, subplot_index=(0,))

plt.tight_layout()
plt.savefig('./images/aot.png')
