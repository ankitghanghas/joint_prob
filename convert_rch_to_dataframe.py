# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 08:27:28 2021

@author: aghangha
"""


import pandas as pd

import os

pd.options.mode.chained_assignment=None

strfile=open (r"C:\Users\aghangha\Documents\copulas\swat_ohiorb\output.txt")
lines=strfile.readlines()

heading=lines[8].split()

reach=[]
day=[]
area=[]
flow_incms=[]
flow_outcms=[]
evp_cms=[]

year=[]
yr=2011
d_1=0
i=0
for line in lines[9:]:
    a=line.split()
    #reach.append(int(a[1])) some error as using this method I am not able to read reach after reach =9999 after that it just shows reach= ****, which is not parsable
    try :
        reach.append(int(a[1]))
        i=int(a[1])
    except ValueError:
        i +=1
        reach.append(i)
        
    day.append(int(a[3]))
    d=int(a[3])
    area.append(float(a[4]))
    flow_incms.append(float(a[5]))
    flow_outcms.append(float(a[6]))
    evp_cms.append(float(a[7]))
    if d_1>d: 
        yr=yr+1
    year.append(yr)
    d_1=d
    
df=pd.DataFrame({'RCH':reach , 'YEAR':year, 'DAY': day, 'AREAkm2':area, 'FLOW_INcms':flow_incms,'FLOW_OUTcms':flow_outcms,'EVAPcms':evp_cms})
df.to_csv("C:\\Users\\aghangha\\Documents\\copulas\\swat_ohiorb\\output_11_14.csv", index=False)