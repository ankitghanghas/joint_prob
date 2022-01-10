# -*- coding: utf-8 -*-
"""
Created on Wed May  5 11:27:39 2021

@author: aghangha
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import scipy.stats as st


pd.options.mode.chained_assignment=None


def main(): 
    pairs = pd.read_csv(r"C:\Users\aghangha\Documents\copulas\swat_ohiorb\confluence_pairs_IN.csv")
    data = pd.read_csv(r"C:\Users\aghangha\Documents\copulas\swat_ohiorb\output_11_14.csv")
    
    buffer_time=7
    
    df=pd.DataFrame(columns=['RCH','POM_tau','POT_tau']);
    ######this is for annual maxima, not peak over threshold
    for i in range(len(pairs)):
        main_id=pairs['MAIN_ID'][i]
        trib_id=pairs['TRIB_ID'][i]
    
        main_data=data[data['RCH']==main_id].copy()
        trib_data=data[data['RCH']==trib_id].copy()
        
        start_year=2011
        end_year = 2014
        
        main_focus_dis=[]
        main_cor_dis=[]
        trib_focus_dis=[]
        trib_cor_dis=[]
        for year in range(start_year,end_year+1):
            ab=main_data[main_data['YEAR']==year]
            cd=trib_data[trib_data['YEAR']==year]
            a=ab[ab.FLOW_OUTcms==ab.FLOW_OUTcms.max()]
            main_focus_dis.append(a.FLOW_OUTcms.values[0])
            trib_buff=cd[(cd['DAY']>=(a.DAY.values[0]-int(buffer_time/2))) & (cd['DAY']<=(a.DAY.values[0]+int(buffer_time/2)))]
            main_cor_dis.append(trib_buff[trib_buff.FLOW_OUTcms==trib_buff.FLOW_OUTcms.max()].FLOW_OUTcms.values[0])
                
            b=cd[cd.FLOW_OUTcms==cd.FLOW_OUTcms.max()]
            trib_focus_dis.append(b.FLOW_OUTcms.values[0])
            trib_cor_dis.append(ab[ab['DAY']==b.DAY.values[0]].FLOW_OUTcms.values[0])
        
        tau,p = st.kendalltau(main_focus_dis,main_cor_dis);
        tau1,p = st.kendalltau(trib_focus_dis,trib_cor_dis);
        
        df=df.append({'RCH': main_id,'POM_tau':tau,'POT_tau':tau1},ignore_index=True)
    
    drain_ratio=pairs['MAINDr_area']/pairs['TRIBDr_area']
    df['DRAIN_ratio']=drain_ratio
    df['MAINDr_area']=pairs.MAINDr_area
    df['TRIBDr_area']=pairs.TRIBDr_area
    
    
    df.to_csv("C:\\Users\\aghangha\\Documents\\copulas\\swat_ohiorb\\tau_table_sim_IN.csv")

if __name__ == "__main__":
    main()
    

    
x=df.DRAIN_ratio
y1=df.POM_tau
y2=df.POT_tau
ax=df.plot.scatter(x="DRAIN_ratio",y="POM_tau",marker='o', c='none', edgecolors="DarkBlue", label="Peak on Mainstream")
ax1=df.plot.scatter(x="DRAIN_ratio",y="POT_tau",marker='v', c='none',edgecolors="DarkRed",label="Peak on Tributary",ax=ax)
ax.set_xscale('log')
plt.xlabel("Drainage Area Ratio")
plt.ylabel("Kendall's Tau")
plt.title("Kendall's Tau variation with Drainage Area Ratio (Wabash Basin)")

