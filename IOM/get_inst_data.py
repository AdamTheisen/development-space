import datetime as dt
import requests
import pandas as pd
import numpy as np
import time
import json
import os
from collections import OrderedDict
import sys

import urllib.request

def convert_datetime_time_from_epoch(d):
    epoch = dt.datetime.utcfromtimestamp(d/1000.)
    print(d, epoch)
    return ('%f' % ((d - epoch).total_seconds() * 1000)).split(".")[0]


def get_url(search_url):
    with urllib.request.urlopen(search_url) as url:
        results = json.loads(url.read().decode())
    return results

#1    Open - Requires Action
#2    In Progress - Assignments
#3    Closed - All Assignments Completed
#4    Open - Escalated to PRB Attention
#6    Closed - No DQR or PRB Requested Solution Assignments Required
#8    Waiting - For Spares
#9    Waiting - For Site Visit
#9999    DQPR Rejected

non_rejected_status = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
all_status = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,9999]
open_waiting_status = [1,2,4,8,9]
closed_status = [3,5,6,7]

codeDesc=['Incorrect','Questionable','Missing','-9999','Data Unaffected']
statusDesc=['Open - Requires Action','In Progress - Assignments',
'Closed - All Assignments Complete', 'Open - Escalated to PRB Attention',
'Closed - No DQR or PRB Requested Solution','Waiting - For Spares',
'Waiting - For Site Visit','DQPR Rejected']

comment_url = 'https://adc.arm.gov/dq/api/dq/comment/user/'
search_url = 'https://adc.arm.gov/dq/api/dq/dqpr/search?'
pid_url = 'https://adc.arm.gov/arm-people-api/person/search?personIds='
lname_url = 'https://adc.arm.gov/arm-people-api/person/search?nameLast='

instruments = ['maws']

for instrument in instruments:
    criteria = {
                'instrument': instrument,
                'start_date': '2015-01-01%2000:00:00'
               }

    search = search_url
    for c in criteria:
        search += c + '=' + criteria[c] + '&'

    results = get_url(search)
    summary = {}
    for dqpr in results:
        summary[dqpr['dqprNo']] = {}
        summary[dqpr['dqprNo']]['startDate'] = dqpr['dqprStartdateStr']
        summary[dqpr['dqprNo']]['endDate'] = dqpr['dqprEnddateStr']
        summary[dqpr['dqprNo']]['probDesc'] = dqpr['probDesc']
        summary[dqpr['dqprNo']]['qaCode'] = dqpr['qaCode']
        summary[dqpr['dqprNo']]['status'] = dqpr['dqprStatus']

        comments = get_url(comment_url+str(dqpr['dqprNo']))
        comment = '' if len(comments) == 0 else comments[-1]['comment']
        commentDate = 0 if len(comments) == 0 else comments[-1]['commentDate']
        commentDate = dt.datetime.utcfromtimestamp(commentDate/1000.) if commentDate != 0 else ''

        summary[dqpr['dqprNo']]['last_comment'] = comment
        summary[dqpr['dqprNo']]['last_comment_date'] = commentDate


    print(summary)
