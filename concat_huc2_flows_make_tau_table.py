#%%
import pandas as pd
import scipy.stats as st
import os

os.chdir(r"E:\copula\nwm_outputs\conus")
nhd_con_path=r"E:\copula\nwm\conus_confluence_pairs_vupid_gtr10.csv"
pairs=pd.read_csv(nhd_con_path)

pairs['POM_tau']=''
pairs['POT_tau']=''
pairs['POM_pval']=''
pairs['POT_pval']=''
pairs.VPUID=pairs.VPUID.astype('str') # because of large datasize, some of these load as int not string
pairs.VPUID=pairs.VPUID.replace(['4','5','6','7','8'],['04','05','06','07','08'])
huc_list=pairs.VPUID.unique()

#huc_list=['01','02','03N','03S','03W','04','4','5','6','07','7','08','8','09','10U','10L','11','12','13','14','15','16','17']
#%%
for huc_id in huc_list:
    main_focus_path="main_focus_df_"+huc_id+"_15day.csv"
    main_cor_path="main_cor_df_"+huc_id+"_15day.csv"
    trib_focus_path="trib_focus_df_"+huc_id+"_15day.csv"
    trib_cor_path="trib_cor_df_"+huc_id+"_15day.csv"

    trib_cor_df=pd.read_csv(trib_cor_path)
    main_cor_df=pd.read_csv(main_cor_path)
    trib_focus_df=pd.read_csv(trib_focus_path)
    main_focus_df=pd.read_csv(main_focus_path)

    tau_list=[]
    p_list=[]
    tau1_list=[]
    p1_list=[]
    for i in range(len(list(trib_focus_df.columns))):
        tau,p=st.kendalltau(main_focus_df.iloc[:,i],main_cor_df.iloc[:,i])
        tau1,p1=st.kendalltau(trib_focus_df.iloc[:,i],trib_cor_df.iloc[:,i])
        tau_list.append(tau)
        p_list.append(p)
        tau1_list.append(tau1)
        p1_list.append(p1)
    pairs.loc[pairs.MAIN_ID.isin(list(main_focus_df.columns)),'POM_tau']=tau_list
    pairs.loc[pairs.MAIN_ID.isin(list(main_focus_df.columns)),'POM_pval']=p_list
    pairs.loc[pairs.TRIB_ID.isin(list(trib_focus_df.columns)),'POT_tau']=tau1_list
    pairs.loc[pairs.TRIB_ID.isin(list(trib_focus_df.columns)),'POT_pval']=p1_list

pairs.to_csv("tau_table_15day.csv")

pairs=pairs.dropna()
pairs=pairs[(pairs.POM_pval<0.05)&(pairs.POT_pval<0.05)]
pairs.to_csv("tau_table_15day_stat_sig.csv",index=False)
# %%
