# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 08:19:49 2020

@author: aghangha
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import scipy.stats as st

pd.options.mode.chained_assignment=None

#mainlist=['03245500', '03227500','03229610','03271500','03270500','03263000']
#triblist=['03247500', '03229500','03229796','03272000','03271000','03266000']


mainlist=['04094000','04092677','03330500','03334000','05522500','03340500','03342000','03378500','03373500','03350500','03353500','03353800']
triblist=['04094400','04092750','03331224','03334500','05523865','03341300','03342500','03378550','03373508','03349000','03353600','03353910']
colnames=['agency_cd','site_no','datetime','discharge','dis_qual','timezone']





def distribution(discharge,pp):
    typofEx=[]
    dpara=[]
    x =discharge.values
    x.sort()
    D=[];p=[];
    # KS test
    pnorm=st.norm.fit(x)
    Dval,pval = st.kstest(x,'norm',pnorm)
    D.append(Dval);p.append(pval);
    TLog=np.log(x)
    TmeanL=TLog.mean()
    TstdL=TLog.std()
    TskewL=st.skew(TLog)
    z=st.norm.ppf(pp)
    Q=np.power(math.e,TmeanL+TstdL*z)
    Dval,pval=st.ks_2samp(Q,x)
    D.append(Dval);p.append(pval);
    plog=(TmeanL,TstdL)
    ppear=st.pearson3.fit(x)
    Dval,pval = st.kstest(x,'pearson3', ppear)
    D.append(Dval);p.append(pval);
    
    #log pearson type 3 (LP3)
    plpear=st.pearson3.fit(TLog)
    if plpear[0]<0: #handle negative skewness case specially to avoid inverting of CDF (getting a reverse CDF)
        y=(1-st.pearson3.cdf(np.log(x),plpear[0],plpear[1],plpear[2]))
    else :
        y=st.pearson3.cdf(np.log(x),plpear[0],plpear[1],plpear[2])
    Dval,pval = st.ks_2samp(y, pp)
    D.append(Dval); p.append(pval)
    
    # print(Dval)
    # print(p)
    idx=D.index(min(D))
    if idx == 0:
        dpara.append(pnorm)
        typofEx.append('Normal')
    elif idx == 1:
        dpara.append(plog)
        typofEx.append('LogNormal')
    elif idx == 2:
        dpara.append(ppear)
        typofEx.append('pearson3')
    elif idx == 3:
        dpara.append(plpear)
        typofEx.append('LP3')
    # lb=['Original CDF','Lognormal','Normal','Pearson 3', 'LP3']
    # plt.figure()
    # plt.plot(x,pp,'r-', x,st.norm.cdf(np.log(x),plog[0],plog[1]) ,'b--', x, st.norm.cdf(x,pnorm[0],pnorm[1]),'g--', x,st.pearson3.cdf(x,ppear[0],ppear[1],ppear[2]),'y--',x,y,'r--')
    # plt.legend((lb[0], lb[1], lb[2],lb[3], lb[4]),loc='lower right')
    # plt.xlabel('Discharge (cfs)')
    # plt.ylabel('Cummulative Frequency')
    # plt.show()
    return dpara, typofEx


def plottingposition(discharge,formula_name='Cunnane'):
    x=discharge.sort_values()
    N=len(x)
    rank=np.arange(1,N+1)
    if formula_name=='Weibull':
        a= 0
    elif formula_name=='Hazen':
        a=0.5
    elif formula_name=='Blom':
        a=3/8
    elif formula_name=='Gringorten':
        a=0.44
    elif formula_name=='Cunnane':
        a=0.4
    pp=(rank-a)/(N+1-2*a)
    return pp


