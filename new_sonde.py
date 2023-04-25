import act
import matplotlib.pyplot as plt
import glob


ds = act.io.read_netcdf(act.tests.sample_files.EXAMPLE_SONDE1)
display = act.plotting.SkewTDisplay(ds)
display.plot_enhanced_skewt(color_field='alt', component_range=85)
#files = glob.glob(act.tests.sample_files.EXAMPLE_SONDE1)
#ds = act.io.read_netcdf(files)
#
#display = act.plotting.SkewTDisplay(ds)
#display.plot_enhanced_skewt(color_field='alt')

#fig, axs = plt.subplot_mosaic([['a', 'a', 'b'], ['a', 'a', 'b'], ['a', 'a', 'c'], ['a', 'a', 'c']], layout='constrained')
#display = act.plotting.SkewTDisplay(ds)
#display.plot_from_u_and_v('u_wind', 'v_wind', 'pres', 'tdry', 'dp')
#display.plot_hodograph('wspd', 'deg', set_axes=axs['b'], color_field='alt')
#overwrite = {
#    'test': 124.2,
#    'test2': 12434.3,
#    'test6': 2345.3
#}
#display.add_stability_info(set_axes=axs['c'])
#display.plot_hodograph('u_wind', 'v_wind', uv_flag=True, set_axes=axs['b'], color_field='alt')

plt.show()
