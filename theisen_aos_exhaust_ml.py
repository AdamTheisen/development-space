import matplotlib as mpl
mpl.use('Agg')
from matplotlib.dates import DateFormatter,date2num

import act.io.armfiles as arm
import act.plotting.plot as armplot
import act.discovery.get_files as get_data

import glob
import matplotlib.pyplot as plt
import os
import json
import sys
import numpy as np
import xarray as xr
import pandas as pd
import datetime
from sklearn.ensemble import RandomForestClassifier


with open('./token.json') as f:
    data = json.load(f)
username = data['username']
token = data['token']

#Set up initial data request
datastream = 'maraoscpcfM1.b1'
site = 'mar'
startdate = '2017-10-25'
enddate = '2018-03-26'
var = 'concentration'


def getAOSData(files):
    period = 15
    minp = 5

    obj = arm.read_netcdf(files,variables=var)
    diff = obj[var].diff('time',n=1)
    time = obj['time'].values

    ds = diff.to_dataset(name='cpc_diff')
    ds['cpc_diff'].values = abs(diff.values)
    ds = ds.rolling(time=period,min_periods=minp,center=True).mean()
    #ds['cpc'] = obj[var]

    return ds, obj[var]


if __name__ == '__main__':
    #Use ADC example script to get the data
    sdate = '20171111'
    edate = sdate
    files = glob.glob(''.join(['./',datastream,'/*',sdate,'*']))
    if len(files) == 0:
        get_data.download_data(username, token, datastream, startdate, enddate)
        files = glob.glob(''.join(['./',datastream,'/*',sdate,'*']))

    ds,cpc = getAOSData(files)
    time = ds['time'].values

    stime=['010738','011133']
    etime=['011017','011220']
    sbad=[]
    ebad=[]
    for i in range(len(stime)):
        sdummy=np.datetime64(''.join(['-'.join([sdate[0:4],sdate[4:6],sdate[6:8]]),
            'T',':'.join([stime[i][0:2],stime[i][2:4],stime[i][4:6]])]))
        sbad.append(sdummy)
        edummy=np.datetime64(''.join(['-'.join([edate[0:4],edate[4:6],edate[6:8]]),
            'T',':'.join([etime[i][0:2],etime[i][2:4],etime[i][4:6]])]))
        ebad.append(edummy)

    #Create the flag that we want to train for.. I.e. exhaust, no exhaust
    y_train=np.zeros(len(time))
    all_indices=[]
    for i in range(len(sbad)):
        idx=(time >= sbad[i])*(time <= ebad[i])
        all_indices.append(list(np.where(idx)[0]))

    #Set indices of previous periods to bad
    y_train[all_indices[0]]=1.

    #Sets different values for the RandomForestClassifier
    md=5 #Max depth of branches
    nest=25  #Total number of trees in the forest
    leafs=5 # Min number of leafs to use

    #Setup the model using 16 cores
    #Random_state=0 gaurantees that we will get the same result each time
    model = RandomForestClassifier(n_estimators = nest,max_depth=md,random_state=0,min_samples_leaf=leafs,n_jobs=16)

    #Fit the model  to the training dataset
    model.fit(ds.to_dataframe(),y_train)

    #If using a RandomForest, print out the feautre importance values
    #This will tell us what weight each variable had on the result
    try:
        fi=model.feature_importances_
        col=ds.columns
        print(col)
        print(fi)
        type='RandomForest'
    except:
        type='KNeighbors'

    #Get Data to apply the ML algorith to
    args = sys.argv
    if len(args) > 1:
        sdate = str(args[1])
        edate = sdate
    if len(args) > 2:
        edate = str(args[2])

    files = glob.glob(''.join(['./',datastream,'/*']))
    files.sort()
    files = [f for f in files if f.split('.')[-3] >= sdate and f.split('.')[-3] <= edate]

    obs_ds,cpc = getAOSData(files)
    X_test = obs_ds.to_dataframe()

    # 2 methods that could be used
    #This one just goes off the model prediction of 0 or 1 
    result=model.predict(X_test)
    idx=(result == 1)

    #Working method uses the probabilites that the model ouputs that a point is exhaust
    #Smooths that data out so we don't get noisy flagging every other time
    prob=model.predict_proba(X_test)[:,1]
    prob=pd.DataFrame(data=prob).rolling(min_periods=5,window=60*10,center=True).mean().values.flatten()

    #Flags anything with a probability higher than 1.5% which seems very small
    #but actually works out very well
    flag=0.00001
    idx=(prob >= flag)
    index=np.where(idx)

    #The rest of the program is plotting up the data for visualization and testing purposes
    time=X_test.index.to_pydatetime()

    #Plot Data#
    xmin = min(time)
    xmax = max(time)
    fig=plt.figure(figsize=(12,15))
    ax = fig.add_subplot(211)
    data = cpc.values
    cpc_time = cpc['time']

    ax.plot_date(cpc_time,data,'.',linewidth=1.5,color='k')
    ax.plot_date(time[index],data[index],'.',color='r',markersize=4)
    ax.set_title('CPC Concentration')
    ax.set_yscale('log')
    ax.set_ylim([0.1,1000000])
    ax.set_xlim([xmin,xmax])
    ax.yaxis.grid()


    ax = fig.add_subplot(212)
    data = X_test['cpc_diff'].values
    ax.plot_date(time,data,'.',linewidth=1.5,color='k')
    ax.plot_date(time[index],data[index],'.',color='r',markersize=4)
    ax.set_title('Difference CPC Concentration')
    ax.set_yscale('log')
    ax.set_ylim([0.1,100000])
    ax.set_xlim([xmin,xmax])
    ax.yaxis.grid()
 
    mpl.rcParams['agg.path.chunksize'] = 10000
    d=datetime.datetime.today()
    cdate=d.strftime("%Y%m%d")
    cwd = os.getcwd()
    fdir=cwd+'/'+site+'aos/'
    try:
        os.stat(fdir)
    except:
        os.mkdir(fdir)
    print('Writing: '+fdir+site+'_ship_exhaust_ml_'+sdate+'_'+edate+'.png')
    fig.tight_layout()
    fig.savefig(fdir+site+'_ship_exhaust_ml_'+sdate+'_'+edate+'.png') 