for zi in range(len(mainlist)):
    tribc_path = 'C:/Users/aghangha/Documents/copulas/trib/daily_'+triblist[zi] + '.csv'
    mainc_path = 'C:/Users/aghangha/Documents/copulas/main/daily_'+mainlist[zi] + '.csv'
    tribc=pd.read_csv(tribc_path, sep=',', names=colnames, skiprows=1, header=None)
    mainc=pd.read_csv(mainc_path, sep=',', names=colnames, skiprows=1, header=None)
    df_list=[mainc,tribc]
    idx=0
    pp={}
    annual_max=[];
    try:
        for df in df_list:
            df.index=pd.to_datetime(df.datetime)
            df=df[df['discharge'].notnull()]
            a=df.sort_values(by='discharge', ascending=False)
            threshold_index=round(0.01*a.shape[0])      #peak over threshold, assuming 99the percentile peaks on daily flow
            a=a.iloc[:threshold_index,:]
            a=a[{'datetime','discharge'}]
            annual_max.append(a)
            
            # #Creating Corresponding pair of data.
        amax_folder=('C:/Users/aghangha/Documents/copulas/amax/')
        File_name=['amax_on_main_daily','amax_on_trib_daily']
        File_name=[File + '_' + mainlist[zi] +'_7day'+'.csv' for File in File_name]
        ind=[1,0];
        for i in range(len(annual_max)):
            a=annual_max[i];
            a.index=pd.to_datetime(a.datetime)
            x=df_list[i].discharge.loc[a.index].values;
            y=np.empty(len(x))
            for j in range(len(x)):
                values_before=df_list[ind[i]].discharge.loc[:a.index[j]].tail(4).values; # tail 84 extracts all 84 values just above this index
                values_after=df_list[ind[i]].discharge.loc[a.index[j]:].head(4).values; # 84 for 7 day, 48 for four day, 24 for two day, 12 for 1 day
                y[j]=max(np.append(values_after,values_before))
            x=x[~np.isnan(y)]
            y=y[~np.isnan(y)]
            df=pd.DataFrame({'Focus' : x, 'Corresponding': y})
            df.to_csv(amax_folder + File_name[i], index=False)
            
        amax_on_main= pd.read_csv(amax_folder + File_name[0])
        amax_on_trib = pd.read_csv(amax_folder + File_name[1])    
        
        ##################################
        #Copula Creation.
        ###################################   
        # Annual Max on Main Stream
        
        df_pairs=pd.DataFrame()
        
        x=amax_on_main.Focus.values;
        y=amax_on_main.Corresponding.values;
        rho=(np.sum((x-x.mean())*(y-y.mean())))/(np.sqrt((np.sum((x-x.mean())**2))*(np.sum((y-y.mean())**2)))) # co-relation coefficient
            #kendall's tau
        tau,p = st.kendalltau(x,y)
            #gumbel-hougaard copula
        theta=1/(1-tau);

            # if typofEx[0]=="pearson3":
            #     u=st.pearson3.cdf(x,dpara[0][0],dpara[0][1],dpara[0][2]);
            # elif typofEx[0]=="LogNormal":
            #     u=st.norm.cdf(np.log(x),dpara[0][0],dpara[0][1])
            # if typofEx[1]=="pearson3":
            #     v=st.pearson3.cdf(y,dpara[1][0],dpara[1][1],dpara[1][2]);
            # elif typofEx[1]=="LogNormal":
            #     v=st.norm.cdf(np.log(y),dpara[1][0],dpara[1][1])
                
            # Cg=np.exp(-((-np.log(u))**theta + (-np.log(v))**theta)**(1/theta));
            #     #3D plotting of copula generated joint probability
            # from mpl_toolkits.mplot3d import Axes3D
            # fig = plt.figure()
            # ax = Axes3D(fig)
            # ax.scatter(x, y, Cg)
            # #    plt.title(title[i])
            # ax.set_xlabel('Main Stream Discharge')
            # ax.set_ylabel("Tributary Discharge")
            # ax.set_zlabel('Joint Cummulative Frequency')
            # plt.show()
        
            
        #####
        u1=np.asarray([100,99,97,95,90,80,75,70,60,55,50,45,40,35,30,25,20,15,10,9,8,7,6,5,4,3,2,1])
        u1=1/u1
        v1=np.exp(-((-math.log(0.01))**theta - (-np.log(u1))**theta)**(1/theta))    #100 year
        v2=np.exp(-((-math.log(0.02))**theta - (-np.log(u1))**theta)**(1/theta))    #50 year
        v3=np.exp(-((-math.log(0.04))**theta - (-np.log(u1))**theta)**(1/theta))    #25 year
        
        
        df_pairs['POM_mainstream']=1/u1
        df_pairs['POM_tributary_100_yr']=1/v1
        df_pairs['POM_tributary_50_yr']=1/v2
        df_pairs['POM_tributary_25_yr']=1/v3
        
        
        # pp_1=plottingposition(amax_on_main.Focus)
        # dpara, typeofEx = distribution(amax_on_main.Focus, pp_1)
        # if typeofEx[0]=="pearson3":
        #     a1=st.pearson3.ppf((1-u1),dpara[0][0],dpara[0][1],dpara[0][2])
        # elif typeofEx[0]=="LogNormal":
        #     a1=np.exp(st.norm.ppf((1-u1),dpara[0][0],dpara[0][1]))
        # elif typeofEx[0] =="LP3":
        #     a1=np.exp(st.pearson3.ppf((u1),dpara[0][0],dpara[0][1],dpara[0][2]))
        
        # pp_1 = plottingposition(amax_on_main.Corresponding)
        # dpara, typeofEx = distribution(amax_on_main.Corresponding, pp_1)
        # if typeofEx[0]=="pearson3":
        #     b1=st.pearson3.ppf((1-v1),dpara[0][0],dpara[0][1],dpara[0][2])
        #     b2=st.pearson3.ppf((1-v2),dpara[0][0],dpara[0][1],dpara[0][2])
        #     b3=st.pearson3.ppf((1-v3),dpara[0][0],dpara[0][1],dpara[0][2])
        # elif typeofEx[0]=="LogNormal":
        #     b1=np.exp(st.norm.ppf((1-v1),dpara[0][0],dpara[0][1]))
        #     b2=np.exp(st.norm.ppf((1-v2),dpara[0][0],dpara[0][1]))
        #     b3=np.exp(st.norm.ppf((1-v3),dpara[0][0],dpara[0][1]))
        # elif typeofEx[0]=="Normal":
        #     b1=(st.norm.ppf((1-v1),dpara[0][0],dpara[0][1]))
        #     b2=(st.norm.ppf((1-v2),dpara[0][0],dpara[0][1]))
        #     b3=(st.norm.ppf((1-v3),dpara[0][0],dpara[0][1]))
        # elif typeofEx[0] =="LP3": # since for finding CDF of lp3 we used 1-CDF so here ppf is inverse pf CDF so we will find ppf of 1-cdf value. hence
        #     b1=np.exp(st.pearson3.ppf((v1),dpara[0][0],dpara[0][1],dpara[0][2]))
        #     b2=np.exp(st.pearson3.ppf((v2),dpara[0][0],dpara[0][1],dpara[0][2]))
        #     b3=np.exp(st.pearson3.ppf((v3),dpara[0][0],dpara[0][1],dpara[0][2]))
            
        ################
        # Annual Max on Tributary
        
        x=amax_on_trib.Focus.values;
        y=amax_on_trib.Corresponding.values;
        rho=(np.sum((x-x.mean())*(y-y.mean())))/(np.sqrt((np.sum((x-x.mean())**2))*(np.sum((y-y.mean())**2)))) # co-relation coefficient
            #kendall's tau
        tau,p = st.kendalltau(x,y)
            #gumbel-hougaard copula
        theta=1/(1-tau);
        
        v1=np.exp(-((-math.log(0.01))**theta - (-np.log(u1))**theta)**(1/theta))
        v2=np.exp(-((-math.log(0.02))**theta - (-np.log(u1))**theta)**(1/theta))
        v3=np.exp(-((-math.log(0.04))**theta - (-np.log(u1))**theta)**(1/theta))
        
        df_pairs['POT_tributary']=1/u1
        df_pairs['POT_mainstream_100_yr']=1/v1
        df_pairs['POT_mainstream_50_yr']=1/v2
        df_pairs['POT_mainstream_25_yr']=1/v3
        
        fi_name= amax_folder + File_name[0][13:-4] + '_table.csv'
        df_pairs=df_pairs[['POM_mainstream','POM_tributary_100_yr','POT_tributary','POT_mainstream_100_yr','POM_mainstream','POM_tributary_50_yr','POT_tributary','POT_mainstream_50_yr','POM_mainstream','POM_tributary_25_yr','POT_tributary','POT_mainstream_25_yr']]
        
        df_pairs.to_csv(fi_name,index=False)

        # pp_1=plottingposition(amax_on_trib.Focus)
        # dpara, typeofEx = distribution(amax_on_trib.Focus, pp_1)
        # if typeofEx[0]=="pearson3":
        #     a2=st.pearson3.ppf((1-u1),dpara[0][0],dpara[0][1],dpara[0][2])
        # elif typeofEx[0]=="LogNormal":
        #     a2=np.exp(st.norm.ppf((1-u1),dpara[0][0],dpara[0][1]))
        # elif typeofEx[0]=="Normal":
        #     a2=(st.norm.ppf((1-u1),dpara[0][0],dpara[0][1]))
        # elif typeofEx[0] =="LP3":
        #     a2=np.exp(st.pearson3.ppf((u1),dpara[0][0],dpara[0][1],dpara[0][2]))
        
        # pp_1 = plottingposition(amax_on_trib.Corresponding)
        # dpara, typeofEx = distribution(amax_on_trib.Corresponding, pp_1)
        # if typeofEx[0]=="pearson3":
        #     b11=st.pearson3.ppf((1-v1),dpara[0][0],dpara[0][1],dpara[0][2])
        #     b12=st.pearson3.ppf((1-v2),dpara[0][0],dpara[0][1],dpara[0][2])
        #     b13=st.pearson3.ppf((1-v3),dpara[0][0],dpara[0][1],dpara[0][2])
        # elif typeofEx[0]=="LogNormal":
        #     b11=np.exp(st.norm.ppf((1-v1),dpara[0][0],dpara[0][1]))
        #     b12=np.exp(st.norm.ppf((1-v2),dpara[0][0],dpara[0][1]))
        #     b13=np.exp(st.norm.ppf((1-v3),dpara[0][0],dpara[0][1]))
        # elif typeofEx[0]=="Normal":
        #     b11=(st.norm.ppf((1-v1),dpara[0][0],dpara[0][1]))
        #     b12=(st.norm.ppf((1-v2),dpara[0][0],dpara[0][1]))
        #     b13=(st.norm.ppf((1-v3),dpara[0][0],dpara[0][1]))
        # elif typeofEx[0] =="LP3":
        #     b11=np.exp(st.pearson3.ppf((v1),dpara[0][0],dpara[0][1],dpara[0][2]))
        #     b12=np.exp(st.pearson3.ppf((v2),dpara[0][0],dpara[0][1],dpara[0][2]))
        #     b13=np.exp(st.pearson3.ppf((v3),dpara[0][0],dpara[0][1],dpara[0][2]))
        
        # #Plotting the Joint Distribution with POT and POM
        
        # # mainc.index=pd.to_datetime(mainc.datetime)
        # # tribc.index=pd.to_datetime(tribc.datetime)
        # x=mainc.discharge.rename('main')
        # #y=tribc.discharge.loc[mainc.index].values
        # y=tribc.discharge.rename('trib')
        # x=pd.concat([x,y],axis=1,join='inner')
        # fig=plt.figure()
        # plt.scatter(x.main.values,x.trib.values)
        # plt.plot(a1,b1,'r-',a1,b2,'b-',a1,b3,'g-', a2,b11,'r--',a2,b12,'b--',a2,b13,'g--' )
        # #plt.plot(a1,b1,'r-', a2,b11,'r--')
        # plt.legend(('100 year Returm period POM','50 year return period POM','25 year return period POM', '100 year Returm period POT','50 year return period POT','25 year return period POT'), loc ='upper right')
        # #plt.legend(('Peak on MainStream', 'Peak on Tributary'), loc ='upper right')
        # plt.title("Return Period assuming 7 day buffer period")
        # plt.xlabel('Main Stream Discharge(cfs)')
        # plt.ylabel('Tributary Discharge(cfs)')
        # fig_name= amax_folder + File_name[0][:-4] + '_assuming_7day'+ '.png'
        # plt.savefig(fig_name)
    except AttributeError:
        print ('Main stream station has missing year data, station id:' + mainlist[zi])
    
    
    
    
    
    
    
    
    
    
    
