import numpy as np
import datetime
import warnings
import os
import pandas as pd
import logging
import pytz
from scipy.fftpack import fft, rfft,rfftfreq
import matplotlib.pyplot as plt

from dqlib.utils.network_utils import send_mail_html
from dqlib.utils.utils import DatastreamParser 
from dqlib.utils.db_utils import send_test_results as send
from dqlib.utils.utils import SolarCalc
from dqlib.utils.qc_utils import add_qc_bit,get_qc_info
from dqlib.io.image import save_plot

variable='diffuse_hemisp_narrowband_filter4'
#Set up windows and options for processing
del_t=1. #1-hour windows
nh=24. #Span 24 hours
n_window=int(nh/del_t) #Number of windows
nc=4. #Number of Columns
nr=nh/nc/del_t # Number of rows needed
dt=20. #Seconds between time steps

def shading_detection(filename,dq_object):
    '''Algorithm to detect shading problems based on an FFT method for a full day
       Note, this has not been updated to work with X-Array format yet
    '''

    #Get the metadata needed for processing
    params = DatastreamParser(filename, armfile=True, suppress=True)
    datastream = params.datastream_standard
    date = params.date
    site=params.site
    platform=params.datastream_class

    #Get data and time 
    data=dq_object[variable].data

    #Open plot
    fig=plt.figure()

    #Pass data to FFT analysis script
    result=fft_shading_test(data,'day')

    #Ssve plot
    fdir=os.environ['DQPLOT_DATA']+'/'+site+'/'+site+platform+'/'+date+'/'
    imagename=datastream+'.shading_fft.'+date+'.png'
    save_plot(fig,fdir,imagename)

    return result

def shading_detection_window(filename,dq_object):
    '''Function to Review Shading Detection in 1-Hour windows
       Note, this has not been updated to work with X-Array format yet
    '''
    #Get the metadata needed for processing
    params = DatastreamParser(filename, armfile=True, suppress=True)
    datastream = params.datastream_standard
    date = params.date
    site=params.site
    platform=params.datastream_class

    #Get Sunrise and Sunset data so we don't process on nighttime data
    lat=dq_object.lat
    lon=dq_object.lon
    solar_obj=SolarCalc([date],lat,lon)
    sr=solar_obj.sunrise
    ss=solar_obj.sunset
 
    #Get time
    time=dq_object.py_datetimes

    #Remove data from sunset to sunrise
    ss=ss[0].replace(tzinfo=None)
    sr=sr[0].replace(tzinfo=None)
    date_dt=datetime.datetime.strptime(date,'%Y%m%d')
    if sr.day > date_dt.day:
        sr=sr-datetime.timedelta(days=1)
    if ss.day > date_dt.day:
        ss=ss-datetime.timedelta(days=1)
    idx=(time > sr)|(time < ss)
    index=np.where(idx)
    data=dq_object.get_variable(variable).data
    time=time[index]
    data=data[index]

    #Get date components
    day=time[0].day
    month=time[0].month
    year=time[0].year

    #Create Figure
    fig=plt.figure(figsize=(15,10))
    plt.subplots_adjust(hspace=.4,right=0.95,left=0.05,top=0.975,bottom=0.05)

    #Run through each hourly window and compute the FFT
    shading=[]
    for i in range(n_window):
        sr=datetime.datetime(year,month,day,i,0,0)
        er=datetime.datetime(year,month,day,i,59,59)
  
        idx=(time >= sr)*(time <= er)
        index=np.where(idx)
        ax=fig.add_subplot(nr,nc,i+1)
        #Function to calculate FFT
        result=fft_shading_test(data[index],'window',[sr,er])
        shading.append(result)

    #Write Image
    fdir=os.environ['DQPLOT_DATA']+'/'+site+'/'+site+platform+'/'+date+'/'
    imagename=datastream+'.shading_fft_window.'+date+'.png'                            
    save_plot(fig,fdir,imagename)
    return shading 

