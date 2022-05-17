#%%
import pandas as pd
import datetime as dt
import numpy as np
import os


os.chdir(r"E:\copula\nwm_outputs\ca")

start_year=1980
end_year=2021

# def split_last_files(path):
#     parser = lambda date: dt.datetime.strptime(date,'%Y-%m-%d' )
#     df=pd.read_csv(path,parse_dates=[0],date_parser=parser)
#     a=df[df.timestamp.dt.year==(year-1)]
#     b=df[df.timestamp.dt.year==year]
#     if len(a)<1:
#         return
#     a.to_csv((path[:-14]+str(year-1)+"123123.csv"),index=False)
#     b.to_csv(path,index=False)


# for year in range(start_year,end_year):
#     print(year)
#     main_file_path=[f for f in os.listdir(r"E:\copula\nwm_outputs\conus") if f[:4]=="Main" and f[13:17]==str(year)][0]
#     trib_file_path=[f for f in os.listdir(r"E:\copula\nwm_outputs\conus") if f[:4]=='Trib'and f[13:17]==str(year)][0]
#     split_last_files(main_file_path)
#     split_last_files(trib_file_path)


def merge_ends(conc_df,df,hour):
    fraction=hour/24
    if fraction<1.0:
        conc_df.iloc[-1,1:]=conc_df.iloc[-1,1:]*fraction + df.iloc[0,1:]*(1-fraction)
        df=df[1:]
    conc_df=pd.concat([conc_df,df])
    return(conc_df)


def Concat(file_list):
    for i,f in enumerate(file_list):
        parser = lambda date: dt.datetime.strptime(date,'%Y-%m-%d' )
        df=pd.read_csv(f,parse_dates=[0],date_parser=parser)
        if i==0:
            conc_df=df.copy()
        else:
            conc_df=merge_ends(conc_df,df,hour)
        
        hour=int(f[21:23])+1
    
    return conc_df

def super_conc(list1):
    for year in list1:
        print(year)
        main_list=[f for f in os.listdir(r"E:\copula\nwm_outputs\ca") if f[:4]=="Main" and f[13:17]==str(year)]
        trib_list=[f for f in os.listdir(r"E:\copula\nwm_outputs\ca") if f[:4]=='Trib'and f[13:17]==str(year)]
        a=Concat(main_list)
        a.to_csv((str(year)+'_main.csv'),index=False)
        b=Concat(trib_list)
        b.to_csv((str(year)+'_trib.csv'),index=False)

num_worker=8
year_list=[year for year in range(start_year,end_year)]
split_year=np.array_split(year_list,num_worker)

from multiprocessing import Pool

if __name__ == '__main__':
    with Pool(num_worker) as p:
        p.map(super_conc,split_year)
      
