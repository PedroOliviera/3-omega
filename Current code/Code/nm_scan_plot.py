# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 20:25:18 2019

@author: Pedro
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 19:38:50 2019

@author: Pedro
"""

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

def ask_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush()
    state = lock.readline()  
    decoded = bytes.decode(state)
    return(decoded)

def tell_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush() 


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
        T[ctr] =(Rt/r0-1)/a
        ctr += 1
    n_avg = 1
    T = np.array(T)
    n_pt = int(len(T)/n_avg)
    T1 = np.array( [None for i in range(n_pt)])
    for i in range(n_pt):
        T1[i] = T[i*n_avg: (i+1)*n_avg ].mean()
    return T1
        

########################################
#initialize
########################################
   
lock = serial.Serial('COM5', baudrate=19200, parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)   

tell_lockin("OUTX0")
tell_lockin('SRAT9')
tell_lockin('SEND1')


total_t = 5
time_per_sample = 0.2
num_samples = total_t/time_per_sample
num_samples = int(num_samples)
num_samples=1000
current = [0 for i in range(num_samples)]
resist = [0 for i in range(num_samples)]
tc = [0 for i in range(num_samples)]
data = []
k1 = np.array()
k2 = []

########################################
#scan temp
########################################

unstable = True
oldmean = 0
allowedrange = 0.25
lower = allowedrange/2 
upper = lower
tell_lockin('REST')

t = 60
t5 = time.time()
with nidaqmx.Task() as task1:
        task1.ai_channels.add_ai_voltage_chan("myDAQ1/ai1")
        while True:    
            #task1.start()  
            data = task1.read(2000)
            data = np.array(data)
            k1[:len(k1)-1] = k1[1:len(k1)]
            k1[len(k1)] = data
            temp = tempconv(k1)
            mean = temp.mean()
            if mean - lower < oldmean and mean + upper > oldmean:
                unstable = False
            print(unstable)
            ###############take this out for completely continuous scan
            if (time.time()-t5 > 60):
                a = input('do you wanna graph? (y/n)')
                if a == 'y':
                    x = [i for i in range(len(temp))]
                    plt.plot(x,temp)
                t5 = time.time()


#####################
#RECORDS TEMP AND V1w
#####################

'''
with nidaqmx.Task() as task1:
    task1.ai_channels.add_ai_voltage_chan("myDAQ1/ai1")
    
   #task1.start()  
    
    while unstable:
        t5=time.time()
        tell_lockin('STRT')
        while(time.time()-t5) < t:
            data = task1.read(2000)
            data = np.array(data)
            k1.append(data.mean())
        tell_lockin('PAUS')
        temp = tempconv(k1)
        mean = temp.mean()
        if mean - lower < oldmean and mean + upper > oldmean:
            unstable = False

end_point = ask_lockin('SPTS?')
end_point = int(end_point)
start_point = end_point - samp_rate * t
x = ask_lockin('TRCA?1,' + str(start_point) + ',' + str(end_point))
x =  x[:len(x)-2]      
x = x.split(',')
x_split = [float(i) for i in x]
x_split = np.array(x_split)


x = [i for i in range(len(temp))]
x2 = [i for i in range(len(x_split))]
plt.plot(x,temp)
plt.plot(x2,x_split)
'''
