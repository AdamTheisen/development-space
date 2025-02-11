import datetime as dt
import numpy as np
import requests
import json
import pandas as pd

def proc_dqr(datastream, start_date, end_date, assessment='incorrect'):
    # Create URL
    url = 'https://dqr-web-service.svcs.arm.gov/dqr_full'
    url += f"/{datastream}"
    url += f"/{start_date}/{end_date}"
    url += f"/{assessment}"

    # Call web service
    req = requests.get(url)

    # Check status values and raise error if not successful
    status = req.status_code
    if status == 400:
        raise ValueError('Check parameters')
    if status == 500:
        raise ValueError('DQR Webservice Temporarily Down')

    # Convert from string to dictionary
    docs = json.loads(req.text)

    # If no DQRs found will not have a key with datastream.
    # The status will also be 404.
    try:
        docs = docs[datastream]
    except:
        return

    d_range = pd.date_range(start_date, end_date, freq='1min', inclusive='left')
    df = pd.DataFrame({'counts': np.zeros(len(d_range))}, index=d_range)
    dqr_results = {}
    for quality_category in docs:
        for dqr_number in docs[quality_category]:
            index = np.array([], dtype=np.int32)
            for time_range in docs[quality_category][dqr_number]['dates']:
                starttime = np.datetime64(time_range['start_date'])
                endtime = np.datetime64(time_range['end_date'])
                df.loc[starttime:endtime] += 1

            dqr_results[dqr_number] = {
                'starttime': starttime,
                'endtime': endtime,
                'test_assessment': quality_category.lower().capitalize(),
                'test_meaning': f"{dqr_number} : {docs[quality_category][dqr_number]['description']}",
                'variables': docs[quality_category][dqr_number]['variables'],
            }

    total_per = df[df > 0].count()/df.count()

    df_dqr = df[df > 0]
    group = df.groupby(pd.PeriodIndex(df.index, freq="Y"))
    group_dqr = df_dqr.groupby(pd.PeriodIndex(df_dqr.index, freq="Y"))
    print(group_dqr.count()/group.count())
    print(total_per)


if __name__ == "__main__":

    fc = {'gan': {'start_date': '2011-10-01', 'end_date': '2012-03-31'},
          'pgh': {'start_date': '2011-06-13', 'end_date': '2012-03-31'},
          'mag': {'start_date': '2012-10-01', 'end_date': '2013-09-30'},
          'pvc': {'start_date': '2012-07-01', 'end_date': '2013-06-30'},
          'mao': {'start_date': '2014-01-01', 'end_date': '2015-11-30'},
          'tmp': {'start_date': '2014-02-01', 'end_date': '2014-09-13'},
          'acx': {'start_date': '2015-01-14', 'end_date': '2015-02-12'},
          'awr': {'start_date': '2015-11-23', 'end_date': '2017-01-05'},
          'asi': {'start_date': '2016-06-01', 'end_date': '2017-10-31'},
          'cor': {'start_date': '2018-10-01', 'end_date': '2019-04-30'},
          'mos': {'start_date': '2019-10-11', 'end_date': '2020-10-01'},
          'anx': {'start_date': '2019-12-01', 'end_date': '2020-05-31'},
          'hou': {'start_date': '2021-10-01', 'end_date': '2022-09-30'},
          'guc': {'start_date': '2021-11-01', 'end_date': '2023-06-15'},
          'epc': {'start_date': '2023-02-15', 'end_date': '2024-02-14'},
          'sgp': {'start_date': '2020-01-01', 'end_date': '2023-12-31'},
         }

    #site = 'guc'
    #instruments = ['kazrcfrgeM1.a1', 'xprecipradarS2.00']
    site = 'sgp'
    instruments = ['metE13.b1']
    for inst in instruments:
        sd = ''.join(fc[site]['start_date'].split('-'))
        ed = ''.join(fc[site]['end_date'].split('-'))
        proc_dqr(site + inst, sd, ed)

