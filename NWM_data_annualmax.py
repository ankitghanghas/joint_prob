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

os.chdir(r"E:\copula\nwm_outputs")


start_date='1980-01-01'
end_date='2020-12-31'

time_list=pd.date_range(start=start_date,end=end_date,freq='H')     #makes a time list with one hour frequency between start and end date.


bucket_name="https://noaa-nwm-retrospective-2-1-pds.s3.amazonaws.com/model_output/"

nhd_con_path=r"E:\copula\nwm\indiana_nhd_confluence_pairs.csv" # path of file containing COMID (feature ID) list.
nhd_con=pd.read_csv(nhd_con_path)

MAIN_ID=nhd_con.MAIN_ID         #get COMID from the file.
TRIB_ID=nhd_con.TRIB_ID

df_main_dis=pd.DataFrame(columns=MAIN_ID)
df_trib_dis=pd.DataFrame(columns=TRIB_ID)

timestamp=[]

df_main_dis.insert(0,'timestamp',timestamp)
df_trib_dis.insert(0,'timestamp',timestamp)


for t in time_list:
    time=t.strftime('%Y%m%d%H')
    f_name=time+"00.CHRTOUT_DOMAIN1.comp"
    key_name=str(t.year)+"/" + f_name
    url_path=bucket_name+key_name
    
    #coudn't just read file directly into python so i am just downloading it, will remove at the end
    try: 
        urllib.request.urlretrieve(url_path,f_name)
    except urllib.request.HTTPError:
        continue
    data=netCDF4.Dataset(f_name)    # open the NWM output file.
    COMID_list=data['feature_id'][:].data   # creates COMID list of all COMID in NWM output file.
    main_index=np.searchsorted(COMID_list,MAIN_ID)  # finds indices of COMID (in NWM file)= desired feature id (comid) 
    trib_index=np.searchsorted(COMID_list,TRIB_ID)

    main_dis=[data['streamflow'][index] for index in main_index] # get discharges for all the indices found above
    trib_dis=[data['streamflow'][index] for index in trib_index]
    main_dis.insert(0,time)
    trib_dis.insert(0,time)
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

df_main_dis.to_csv('Main_dis_nwm.csv', index=False)
df_trib_dis.to_csv('Trib_dis_nwm.csv',index=False)
