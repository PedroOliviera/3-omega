# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 09:31:01 2019

@author: Pedro
"""

import nidaqmx
import time
import csv
import numpy as np
import matplotlib.pyplot as plt
import time
import numpy as np
import serial

    

def tempconv(voltage):
#   for k1 to make sense
    current = 0.0009985
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
        T[ctr] = (-a + np.sqrt((a*2-4*b*c)))/(2*b) - Rt/r0
        ctr += 1
    n_avg = 1
    T = np.array(T)
    n_pt = int(len(T)/n_avg)
    T1 = [None for i in range(n_pt)]
    for i in range(n_pt):
        T1[i] = T[i*n_avg: (i+1)*n_avg ].mean()
    return T1
        

total_t=5
time_per_sample = 0.2
num_samples = total_t/time_per_sample
num_samples = int(num_samples)
num_samples=1000
current = [0 for i in range(num_samples)]
resist = [0 for i in range(num_samples)]
tc = [0 for i in range(num_samples)]
data = []
k1 = []
k2 = []



with nidaqmx.Task() as task1:
    task1.ai_channels.add_ai_voltage_chan("myDAQ1/ai1")
    #task2.ai_channels.add_ai_resistance_chan("myDAQ1/ai0")
    #task3.add_ai_thrmcpl_chan("myDAQ1/ai0")
    
    task1.start()

    t5=time.time()
    while(time.time()-t5) < 60:
        data = task1.read(2000)
        data = np.array(data)
        k1.append(data.mean())




k1 = np.array(k1)




temp = tempconv(k1)
temp = np.array(temp)
title = ['TEMP']

print(temp.mean())
print('max:')
print(temp.max())
print('min:')
print(temp.min())

x = [i for i in range(len(temp))]
plt.plot(x,temp)
plt.show()
