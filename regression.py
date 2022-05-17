# -*- coding: utf-8 -*-
"""
Created on Mon May 10 17:15:43 2021

regression on correlation coefficient and drainage area ratio.

@author: aghangha
"""
#%%

from math import log
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np


# calculate bic for regression
def calculate_bic(n, mse, num_params):
	bic = n * log(mse) + num_params * log(n)
	return bi


#df=pd.read_csv(r"E:\copula\nwm_outputs\conus\tau_table_stat_sig.csv",index_col=0)
#df=pd.read_csv(r"E:\copula\nwm_outputs\tau_table_stat_sig_all.csv",index_col=0)
df=pd.read_csv(r"E:\copula\nwm_outputs\tau_table_15day_stat_sig_CONUS.csv",index_col=0)
df.VPUID=df.VPUID.astype('str') # large file so sometimes it does read it as strings
df.RPUID=df.RPUID.astype('str')
#%%

class Regression:
    def __init__(self,dataframe,stream,type_of_regress):
        self.df=dataframe
        self.stream=stream
        self.func=type_of_regress
    
    def data(self):
        x=self.df["DRAIN_ratio"]
        if self.stream == "POM":
            y=self.df['POM_tau']
        elif self.stream == "POT":
            y=self.df['POT_tau']
        return x,y
    def regress(self):
        x,y=self.data()
        if self.func == "Log" :
            x=np.log(x)
        elif self.func == "Power":
            x=np.log(x)
            y=np.log(y)
        
        model=LinearRegression()
        model.fit(x.values.reshape(-1,1), y.values)
        yhat=model.predict(x.values.reshape(-1,1))
        mse=mean_squared_error(y.values,yhat)
        r2=r2_score(y.values,yhat)
        
        if self.func =="Log" :
            print("Best fit line is:   tau=%.3f *ln(Ra) + %.3f" %(model.coef_[0],model.intercept_))
            print(" R_squared : %.4f  , MSE : %.4f " %(r2,mse))
        elif self.func == "Power":
            print("Best fit line is:   tau=%.3f * Ra^(%.3f)"  %(np.exp(model.intercept_), model.coef_[0],))
            print(" R_squared : %.4f  , MSE : %.4f " %(r2,mse))
        out={'Coeff' : model.coef_,
             'Intercept'  : model.intercept_,
             'MSE': mse,
             'R_squared': r2,
             'predicted' : yhat}
        
        return out

#%%

r2_pom=[]
ms_error_pom=[]
equation_pom=[]
coef_pom=[]
intercept_pom=[]
r2_pot=[]
ms_error_pot=[]
equation_pot=[]
coef_pot=[]
intercept_pot=[]
idx=[]

## doing this for conus first
a=Regression(dataframe=df,stream='POM',type_of_regress='Log').regress()
b=Regression(dataframe=df,stream='POT',type_of_regress='Log').regress()
equation_pom.append("tau=%.3f *ln(Ra) + %.3f" %(a['Coeff'],a['Intercept']))
equation_pot.append("tau=%.3f *ln(Ra) + %.3f" %(b['Coeff'],b['Intercept']))
r2_pom.append(a['R_squared'])
r2_pot.append(b['R_squared'])
ms_error_pom.append(a['MSE'])
ms_error_pot.append(b['MSE'])
coef_pom.append(a['Coeff'][0])
coef_pot.append(b['Coeff'][0])
intercept_pom.append(a['Intercept'])
intercept_pot.append(b['Intercept'])
idx.append('CONUS')

## for individual hu_ids
huc_list=df.VPUID.unique()
for huc_id in huc_list:
    a=Regression(dataframe=df[df.VPUID==huc_id],stream='POM',type_of_regress='Log').regress()
    b=Regression(dataframe=df[df.VPUID==huc_id],stream='POT',type_of_regress='Log').regress()
    equation_pom.append("tau=%.3f *ln(Ra) + %.3f" %(a['Coeff'],a['Intercept']))
    equation_pot.append("tau=%.3f *ln(Ra) + %.3f" %(b['Coeff'],b['Intercept']))
    r2_pom.append(a['R_squared'])
    r2_pot.append(b['R_squared'])
    ms_error_pom.append(a['MSE'])
    ms_error_pot.append(b['MSE'])
    coef_pom.append(a['Coeff'][0])
    coef_pot.append(b['Coeff'][0])
    intercept_pom.append(a['Intercept'])
    intercept_pot.append(b['Intercept'])
    idx.append(huc_id)

df_regress=pd.DataFrame({'HUC_ID':idx,
                        'R_sq_POM':r2_pom,
                        'MSE_POM':ms_error_pom,
                        'Eq_POM':equation_pom,
                        'R_sq_POT':r2_pot,
                        'MSE_POT':ms_error_pot,
                        'Eq_POT':equation_pot,
                        'Coeff_POM':coef_pom,
                        'Coeff_POT':coef_pot,
                        'Intercept_POM':intercept_pom,
                        'Intercept_POT':intercept_pot})




    
       
        
        


            

# %%
