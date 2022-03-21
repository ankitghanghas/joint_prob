#%%
import pandas as pd

import scipy.stats as st
import os
import datetime as dt

pd.options.mode.chained_assignment=None
os.chdir(r"E:\copula\nwm_outputs\conus")

buffer_time=7
nhd_con_path=r"E:\copula\nwm\conus_nhd_confluence_pairs_gtr10sqkm.csv"
pairs=pd.read_csv(nhd_con_path)


start_year=1980
end_year=2020
#%%
main_focus_df=pd.DataFrame(columns=pairs.MAIN_ID)
main_cor_df=pd.DataFrame(columns=pairs.MAIN_ID)
trib_focus_df=pd.DataFrame(columns=pairs.TRIB_ID)
trib_cor_df=pd.DataFrame(columns=pairs.TRIB_ID)


for year in range(start_year,end_year+1) :
    main_path=str(year)+"_main.csv"
    trib_path=str(year)+"_trib.csv"
    main_df=pd.read_csv(main_path,parse_dates=[0])
    main_df=main_df.set_index('timestamp')
    trib_df=pd.read_csv(trib_path,parse_dates=[0])
    trib_df=trib_df.set_index('timestamp')
    main_idx=main_df.idxmax()
    main_focus_dis=main_df.max()
    main_cor_dis=[]
    trib_cor_dis=[]
    trib_idx=trib_df.idxmax()
    trib_focus_dis=trib_df.max()
    for i in range(len(main_idx)):
        main_cor_dis.append(trib_df.loc[main_idx[i]][i])
        trib_cor_dis.append(main_df.loc[trib_idx[i]][i])
    main_focus_dis=pd.Series(main_focus_dis.to_list(),index=main_focus_df.columns)
    main_cor_dis=pd.Series(main_cor_dis, index=main_cor_df.columns)
    trib_focus_dis=pd.Series(trib_focus_dis.to_list(),index=trib_focus_df.columns)
    trib_cor_dis=pd.Series(trib_cor_dis, index=trib_cor_df.columns)
    main_focus_df=main_focus_df.append(main_focus_dis,ignore_index=True)
    trib_focus_df=trib_focus_df.append(trib_focus_dis,ignore_index=True)
    main_cor_df=main_cor_df.append(main_cor_dis,ignore_index=True)
    trib_cor_df=trib_cor_df.append(trib_cor_dis,ignore_index=True)
    print(year)

trib_cor_df.to_csv("trib_cor_df.csv",index=False)
main_cor_df.to_csv("main_cor_df.csv",index=False)
trib_focus_df.to_csv('trib_focus_df.csv',index=False)
main_focus_df.to_csv('main_focus_df.csv',index=False)
# %%
pairs['POM_tau']=''
pairs['POT_tau']=''
pairs['POM_pval']=''
pairs['POT_pval']=''
for i in range(len(main_idx)):
    tau,p=st.kendalltau(main_focus_df.iloc[:,i],main_cor_df.iloc[:,i])
    tau1,p1=st.kendalltau(trib_focus_df.iloc[:,i],trib_cor_df.iloc[:,i])
    pairs['POM_tau'][i]=tau
    pairs['POM_pval'][i]=p
    pairs['POT_tau'][i]=tau1
    pairs['POT_pval'][i]=p1

pairs.to_csv('tau_table.csv')