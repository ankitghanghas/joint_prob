# -*- coding: utf-8 -*-
"""
Created on Mon May 10 17:15:43 2021

regression on correlation coefficient and drainage area ratio.

@author: aghangha
"""

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

df=pd.read_csv("C:\\Users\\aghangha\\Documents\\copulas\\simulated_Wabash\\tau_table_sim_wabash.csv")

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


def plot_regression(data,predicted,stream,func):
    
       
        
        


            
