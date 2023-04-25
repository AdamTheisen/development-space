import act
import glob
import matplotlib.pyplot as plt

site_code = 'BARR'
product_id = 'DP1.00002.001'
product_id = 'DP1.00001.001'

#act.discovery.get_neon.download_neon_data(site_code, product_id, '2022-09')

files = glob.glob('./' + site_code + '_' + product_id + '/*.010.*2min*expanded*csv')
variable_files = glob.glob('./' + site_code + '_' + product_id + '/*.variables.*csv')
loc_files = glob.glob('./' + site_code + '_' + product_id + '/*.sensor_positions.*csv')
files.sort()
variable_files.sort()
loc_files.sort()

obj = act.io.neon.read_neon_csv(files)
print(obj)
display = act.plotting.TimeSeriesDisplay(obj)
#display.plot('tempSingleMean')
display.plot('windSpeedMean')
plt.show()
