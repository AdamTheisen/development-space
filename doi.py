import act
import requests
import json

ds = 'sgpstampE13.b1'
ds = 'test'
site = ds[0:3]
c_start = '2022-05-01'
c_end = '2022-05-31'


doi = act.discovery.get_arm_doi(ds, c_start, c_end)
print(doi)
