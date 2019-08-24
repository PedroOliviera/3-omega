# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 10:19:23 2019

@author: Pedro
"""

#testing hysteresis

import serial
import time
import matplotlib.pyplot as plt   
import numpy as np
import math

def ask_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush()
    state = lock.readline()  
    decoded = bytes.decode(state)
    return(decoded)

def tell_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush() 
    
def getData():
        tt = 5
        time.sleep(15)
        tell_lockin('REST')
        tell_lockin('STRT')
        time.sleep(tt)
        tell_lockin('PAUS')
    
        num_points = ask_lockin('SPTS?')
        x = ask_lockin('TRCA?1,0,'+str(num_points))  #outputs buffer
        x = x[:len(x)-2]                                 #investigate why -1 here and -2 in calb
        x = x.split(',')
        x_split = [float(i) for i in x]
        x_split = np.array(x_split) 
        
        print('For:   ' + str(freq))
        print('x:  ')
        print(x)
        
        out_x = x_split.mean()
        
        sd_x = x_split.std()
        
        print("output mean:  "+str(out_x))
        print("standard deviation:  "+ str(sd_x))
        print('')
        
        return out_x,sd_x

def to_freq(): #converts ln2w to freq
    sc = sc_freq
    sc = np.array(sc)
    sc = np.exp(sc)/(4*np.pi)
    return sc

def to_ln2w(): #converst freq to ln2w
    sc = sc_freq
    sc = np.array(sc)
    sc = np.log(4*np.pi*sc)
    return sc

def plot_values(x,y):
    plt.errorbar(x,y,ms=8, fmt='o')
    #plt.scatter(x,y,s=40)
    
def plot_labels(sweep):
    
    fig.suptitle('V3\u03C9  vs Number of Increments to 2400Hz) ', fontsize=26)
    plt.xlabel('Number of Increments', fontsize = 22)
    plt.ylabel('V3\u03C9 [V]', fontsize = 22) 
    plt.legend([str(i) for i in range(1,sweep + 1)], fontsize =10) 
    fig.savefig('Hysteresistest.jpg')
    plt.show()

def sweeps():
    for i in range(len(inc)):
        plot_values(inc1[i*n_sweeps:(i+1)*n_sweeps],v3w[i*n_sweeps:(i+1)*n_sweeps])

def setup():
    tell_lockin('HARM3')
    tell_lockin('SLVL3')
    tell_lockin('SENS22')
    
lock = serial.Serial('COM5', baudrate=19200, parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)  

freq = 3807 #2401.04565681



inc = [i+1 for i in range(6)] #number of test increments smallest increment in last program was about 267 here it will be 200

n_sweeps = 1 #change to 50
inc1=[]
v3w=[]
v3w_sd=[]
est_time = 0
while est_time < 1:
    n_sweeps += 1
    est_time = 0
    for i in inc:
        est_time+=(3*i+26)*n_sweeps
    est_time = est_time/3600
print('number of sweeps: ' + str(n_sweeps))
print('estimated time for test: ' + str(est_time) + ' hours')
t5=time.time()
setup()

for i in inc:
    spacing = freq/i
    for j in range(n_sweeps):
        tell_lockin('FREQ1')
        inc1.append(i)
        print(1)
        time.sleep(3)
        for k in range(i):
            tell_lockin('FREQ'+str((spacing)*(k+1)))
            print(str((spacing)*(k+1)))
            if k!=(i-1):
                time.sleep(6)
            else:
                a,b=getData()
                v3w.append(a)
                v3w_sd.append(b)
print('time it took: ' + str(t5-time.time()))
fig = plt.figure()


sweeps()
plot_labels(n_sweeps)
'''
freq = [[1,500],[20000,500],[100,200,300,400,500],[1000,900,800,700,600,500]]
ctr=0
for h in freq:
    ctr+=1
    for g in h:
        time.sleep(3)
        tell_lockin('FREQ'+str(g))
        
    print('starting scan')
    tell_lockin('REST')
    tell_lockin('STRT')
    elapsed = time.time()
    time.sleep(t)
    tell_lockin('PAUS')
    elapsed = time.time() - elapsed
    
    num_points = ask_lockin('SPTS?')
    
    
    print('amount of time sampling: ')
    print(elapsed)
    
    
    y = ask_lockin('TRCA?1,0,'+str(num_points)) 
    y = y[:len(y)-2]
    y = y.split(',')
    y = [float(i) for i in y]
    y = np.array(y)
     
    l = len(y)
    spacing = elapsed / l
    x = [(n*spacing + spacing) for n in range(l)]
    
    
    fig = plt.figure() 
    print('plotting')
    plt.errorbar(x,y)
    fig.suptitle('V3w vs Time at 2000Hz and 3V', fontsize=20)
    plt.ylabel('Time(s)')
    plt.ylabel('V3W[V]') 
    fig.savefig('V3w vs Time at 2000Hz and 3V'+str(ctr)+'.jpg')
    plt.show()
    data = [x, y]
    filename = 'steadystateV3W'+str(ctr)
    title = ['time','v3w']
    csv_writer(filename,data,title)
'''
            
            
        
    