# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 16:48:46 2022

@author: aghangha
"""

import pandas as pd

import scipy.stats as st
import os
import datetime as dt


pd.options.mode.chained_assignment=None


def main():

    os.chdir(r"E:\copula\nwm_outputs")
    buffer_time=7
    
    
    main_df=pd.read_csv('Main_dis_nmw_daily_80_08.csv',parse_dates=[0])
    main_df=main_df.set_index('timestamp')
    
    trib_df=pd.read_csv('Trib_dis_nmw_daily_80_08.csv',parse_dates=[0])
    trib_df=trib_df.set_index('timestamp')
    
    pairs=pd.read_csv(r"E:\copula\nwm\indiana_nhd_confluence_pairs.csv")
    
    
    df=pd.DataFrame(columns=['RCH','POM_tau','POT_tau', 'POM_pval', 'POT_pval','Main_mean_flow', 'Trib_mean_flow', 'DRAIN_ratio', 'MAINDr_area','TRIBDr_area']);
    
    for i in range(len(pairs)):
        main_id=pairs['MAIN_ID'][i]
        trib_id=pairs['TRIB_ID'][i]
        
        try:
            main_data=main_df[str(main_id)]
            trib_data=trib_df[str(trib_id)]
        except:
            continue
        
        start_year=1980
        end_year=2008
        
        main_focus_dis=[]
        main_cor_dis=[]
        trib_focus_dis=[]
        trib_cor_dis=[]
    
        ms_mean_flow=main_data.mean()
        ts_mean_flow=trib_data.mean()
        
        for year in range(start_year,end_year+1):
            ab=main_data[main_data.index.year==year]
            cd=trib_data[trib_data.index.year==year]
    
            
            a=ab[ab==ab.max()]
            if len(a)>0: #### in case i get more than one max values, I just choose first value
                a=a.head(1)
            main_focus_dis.append(a.values[0])
            trib_buff=cd[(cd.index.date>(a.index.date-dt.timedelta(days=(int(buffer_time//2)+1)))) & (cd.index.date<(a.index.date+dt.timedelta(days=(int(buffer_time//2)+1))))]
            main_cor_dis.append(trib_buff.max())
            
            b=cd[cd==cd.max()]
            if len(b)>0:
                b=b.head(1)
            trib_focus_dis.append(b.values[0])
            main_buff=ab[(ab.index.date>(b.index.date-dt.timedelta(days=(int(buffer_time//2)+1)))) & (ab.index.date<(b.index.date+dt.timedelta(days=(int(buffer_time//2)+1))))]
            trib_cor_dis.append(main_buff.max())
            
        tau,p = st.kendalltau(main_focus_dis,main_cor_dis);
        tau1,p1 = st.kendalltau(trib_focus_dis,trib_cor_dis);
        
        DRAIN_ratio=pairs.DRAIN_ratio[i]
        MAINDr_area=pairs['MAINDr_area'][i]
        TRIBDr_area=pairs['TRIBDr_area'][i]
        
        df=df.append({'RCH': main_id,'POM_tau':tau,'POT_tau':tau1, 'POM_pval':p, 'POT_pval':p1, 'Main_mean_flow':ms_mean_flow,'Trib_mean_flow':ts_mean_flow, 'DRAIN_ratio':DRAIN_ratio,'MAINDr_area':MAINDr_area,'TRIBDr_area':TRIBDr_area},ignore_index=True)
        
    df.to_csv('tau_with_DA_ratio_80_08_AMax.csv')
    a=df[(df.POM_pval<0.05) & (df.POT_pval<0.05)]
    a.to_csv('tau_with_DA_ratio_80_08_AMax_statistically_sig.csv')

if __name__ == "__main__":
    main()
    
            
            