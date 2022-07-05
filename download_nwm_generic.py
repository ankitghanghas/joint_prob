# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 10:46:36 2022
@author: aghangha
"""

import netCDF4
import numpy as np
import pandas as pd
import urllib.request

import os
import time

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

## change_this
os.chdir(r"E:\copula\nwm_outputs\ca")



# change_this
start_time=time.time()
start_date='1980-01-02'
end_date='2020-12-31'

time_list=pd.date_range(start=start_date,end=end_date,freq='H')     #makes a time list with one hour frequency between start and end date.


bucket_name="https://noaa-nwm-retrospective-2-1-pds.s3.amazonaws.com/model_output/"

## change_this
nhd_con_path=r"E:\copula\nwm\nhd_confluence_gtr_10_ca.csv" # path of file containing COMID (feature ID) list.
nhd_con=pd.read_csv(nhd_con_path)

# change_this (possibly)
COMID=nhd_con.COMID        #get COMID from the file.


def main_index():  ## gets the index of comid in the NWM stream flow file for all the id in the list COMID above
    t=time_list[0]
    time1=t.strftime('%Y%m%d%H')
    f_name="198001010000.CHRTOUT_DOMAIN1.comp"
    key_name=str(t.year)+"/" + f_name
    url_path=bucket_name+key_name
    urllib.request.urlretrieve(url_path,f_name)
    data=netCDF4.Dataset(f_name)  # type: ignore
    COMID_list=data['feature_id'][:].data
    main_index=np.searchsorted(COMID_list,COMID)
    
    data.close()
    os.remove(f_name)
    
    return (main_index)

comid_index= main_index()


def DailyFlow(df):
    a=df.copy()
    a.timestamp=pd.to_datetime(a.timestamp,format='%Y%m%d%H')
    a=a.set_index('timestamp')
    a=a.resample('D').mean().copy() 
    return a

def df_formation(time_list):
    
    df_main_dis=pd.DataFrame(columns=COMID)
    
    timestamp=[]
    
    df_main_dis.insert(0,'timestamp',timestamp)


    for idx, t in enumerate(time_list):
        time1=t.strftime('%Y%m%d%H')
        f_name=time1+"00.CHRTOUT_DOMAIN1.comp"
        key_name=str(t.year)+"/" + f_name
        url_path=bucket_name+key_name
        
        #coudn't just read file directly into python so i am just downloading it, will remove at the end
        try: 
            urllib.request.urlretrieve(url_path,f_name)
        except urllib.request.HTTPError:  
            continue
        data=netCDF4.Dataset(f_name)    # open the NWM output file.
    
        main_dis=data['streamflow'][comid_index].data # get discharges for all the indices found above
        main_dis=np.insert(main_dis,0,time1)
        main_dis_row=pd.Series(main_dis,index=df_main_dis.columns)
        df_main_dis=df_main_dis.append(main_dis_row,ignore_index=True)
        
        data.close() # close the file, now you can delete it.
        ## try to delete the file.
        
        try :
            os.remove(f_name)
        except OSError as e:
            print("Error : %s - %s." % (e.filename, e.strerror))
            
        if idx % 1440 == 1439:### change_this this will save files every 14000 timesteps (had to do this coz of large file for my data requirements)
            
            df_main_dis=DailyFlow(df_main_dis)
            
            main_name='Main_dis_nwm_'+time1+'.csv'
            df_main_dis.to_csv(main_name)
            
            df_main_dis=pd.DataFrame(columns=COMID)
            
            timestamp=[]
            
            df_main_dis.insert(0,'timestamp',timestamp)

            
    df_main_dis=DailyFlow(df_main_dis)
    main_name='Main_dis_nwm_'+time1+'.csv'
    df_main_dis.to_csv(main_name)

split_time=np.array_split(time_list,8) # splitting into 8 smaller chunks

from multiprocessing import Pool

if __name__ == '__main__':
    with Pool(8) as p:
        p.map(df_formation,split_time)
    print("The time used to execute this is given below")
    end_time = time.time()
    print(end_time - start_time)