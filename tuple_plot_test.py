import matplotlib
import act.io.armfiles as arm
import act.discovery.get_files as get_data
import act.tests.sample_files as sample_files
import act.corrections.ceil as ceil
import pytest
import glob
import matplotlib.pyplot as plt
import os
import boto3
import numpy as np

from act.plotting import TimeSeriesDisplay, WindRoseDisplay
from botocore.handlers import disable_signing

conn = boto3.resource('s3')
conn.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
bucket = conn.Bucket('act-tests')
if not os.path.isdir((os.getcwd() + '/data/')):
    os.makedirs((os.getcwd() + '/data/'))

for item in bucket.objects.all():
    bucket.download_file(item.key, (os.getcwd() + '/data/' + item.key))

ceil_ds = arm.read_netcdf('data/sgpceilC1.b1*')
sonde_ds = arm.read_netcdf(
    sample_files.EXAMPLE_MET_WILDCARD)
ceil_ds = ceil.correct_ceil(ceil_ds)

# You can use tuples if the datasets in the tuple contain a
# datastream attribute. This is required in all ARM datasets.
display = TimeSeriesDisplay(
    (ceil_ds, sonde_ds), subplot_shape=(2,), figsize=(15, 10))
display.plot('backscatter', 'sgpceilC1.b1', subplot_index=(0,))
display.plot('temp_mean', 'sgpmetE13.b1', subplot_index=(1,))
display.day_night_background('sgpmetE13.b1', subplot_index=(1,))
plt.show()
ceil_ds.close()
sonde_ds.close()
