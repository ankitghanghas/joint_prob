# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 15:13:13 2022

@author: aghangha
"""

import arcpy
import pandas as pd

flowline=r"E:\copula\in_shapefile\nhd\indiana_nhd.shp"
comid_values, length_km, stream_ord,ToNode,drainArea_sqkm =[str(int(row[0])) for row in arcpy.da.SearchCursor(flowline,['COMID'])],[row[0] for row in arcpy.da.SearchCursor(flowline,['LENGTHKM'])],[row[0] for row in arcpy.da.SearchCursor(flowline,['StreamOrde'])],[str(int(row[0])) for row in arcpy.da.SearchCursor(flowline,['ToNode'])],[row[0] for row in arcpy.da.SearchCursor(flowline,['TotDaSqKM'])]
df_stream=pd.DataFrame()
df_stream['COMID']=comid_values; df_stream['LENGTH']=length_km;df_stream['StreamOrder']=stream_ord; df_stream['ToNode']=ToNode;df_stream['DrainArea_sqkm']=drainArea_sqkm 
a=df_stream.ToNode
a=a.values.tolist()
ToNode_confluence=[x for n, x in enumerate(a) if x in a[:n]] ### extracting duplicates in a, duplicate points in toNode are assumed to be confluence points

df_confluence=pd.DataFrame(columns=['MAIN_ID','TRIB_ID','MAINDr_area','TRIBDr_area','DRAIN_ratio','MAIN_str_ord','TRIB_str_ord'])


for node in ToNode_confluence:
   pair=df_stream[df_stream['ToNode']==node]
   if len(pair)>2:
       print("At node :  " + node +"  more than two streams")
       continue
   if pair.DrainArea_sqkm.iloc[0]>pair.DrainArea_sqkm.iloc[1]:
       df_confluence=df_confluence.append({'MAIN_ID' : str(pair.COMID.iloc[0]), 'TRIB_ID':str(pair.COMID.iloc[1]), 'MAINDr_area':pair.DrainArea_sqkm.iloc[0], 'TRIBDr_area':pair.DrainArea_sqkm.iloc[1], 'DRAIN_ratio': pair.DrainArea_sqkm.iloc[0]/pair.DrainArea_sqkm.iloc[1],'MAIN_str_ord': pair.StreamOrder.iloc[0], 'TRIB_str_ord': pair.StreamOrder.iloc[1] }, ignore_index=True)
   
   else:
       df_confluence=df_confluence.append({'MAIN_ID' : str(pair.COMID.iloc[1]), 'TRIB_ID':str(pair.COMID.iloc[0]), 'MAINDr_area':pair.DrainArea_sqkm.iloc[1], 'TRIBDr_area':pair.DrainArea_sqkm.iloc[0], 'DRAIN_ratio': pair.DrainArea_sqkm.iloc[1]/pair.DrainArea_sqkm.iloc[0],'MAIN_str_ord': pair.StreamOrder.iloc[1], 'TRIB_str_ord': pair.StreamOrder.iloc[0] }, ignore_index=True)
           
   

df_confluence.drop(df_confluence[df_confluence.TRIBDr_area<=1].index,inplace=True) ## removing stations where trib area less than 1 sq km
df_confluence.drop(df_confluence[(df_confluence.TRIB_str_ord<2) & (df_confluence.MAIN_str_ord<2)].index,inplace=True) ### removing smaller confluences with both stream order less than 2
df_confluence.drop(df_confluence[(df_confluence.DRAIN_ratio<1.05)].index,inplace=True)
df_confluence.drop(df_confluence[(df_confluence.MAIN_str_ord<df_confluence.TRIB_str_ord)].index,inplace=True) ### dropping points where main stream order is less than tributary stream order.


df_confluence.to_csv(r"E:\copula\nwm\indiana_nhd_confluence_pairs.csv", index=False)