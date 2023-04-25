import act
import requests
import json

ds = 'sgpmetE13.b1'
site = ds[0:3]
c_start = '2022-05-01'
c_end = '2022-05-31'


doi = act.discovery.get_arm_doi(ds, c_start, c_end)
print(doi)
