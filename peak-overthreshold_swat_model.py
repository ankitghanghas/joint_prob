# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 10:50:26 2021

@author: aghangha
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import scipy.stats as st
from scipy.signal import find_peaks


pd.options.mode.chained_assignment=None


def main(): 
    pairs = pd.read_csv(r"C:\Users\aghangha\Documents\copulas\swat_ohiorb\confluence_pairs_IN.csv")
    data = pd.read_csv(r"C:\Users\aghangha\Documents\copulas\swat_ohiorb\output_11_14.csv")
    
    #buffer_time=7   #7 days buffer period
    
    df=pd.DataFrame(columns=['RCH','POM_tau','POT_tau', 'POM_pval', 'POT_pval', 'POM_no_pairs', 'POT_no_pairs','Main_mean_flow', 'Trib_mean_flow']);
    
    for i in range(len(pairs)):
        main_id=pairs['MAIN_ID'][i]
        trib_id=pairs['TRIB_ID'][i]
    
        main_data=data[data['RCH']==main_id].copy()
        trib_data=data[data['RCH']==trib_id].copy()
        ms_mean_flow=main_data.FLOW_OUTcms.mean()
        ts_mean_flow=trib_data.FLOW_OUTcms.mean()
        
        if (ms_mean_flow==0) | (ts_mean_flow==0):
            i+=1
        else:    

    #        start_year=2011
    #        end_year = 2014
            
            main_focus_dis=[]
            main_cor_dis=[]
            trib_focus_dis=[]
            trib_cor_dis=[]
            
            
            threshold_diff=main_data.FLOW_OUTcms.mean() + 3*main_data.FLOW_OUTcms.std()
            peaks,_ =find_peaks(main_data['FLOW_OUTcms'],prominence=threshold_diff) # set the prominence (difference between peak and its nearest lowest point) as 50 cfs or 1.4 cms
            if len(peaks)<15: ### makes sure I get atleat 99 percentile flows.
                peaks,_ =find_peaks(main_data['FLOW_OUTcms'],prominence=0.5*threshold_diff)
            ab=main_data.iloc[peaks[:]]
            ab=ab.sort_values(['YEAR','DAY'])
            buffer_time=int(np.log(ab.AREAkm2/(1.6*1.6)).iloc[0]+5) ## I am defining my own buffer time based on the size of the drainage area. ## see paper by Claps 2003 Can continuous streamflow data support FFA
            a=[]
            ### makes sure that the events are independent and sufficiently far away
            a=(abs(ab.DAY.iloc[1:].values-ab.DAY.iloc[:-1].values)-buffer_time)
            b=[x for (x,j) in enumerate(a) if j<=0]
            add=0
            for idx in b:
                                      ##### 
                if ab.YEAR.iloc[(idx-add)]==ab.YEAR.iloc[(idx-add)+1]:
                    if ab.FLOW_OUTcms.iloc[(idx-add)]>ab.FLOW_OUTcms.iloc[(idx-add)+1]:
                        ab=ab.drop(index=ab.index[idx-add])
                    else:
                        ab=ab.drop(index=ab.index[(idx-add)+1])
                    add+=1                    
                    
            # ab=ab.sort_values(by='FLOW_OUTcms', ascending=False)
            # if len(peaks)>15: # this ensure that at max we only choose 99th percentile flow, not all the minute peaks.
            #     ab=ab[:15]
            main_focus_dis=ab.FLOW_OUTcms.values
            n1=len(ab)
            cors_buffer=min(7,int(np.log(trib_data.AREAkm2/(1.6*1.6)).iloc[0]+5))
            for ij in range (n1):
                trib_buff=trib_data[trib_data['YEAR']==ab.YEAR.iloc[ij]]
                trib_buff=trib_buff[(trib_buff['DAY']>=(ab.DAY.iloc[ij]-int(cors_buffer/2))) & (trib_buff['DAY']<=(ab.DAY.iloc[ij]+int(cors_buffer/2)))]
                main_cor_dis.append(trib_buff.FLOW_OUTcms.max())
            
            tau,p = st.kendalltau(main_focus_dis,main_cor_dis);
            
            
            ts_mean_flow=trib_data.FLOW_OUTcms.mean()
            threshold_diff=trib_data.FLOW_OUTcms.mean() + 3*trib_data.FLOW_OUTcms.std()
            peaks,_ =find_peaks(trib_data['FLOW_OUTcms'],prominence=threshold_diff)
            if len(peaks)<15:
                peaks,_ =find_peaks(trib_data['FLOW_OUTcms'],prominence=0.5*threshold_diff)
            cd=trib_data.iloc[peaks[:]]
            cd=cd.sort_values(['YEAR','DAY'])
            buffer_time=int(np.log(cd.AREAkm2/(1.6*1.6)).iloc[0]+5) ## I am defining my own buffer time based on the size of the drainage area. ## see paper by Claps 2003 Can continuous streamflow data support FFA
            a1=[]
            ### makes sure that the events are independent and sufficiently far away
            a1=(abs(cd.DAY.iloc[1:].values-cd.DAY.iloc[:-1].values)-buffer_time)
            b1=[x1 for (x1,j1) in enumerate(a1) if j1<=0]
            add=0
            for idx in b1:       ##### 
                if cd.YEAR.iloc[(idx-add)]==cd.YEAR.iloc[(idx-add)+1]:
                    if cd.FLOW_OUTcms.iloc[(idx-add)]>cd.FLOW_OUTcms.iloc[(idx-add)+1]:
                        cd=cd.drop(index=cd.index[(idx-add)])
                    else:
                        cd=cd.drop(index=cd.index[(idx-add)+1])
                    add+=1
            
            # cd=cd.sort_values(by='FLOW_OUTcms', ascending=False)
            # if len(peaks)>15:
            #     cd=cd[:15]a1
            trib_focus_dis=cd.FLOW_OUTcms.values
            n2=len(cd)
            cors_buffer=min(7,int(np.log(main_data.AREAkm2/(1.6*1.6)).iloc[0]+5))
            for ij in range (n2):
                main_buff=main_data[main_data['YEAR']==cd.YEAR.iloc[ij]]
                main_buff=main_buff[(main_buff['DAY']>=(cd.DAY.iloc[ij]-int(cors_buffer/2))) & (main_buff['DAY']<=(cd.DAY.iloc[ij]+int(cors_buffer/2)))]
                trib_cor_dis.append(main_buff.FLOW_OUTcms.max())
                
            tau1,p1 = st.kendalltau(trib_focus_dis,trib_cor_dis);
            
            
                
                
                
            
            #####this is for top 15 peak over threshold - 99th percentile.
    #         ab=main_data.sort_values(by='FLOW_OUTcms', ascending=False)
    #         cd=trib_data.sort_values(by='FLOW_OUTcms', ascending=False)
    #         for ij in range(15):
    #             a=ab.iloc[ij,:]
    #             main_focus_dis.append(a.FLOW_OUTcms)
    #             trib_buff=cd[cd['YEAR']==a.YEAR]
    #             trib_buff=trib_buff[(trib_buff['DAY']>=(a.DAY-int(buffer_time/2))) & (trib_buff['DAY']<=(a.DAY+int(buffer_time/2)))]
    #             main_cor_dis.append(trib_buff.FLOW_OUTcms.max())
                
    #             b=cd.iloc[ij,:]
    #             trib_focus_dis.append(b.FLOW_OUTcms)
    #             main_buff=ab[ab['YEAR']==b.YEAR]
    #             main_buff=main_buff[(main_buff['DAY']>=(b.DAY-int(buffer_time/2))) & (main_buff['DAY']<=(b.DAY+int(buffer_time/2)))]
    #             trib_cor_dis.append(main_buff.FLOW_OUTcms.max())
                
                
                
    # #        for year in range(start_year,end_year+1):
    # #            ab=main_data[main_data['YEAR']==year]
    # #            cd=trib_data[trib_data['YEAR']==year]
    # #            a=ab[ab.FLOW_OUTcms==ab.FLOW_OUTcms.max()]
    # #            main_focus_dis.append(a.FLOW_OUTcms.values[0])
    # #            trib_buff=cd[(cd['DAY']>=(a.DAY.values[0]-int(buffer_time/2))) & (cd['DAY']<=(a.DAY.values[0]+int(buffer_time/2)))]
    # #            main_cor_dis.append(trib_buff[trib_buff.FLOW_OUTcms==trib_buff.FLOW_OUTcms.max()].FLOW_OUTcms.values[0])
    # #                
    # #            b=cd[cd.FLOW_OUTcms==cd.FLOW_OUTcms.max()]
    # #            trib_focus_dis.append(b.FLOW_OUTcms.values[0])
    # #            trib_cor_dis.append(ab[ab['DAY']==b.DAY.values[0]].FLOW_OUTcms.values[0])
            
    #         tau,p = st.kendalltau(main_focus_dis,main_cor_dis);
    #         tau1,p = st.kendalltau(trib_focus_dis,trib_cor_dis);
            
            df=df.append({'RCH': main_id,'POM_tau':tau,'POT_tau':tau1, 'POM_pval':p, 'POT_pval':p1, 'POM_no_pairs':n1, 'POT_no_pairs':n2, 'Main_mean_flow':ms_mean_flow,'Trib_mean_flow':ts_mean_flow},ignore_index=True)
    
    drain_ratio=pairs['MAINDr_area']/pairs['TRIBDr_area']
    df['DRAIN_ratio']=drain_ratio
    df['MAINDr_area']=pairs.MAINDr_area
    df['TRIBDr_area']=pairs.TRIBDr_area
    
    
    df.to_csv("C:\\Users\\aghangha\\Documents\\copulas\\swat_ohiorb\\tau_table_sim_IN_peaks_custom_threshold_n_corrected_buffer.csv",index=False)

if __name__ == "__main__":
    main()


# a=np.log(ab.AREAkm2/(1.6*1.6)).iloc[0]+5
# abc=ab.sort_values(by='YEAR')
# a=(abs(abc.DAY.iloc[1:].values-abc.DAY.iloc[:-1].values)-a)
# b=[x for (x,j) in enumerate(a) if j<=0]

