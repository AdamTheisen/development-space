import act
import glob
import matplotlib.pyplot as plt

files = glob.glob(act.tests.EXAMPLE_MET_CSV)
obj = act.io.csvfiles.read_csv(files[0])

display = act.plotting.TimeSeriesDisplay(obj,figsize=(10,8))
set_title = ' '.join(['MET TEMP_MEAN on ',
    act.utils.datetime_utils.numpy_to_arm_date(obj.time.values[0])])
display.plot('temp_mean',color='b',set_title=set_title,day_night_background=True)
#display.day_night_background()
display.axes[0].legend()
plt.savefig('./csv_test.png')
