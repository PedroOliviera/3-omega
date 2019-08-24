# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 09:43:49 2019

@author: Pedro
"""
import serial
import numpy as np
import time

def ask_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush()
    state = lock.readline()  
    decoded = bytes.decode(state)
    print(decoded)
    return decoded



def tell_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush() 
    
lock = serial.Serial('COM5', baudrate=19200, parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3) 
t = 3
i=0
while i != 'a':
    tell_lockin('REST')
    tell_lockin('STRT')
    
    time.sleep(t)
    
    tell_lockin('PAUS') 
    
    num_points = ask_lockin('SPTS?')
    x = ask_lockin('TRCA?1,0,'+str(num_points))  #outputs buffer
    x = x[:len(x)-2]                                 #investigate why -1 here and -2 in calb
    
    x = x.split(',')
       
    x_split = [float(i) for i in x]
    print(x_split)
    x_split = np.array(x_split) 
    print('For:   ' + str(ask_lockin('FREQ?')))
    print('x:  ')
    
    i = input('press a to exit, press anything else to measure again')

lock.close()