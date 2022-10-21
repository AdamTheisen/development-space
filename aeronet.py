import act
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

files = glob.glob('./data/aeronet_locations_v3.txt')

obj = act.io.csvfiles.read_csv(files[0],sep=',')

lat = [21.67777778, 37.24027778]
lon = [-91.15361111, -75.08277778]

obj = obj.where(obj['Latitude'] > lat[0], drop=True)
obj = obj.where(obj['Latitude'] < lat[1], drop=True)
obj = obj.where(obj['Longitude'] > lon[0], drop=True)
obj = obj.where(obj['Longitude'] < lon[1], drop=True)

for i in range(len(obj['index'])):
    with open('./aeronet.txt', "a") as myfile:
        myfile.write(','.join([str(obj['Site_Name'].values[i]), str(obj['Latitude'].values[i]), str(obj['Longitude'].values[i])])+'\n')
