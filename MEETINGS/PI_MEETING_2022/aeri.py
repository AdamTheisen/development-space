import glob
import act
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import xarray as xr
import matplotlib
import pandas as pd
matplotlib.rcParams.update({'font.size': 22})


date = '20220801*'
files = glob.glob('./gucaerich1M1.b1/*'+date+'*')
obj = act.io.armfiles.read_netcdf(files)
obj = obj.where(obj['hatchOpen'] == 1)
obj = act.retrievals.aeri.aeri2irt(obj, hatch_name=None, tolerance=0.05, maxiter=100)

files = glob.glob('./gucirtM1.b1/*'+date+'*')
obj2 = act.io.armfiles.read_netcdf(files)

files = glob.glob('./gucceil10mM1.b1/*'+date+'*')
obj3 = act.io.armfiles.read_netcdf(files)
obj3 = act.corrections.correct_ceil(obj3)

t1 = 'SAIL Corrected Ceilometer Backscatter for 20220801'
t2 = 'SAIL Infrared Sky Temperature Calculated from the AERI for 20220801'
display = act.plotting.TimeSeriesDisplay({'aeri': obj, 'irt': obj2, 'ceil': obj3}, subplot_shape=(2,))
display.plot('backscatter', dsname='ceil', subplot_index=(0,), set_title=t1, cmap='act_HomeyerRainbow', vmin=0)
#display.plot('sky_ir_temp', dsname='irt', subplot_index=(1,))
display.plot('aeri_irt_equiv_temperature', dsname='aeri', subplot_index=(1,), set_title=t2)
#display.plot('first_cbh', dsname='ceil', subplot_index=(1,), set_title=t2, secondary_y=True)
#display.set_xrng([pd.to_datetime('2022-08-01 22:10:00'), pd.to_datetime('2022-08-01 23:50:00')])
display.cbs[0].ax.tick_params(labelsize=10)
plt.subplots_adjust(hspace=0.25)
plt.show()

sys.exit()

obj = obj.resample(time='1min').nearest()
obj2 = obj2.resample(time='1min').nearest()
obj3 = obj3.resample(time='1min').nearest()

m_obj = xr.merge([obj, obj2, obj3], compat='override')

print(m_obj['time'].values[0])

t1 = 'SAIL Corrected Ceilometer Backscatter for 20220901 - 20220909'
t2 = 'SAIL Infrared Sky Temperature Calculated from the AERI for 20220901 - 20220909'
display = act.plotting.TimeSeriesDisplay(m_obj, subplot_shape=(2,))
display.plot('backscatter', subplot_index=(0,), set_title=t1, cmap='act_HomeyerRainbow', vmin=0, fontsize=16)
#display.plot('aeri_irt_equiv_temperature', subplot_index=(1,), set_title=t2, invert_y_axis=True)
scat = display.axes[1].scatter(m_obj['time'].values, m_obj['first_cbh'].values, c=m_obj['aeri_irt_equiv_temperature'].values)
cbaxes = display.fig.add_axes([0.925, 0.12, 0.01, 0.325]) 
plt.colorbar(scat, cax=cbaxes)
plt.show()
