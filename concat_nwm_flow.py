# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 15:28:33 2022

@author: aghangha
"""

import numpy as np
import pandas as pd
import math

import os
import datetime as dt


os.chdir(r"E:\copula\nwm_outputs")

main_data_list=['Main_dis_nwm_80_82.csv',
                'Main_dis_nwm_83_84.csv',
                'Main_dis_nwm_85_87.csv',
                'Main_dis_nwm_88_90.csv',
                'Main_dis_nwm_91_93.csv',
                'Main_dis_nwm_94_96.csv',
                'Main_dis_nwm_97_99.csv',
                'Main_dis_nwm_00_02.csv',
                'Main_dis_nwm_03_05.csv',
                'Main_dis_nwm_06_08.csv',
                ]

trib_data_list=['Trib_dis_nwm_80_82.csv',
                'Trib_dis_nwm_83_84.csv',
                'Trib_dis_nwm_85_87.csv',
                'Trib_dis_nwm_88_90.csv',
                'Trib_dis_nwm_91_93.csv',
                'Trib_dis_nwm_94_96.csv',
                'Trib_dis_nwm_97_99.csv',
                'Trib_dis_nwm_00_02.csv',
                'Trib_dis_nwm_03_05.csv',
                'Trib_dis_nwm_06_08.csv',
                ]



def DailyFlow(file_path):
    parser = lambda date: dt.datetime.strptime(date,'%Y%m%d%H' )
    df=pd.read_csv(file_path, parse_dates=[0], date_parser=parser)
    a=df.copy()
    a=a.set_index('timestamp')
    a=a.resample('D').mean().copy()
    
    return a


def Concat(file_list):
    
    for i in range(len(file_list)):
        file_path=file_list[i]
        df=DailyFlow(file_path)
        if i==0:
            conc_df=df.copy()
        else:
            conc_df=pd.concat([conc_df,df])
    
    return conc_df

            
a=Concat(main_data_list)
a.to_csv('Main_dis_nmw_daily_80_08.csv')

a=Concat(trib_data_list)
a.to_csv('Trib_dis_nmw_daily_80_08.csv')



