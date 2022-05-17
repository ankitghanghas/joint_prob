# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 10:46:36 2022

@author: aghangha
"""
#%%
import netCDF4
import numpy as np
import pandas as pd
import urllib.request

import os
import time

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


os.chdir(r"E:\copula\nwm_outputs\ca")
#os.chdir(r"C:\temp\ankit")

start_time=time.time()
start_date='1980-01-02'
end_date='2020-12-31'

time_list=pd.date_range(start=start_date,end=end_date,freq='H')     #makes a time list with one hour frequency between start and end date.


bucket_name="https://noaa-nwm-retrospective-2-1-pds.s3.amazonaws.com/model_output/"

nhd_con_path=r"E:\copula\nwm\nhd_confluence_gtr_10_ca.csv" # path of file containing COMID (feature ID) list.
nhd_con=pd.read_csv(nhd_con_path)


MAIN_ID=nhd_con.MAIN_ID         #get COMID from the file.
TRIB_ID=nhd_con.TRIB_ID

# df_main_dis=pd.DataFrame(columns=MAIN_ID)
# df_trib_dis=pd.DataFrame(columns=TRIB_ID)

# timestamp=[]

# df_main_dis.insert(0,'timestamp',timestamp)
# df_trib_dis.insert(0,'timestamp',timestamp)



def main_trib_index():
    t=time_list[0]
    time1=t.strftime('%Y%m%d%H')
    f_name="198001010000.CHRTOUT_DOMAIN1.comp"
    key_name=str(t.year)+"/" + f_name
    url_path=bucket_name+key_name
    urllib.request.urlretrieve(url_path,f_name)
    data=netCDF4.Dataset(f_name)  # type: ignore
    COMID_list=data['feature_id'][:].data
    main_index=np.searchsorted(COMID_list,MAIN_ID)  
    trib_index=np.searchsorted(COMID_list,TRIB_ID)
    
    data.close()
    os.remove(f_name)
    
    return (main_index,trib_index)

main_index,trib_index= main_trib_index()


def DailyFlow(df):
    a=df.copy()
    a.timestamp=pd.to_datetime(a.timestamp,format='%Y%m%d%H')
    a=a.set_index('timestamp')
    a=a.resample('D').mean().copy() 
    return a

def df_formation(time_list):
    
    df_main_dis=pd.DataFrame(columns=MAIN_ID)
    df_trib_dis=pd.DataFrame(columns=TRIB_ID)
    
    timestamp=[]
    
    df_main_dis.insert(0,'timestamp',timestamp)
    df_trib_dis.insert(0,'timestamp',timestamp)


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
        #COMID_list=data['feature_id'][:].data   # creates COMID list of all COMID in NWM output file.
        #main_index=np.searchsorted(COMID_list,MAIN_ID)  # finds indices of COMID (in NWM file)= desired feature id (comid) 
        #trib_index=np.searchsorted(COMID_list,TRIB_ID)
    
        main_dis=data['streamflow'][main_index].data # get discharges for all the indices found above
        trib_dis=data['streamflow'][trib_index].data
        #main_dis.insert(0,time1)
        #trib_dis.insert(0,time1)
        main_dis=np.insert(main_dis,0,time1)
        trib_dis=np.insert(trib_dis,0,time1)
        main_dis_row=pd.Series(main_dis,index=df_main_dis.columns)
        trib_dis_row=pd.Series(trib_dis,index=df_trib_dis.columns)
        df_main_dis=df_main_dis.append(main_dis_row,ignore_index=True)
        df_trib_dis=df_trib_dis.append(trib_dis_row,ignore_index=True)
        
        data.close() # close the file, now you can delete it.
        ## try to delete the file.
        
        try :
            os.remove(f_name)
        except OSError as e:
            print("Error : %s - %s." % (e.filename, e.strerror))
            
        if idx % 1440 == 1439:### change this
            
            df_main_dis=DailyFlow(df_main_dis)
            df_trib_dis=DailyFlow(df_trib_dis)
            
            main_name='Main_dis_nwm_'+time1+'.csv'
            trib_name='Trib_dis_nwm_'+time1+'.csv'
            df_main_dis.to_csv(main_name)
            df_trib_dis.to_csv(trib_name)
            
            
            df_main_dis=pd.DataFrame(columns=MAIN_ID)
            df_trib_dis=pd.DataFrame(columns=TRIB_ID)
            
            timestamp=[]
            
            df_main_dis.insert(0,'timestamp',timestamp)
            df_trib_dis.insert(0,'timestamp',timestamp)
            
    df_main_dis=DailyFlow(df_main_dis)
    df_trib_dis=DailyFlow(df_trib_dis)
    main_name='Main_dis_nwm_'+time1+'.csv'
    trib_name='Trib_dis_nwm_'+time1+'.csv'
    df_main_dis.to_csv(main_name)
    df_trib_dis.to_csv(trib_name)




split_time=np.array_split(time_list,8) # splitting into 20 smaller chunks
#%%

split_time[0]=split_time[0][37440:]
split_time[1]=split_time[0][4320:]
split_time[0]=split_time[0][:4320]

split_time[2]=split_time[2][27360:]

split_time[4]=split_time[2][5760:11520]
split_time[5]=split_time[2][11520::]
split_time[2]=split_time[2][0:5670]

split_time=split_time[0:5]
#%%

from multiprocessing import Pool

if __name__ == '__main__':
    with Pool(8) as p:
        p.map(df_formation,split_time)
    print("The time used to execute this is given below")
    end_time = time.time()
    print(end_time - start_time)


# import concurrent.futures as cf

# with cf.ThreadPoolExecutor() as threads:
#    t_res = threads.map(df_formation, split_time)

# import threading

# THREADS = []
# for t_list in split_time:
#     thread=threading.Thread(target=df_formation,args=(t_list))
#     thread.start()
#     THREADS.append(thread)
