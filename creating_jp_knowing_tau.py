# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 13:40:49 2022

@author: aghangha
"""

import numpy as np

import math
from scipy.optimize import fsolve



kendall_tau=0.75

theta=1/(1-kendall_tau)


desired_return_period=100

RP_on_one_stream=np.asarray([1.25,2,5,10,25,40,50,75,100])
RP_on_other_stream=[]

freq_one_stream=1/RP_on_one_stream
u_list=1-freq_one_stream



for i in range(len(u_list)):

    u=u_list[i]
    def equations(p):
        x,y =p
        a=1-u-x+y-1/desired_return_period
        b=y-np.exp(-((-math.log(u))**theta + (-np.log(x))**theta)**(1/theta))
        return(a,b)
    
    x,y=fsolve(equations,(1,1))
    RP_on_other_stream.append(1/(1-x))


