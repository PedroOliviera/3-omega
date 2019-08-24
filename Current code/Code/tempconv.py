# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 17:26:31 2019

@author: Pedro
"""
import matplotlib.pyplot as plt

def tempconv(voltage):
#   for k1 to make sense
    current = 0.000996
   #current = 0.000085
    r0=100
    a=3.9083e-3
    b=-5.775e-7
    c=-4.183e-12
    ctr = 0
    voltage = [abs(i) for i in voltage]
   
    T = [None for i in voltage]
    for v in voltage:
        Rt = v/current
        T[ctr] =(Rt/r0-1)/a
        ctr += 1
    n_avg = 26
    T = np.array(T)
    n_pt = int(len(T)/n_avg)
    print(n_pt)
    T1 = [None for i in range(n_pt)]
    for i in range(n_pt):
        T1[i] = T[i*n_avg: (i+1)*n_avg ].mean()
    return T1


temp = tempconv(k1)
x = [i for i in range(len(temp))]
plt.plot(x,temp)