import act
import numpy as np

url = ['https://downloads.psl.noaa.gov/psd2/data/realtime/DisdrometerParsivel/Stats/ctd/2022/002/ctd2200200_stats.txt',
       'https://downloads.psl.noaa.gov/psd2/data/realtime/DisdrometerParsivel/Stats/ctd/2022/002/ctd2200201_stats.txt',
       'https://downloads.psl.noaa.gov/psd2/data/realtime/DisdrometerParsivel/Stats/ctd/2022/002/ctd2200202_stats.txt']

obj = act.io.noaapsl.read_psl_parsivel(url)

print(obj['number_density_drops'].values[10,10])