def shading_detection_point(filename,dq_object):
    '''Function to Review Shading Detection based on each point'''
    #Get the metadata needed for processing
    params = DatastreamParser(filename, armfile=True, suppress=True)
    date = params.date
    platform=params.datastream_class
    site = params.site
    facility = params.facility
    level = params.level
    if 'mfrsr' in platform:
        platform = 'mfrsr'
    ds = ''.join([site,platform,facility,'.',level])

    #Get Sunrise and Sunset data so we don't process on nighttime data
    lat=dq_object.lat.data
    lon=dq_object.lon.data
    solar_obj=SolarCalc([date],lat,lon)
    sr=solar_obj.sunrise
    ss=solar_obj.sunset

    #Get time
    #time=dq_object.py_datetimes
    time=dq_object.time.data

    #Get date components - Need to convert XARRAY 64 time to datetime to get components
    dummy=pd.to_datetime([time[0]])
    date64=np.datetime64(dummy.date[0],'s')

    #Remove data from sunset to sunrise
    if isinstance(ss[0],datetime.datetime):
        ss=ss[0].replace(tzinfo=None)
        sr=sr[0].replace(tzinfo=None)
        date_dt=datetime.datetime.strptime(date,'%Y%m%d')
        if sr.day > date_dt.day:
            sr=sr-datetime.timedelta(days=1)
        if ss.day > date_dt.day:
            ss=ss-datetime.timedelta(days=1)
        sr=np.datetime64(sr)
        ss=np.datetime64(ss)
    else:
        sr = date64
        ss = date64+np.timedelta64(1,'D')
    data=dq_object[variable].data

    #Create Figure
    fig=plt.figure(figsize=(15,10))
    plt.subplots_adjust(hspace=.4,right=0.95,left=0.05,top=0.975,bottom=0.05)
    ax=fig.add_subplot(nr,nc,1)

    #Compute teh FFT for each point +- x samples
    sp=0
    wind=30
    newp=1
    shading=[]
    sr=date64
    er=date64+np.timedelta64(59*60+59,'s')
    for t in range(len(time)):

        idx=(time[t] > sr)|(time[t] < ss)
        if idx is False:
           shading.append(0)
           continue
        sind=t-wind
        eind=t+wind
        if sind < 0: 
            sind=0
        if eind > len(time):
            eind=len(time)
        if sp == 24:
           break
        while time[t] > er:
            sp+=1
            if sp == 24:
               break
            ax=fig.add_subplot(nr,nc,sp+1)
            sr=date64+np.timedelta64(sp,'h')
            er=sr+np.timedelta64(59*60+59,'s')
            ax.set_title(''.join([str(pd.to_datetime(sr).strftime('%H%M')),
                ' - ',str(pd.to_datetime(er).strftime('%H%M'))]))

        d=data[sind:eind]

        result=fft_shading_test(d,'point',[sr,er]) #Function to calculate FFT
        shading.append(result)

    shading=np.array(shading)

    #Write data to QC variable if more than 5 points tripped
    idx=(shading == 1)
    index=np.where(idx)[0]
 
    testname='Shading detected within '+str(wind)+' samples'
    if len(index) > 5:
        add_qc_bit(dq_object,variable,index,testname,assessment='Bad')

    #Write Image
    fdir=os.environ['DQPLOT_DATA']+'/'+site+'/'+site+platform+'/'+date
    imagename=ds+'.shading_fft_point.'+date+'.png'
    save_plot(fig,fdir,imagename)
    return shading 

