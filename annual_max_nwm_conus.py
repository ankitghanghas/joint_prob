#%%
import pandas as pd

import scipy.stats as st
import os
import datetime as dt
#%%
pd.options.mode.chained_assignment=None
os.chdir(r"E:\copula\nwm_outputs\conus")
#%%
#os.chdir(r"E:\copula\nwm_outputs\ca")

buffer_time=15
#nhd_con_path=r"E:\copula\nwm\conus_nhd_confluence_pairs_gtr10sqkm.csv"
#nhd_con_path=r"E:\copula\nwm\nhd_confluence_gtr_10_ca.csv"
nhd_con_path=r"E:\copula\nwm\conus_confluence_pairs_vupid_gtr10.csv"
pairs=pd.read_csv(nhd_con_path)

pairs.VPUID=pairs.VPUID.astype('str') # because of large datasize, some of these load as int not string
pairs.VPUID=pairs.VPUID.replace(['4','5','6','7','8'],['04','05','06','07','08'])
huc_list=pairs.VPUID.unique()


start_year=1980
end_year=2020

#%%

def buff_cor_dis(i,main_df,trib_df,type):
    if type=='POM':
        #id1=main_idx.index[i]
        #id_cor=pairs[pairs['MAIN_ID']==id1]['TRIB_ID'].values[0]
        id_cor=trib_df.iloc[0].index[i] # my trib_df_index were causing issues as while saving them some converted to decimals

        a=trib_df[str(id_cor)]
        cor_buff=a[(a.index.date>(main_idx[i].date()-dt.timedelta(days=(int(buffer_time//2)+1)))) & (a.index.date<(main_idx[i].date()+dt.timedelta(days=(int(buffer_time//2)+1))))]
        cor_dis=cor_buff.max()
    elif type=='POT':
        #id1=int(trib_idx.index[i])
        #id_cor=pairs[pairs['TRIB_ID']==id1]['MAIN_ID'].values[0]
        id_cor=main_df.iloc[0].index[i]
        a=main_df[str(id_cor)]
        cor_buff=a[(a.index.date>(trib_idx[i].date()-dt.timedelta(days=(int(buffer_time//2)+1)))) & (a.index.date<(trib_idx[i].date()+dt.timedelta(days=(int(buffer_time//2)+1))))]
        cor_dis=cor_buff.max()        

    return cor_dis
#%%
for huc_id in huc_list:
    print(huc_id)
    pairs_1=pairs[pairs.VPUID==huc_id]
    main_focus_df=pd.DataFrame(columns=pairs_1.MAIN_ID)
    main_cor_df=pd.DataFrame(columns=pairs_1.MAIN_ID)
    trib_focus_df=pd.DataFrame(columns=pairs_1.TRIB_ID)
    trib_cor_df=pd.DataFrame(columns=pairs_1.TRIB_ID)

    useful_cols_main=list(pairs_1.MAIN_ID.astype('str'))
    useful_cols_trib=list(pairs_1.TRIB_ID.astype('str'))

    useful_cols_main.insert(0,'timestamp')
    useful_cols_trib.insert(0,'timestamp')

    for year in range(start_year,end_year+1) :
        main_path=str(year)+"_main.csv"
        trib_path=str(year)+"_trib.csv"
        #main_df=pd.read_csv(main_path,parse_dates=[0])
        main_df=pd.read_csv(main_path, usecols=useful_cols_main,parse_dates=[0])
        main_df=main_df.set_index('timestamp')

        #trib_df=pd.read_csv(trib_path,parse_dates=[0])
        trib_df=pd.read_csv(trib_path, usecols=useful_cols_trib,parse_dates=[0])
        trib_df=trib_df.set_index('timestamp')
        main_idx=main_df.idxmax()
        main_focus_dis=main_df.max()
        main_cor_dis=[]
        trib_cor_dis=[]
        trib_idx=trib_df.idxmax()
        trib_focus_dis=trib_df.max()
        for i in range(len(main_idx)):
            main_cor_dis.append(buff_cor_dis(i,type='POM',main_df=main_df,trib_df=trib_df))
            trib_cor_dis.append(buff_cor_dis(i,type='POT',main_df=main_df,trib_df=trib_df))
            # if (len(main_df.loc[trib_idx[i]].shape)>1) & (len(trib_df.loc[main_idx[i]].shape)>1) :
            #     main_cor_dis.append(trib_df.loc[main_idx[i]].iloc[0,i])
            #     trib_cor_dis.append(main_df.loc[trib_idx[i]].iloc[0,i])
            # elif len(main_df.loc[trib_idx[i]].shape)>1:
            #     main_cor_dis.append(trib_df.loc[main_idx[i]][i])
            #     trib_cor_dis.append(main_df.loc[trib_idx[i]].iloc[0,i])
            # elif len(trib_df.loc[main_idx[i]].shape)>1:
            #     main_cor_dis.append(trib_df.loc[main_idx[i]].iloc[0,i])
            #     trib_cor_dis.append(main_df.loc[trib_idx[i]][i])
            
            # else :
            #     main_cor_dis.append(trib_df.loc[main_idx[i]][i])
            #     trib_cor_dis.append(main_df.loc[trib_idx[i]][i])
        main_focus_dis=pd.Series(main_focus_dis.to_list(),index=main_focus_df.columns)
        main_cor_dis=pd.Series(main_cor_dis, index=main_cor_df.columns)
        trib_focus_dis=pd.Series(trib_focus_dis.to_list(),index=trib_focus_df.columns)
        trib_cor_dis=pd.Series(trib_cor_dis, index=trib_cor_df.columns)
        main_focus_df=main_focus_df.append(main_focus_dis,ignore_index=True)
        trib_focus_df=trib_focus_df.append(trib_focus_dis,ignore_index=True)
        main_cor_df=main_cor_df.append(main_cor_dis,ignore_index=True)
        trib_cor_df=trib_cor_df.append(trib_cor_dis,ignore_index=True)
        print(year)


    trib_cor_df.to_csv("trib_cor_df_"+ huc_id +"_15day.csv",index=False)
    main_cor_df.to_csv("main_cor_df_"+ huc_id +"_15day.csv",index=False)
    trib_focus_df.to_csv("trib_focus_df_"+ huc_id +"_15day.csv",index=False)
    main_focus_df.to_csv("main_focus_df_"+ huc_id +"_15day.csv",index=False)

    pairs_1['POM_tau']=''
    pairs_1['POT_tau']=''
    pairs_1['POM_pval']=''
    pairs_1['POT_pval']=''
    for i in range(len(main_idx)):
        tau,p=st.kendalltau(main_focus_df.iloc[:,i],main_cor_df.iloc[:,i])
        tau1,p1=st.kendalltau(trib_focus_df.iloc[:,i],trib_cor_df.iloc[:,i])
        pairs_1['POM_tau'][i]=tau
        pairs_1['POM_pval'][i]=p
        pairs_1['POT_tau'][i]=tau1
        pairs_1['POT_pval'][i]=p1

    pairs_1.to_csv("tau_table_"+ huc_id +"_15day.csv")
    # %%