def fft_shading_test(data,method,timerange=[]):
    '''Function that calculates shading/no shading based on the data passed in
    '''
    
    #Set up and remove missing data
    shading=0
    idx=(data != -9999.)
    index=np.where(idx)
    data=data[index]
 
    #Plot data in previously opened  plot and return if no data
    if len(data) == 0:
        plt.plot([0],[0],'-',linewidth=1.5,color='r')
        if len(timerange) > 0:
            ax=plt.gca()
            ax.set_title(''.join([str(pd.to_datetime(timerange[0]).strftime('%H%M')),
                ' - ',str(pd.to_datetime(timerange[1]).strftime('%H%M'))]))
        return shading

    #Set up method specific thresholds and variables
    warnings.filterwarnings("ignore",category =RuntimeWarning)
    ratio_thresh=2.
    if method is 'day':
        shad_freq_l=[0.0091,0.01825]
        shad_freq_u=[0.0095,0.0185]

        #FFT Algorithm
        fftv=rfft(data)
        freq=rfftfreq(fftv.size,d=20)

        wind=10
        image_sub='shading_fft'

    if method is 'point':
        shad_freq_l=[0.008,0.017]
        shad_freq_u=[0.0105,0.0195]

        #FFT Algorithm
        fftv=abs(rfft(data))
        freq=rfftfreq(fftv.size,d=20)

        idx=(fftv < 1.)
        index=np.where(idx)
        fftv=fftv[index] 
        freq=freq[index]
        wind=3
        ratio_thresh=3.75
        image_sub='shading_fft_point'

    if method is 'window':
        shad_freq_l=[0.0088,0.01805,0.02175]
        shad_freq_u=[0.010,0.01925,0.02275]

        #FFT Algorithm
        fftv=abs(rfft(data))
        freq=rfftfreq(fftv.size,d=20)

        idx=(fftv < 1.)
        index=np.where(idx)
        fftv=fftv[index] 
        freq=freq[index]
        wind=5
        image_sub='shading_fft_window'

    #Get a 3 point running mean
    if len(fftv) == 0:
         return 0
    fftv=pd.DataFrame(data=fftv).rolling(min_periods=3,window=3,center=True).mean().values.flatten()
    

    #Plot data out 
    plt.plot(freq,fftv,'-',linewidth=1.5,color='k')
    ax=plt.gca()
 
    ratio=[]
    #Calculates the ratio (size) of the peaks in the FFT to the surrounding 
    #data 
    for i in range(len(shad_freq_l)):
        idx=np.logical_and(freq > shad_freq_l[i],freq < shad_freq_u[i])
        plt.plot(freq[idx],fftv[idx],'-',linewidth=1.5,color='r')

        index=np.where(idx)
        if len(index[0]) == 0:
            continue
        peak=max(fftv[index])
        index=index[0]

        sind=index[0]-wind
        if sind < 0:
            sind=0
        eind=index[-1]+wind
        if eind > len(fftv):
            eind=len(fftv)

        if len(range(sind,index[0])) == 0 or len(range(index[-1],eind)) == 0:
            ratio.append(0.0)
        else:
            peak_l=max(fftv[range(sind,index[0])])
            peak_r=max(fftv[range(index[-1],eind)])
            ratio.append(peak/np.mean([peak_l,peak_r]))

        if len(fftv) > 60:
            ax.text(shad_freq_l[i], peak*1.1, '{:.2}'.format(ratio[-1]),
                color='red',fontsize=10)
        
    #Checks ration against thresholds
    shading=0
    if len(ratio) > 0:
        pass1=False
        pass2=False
        pass3=False
        if ratio[0] > ratio_thresh:
            pass1=True   
        if len(ratio) > 1:
            if ratio[1] > 1.2:
                pass2=True
        else:
            pass2=True
        if len(ratio) > 2:
            if ratio[2] > 1.2:
                pass3=True
        else:
            pass3=True
        if pass1 and pass2 and pass3:
            ax.text(0.75, 0.925,'Shading Detected',horizontalalignment='center',
               verticalalignment='center',transform = ax.transAxes, color='red')
            shading=1
    if np.nanmax(fftv) >0 :
        ax.set_yscale('log')
    if len(timerange) > 0:
        ax.set_title(''.join([str(pd.to_datetime(timerange[0]).strftime('%H%M')),' - ',
            str(pd.to_datetime(timerange[1]).strftime('%H%M'))]))

    return shading

def fft_email(filename,method):
    '''Function to send an email if shading is detected'''
    #Get the metadata needed for processing
    params = DatastreamParser(filename, armfile=True, suppress=True)
    datastream = params.datastream_standard
    date = params.date
    site=params.site
    platform=params.datastream_class
    facility=params.facility
    level=params.level
    dummy=os.environ['DQPLOT_DATA']
    usr=dummy.split('/')[3]
    if 'tool' in dummy:
        pre='http://plot.dmf.arm.gov/PLOTS/'+site.upper()
    else:
        pre='http://dev.arm.gov/~'+usr+'/data/tool/dq/'+site

    body=''.join(['Please review the data for ',
        '<a href="http://dq.arm.gov/dq-explorer/cgi-bin/main/plots?source=',
        site+'.mfrsr.'+facility+'.'+level+'.'+date+'">',
        site+platform+facility+' on '+date+'</a><br />',
        'Additional information can be found at '])

    for i in range(len(method)):
        if method[i] is 'day':
            image_sub='shading_fft'
            title='Daily '
        if method[i] is 'point':
            image_sub='shading_fft_point'
            title='Point '
        if method[i] is 'window':
            image_sub='shading_fft_window'   
            title='Hourly '
        body+=''.join(['<a href="'+pre+'/'+site+'mfrsr/',
            date+'/'+site+'mfrsr'+facility+'.b1.'+image_sub+'.'+date,
            '.png">'+title+' FFT Plot</a>'])
    subject=site.upper()+facility.upper()+' Shading Detected on '+date
    send(datastream,'shading_fft',date,subject,body)
