# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 16:17:37 2019

@author: Pedro
"""
import serial
import numpy as np

def ask_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush()
    state = lock.readline()  
    decoded = bytes.decode(state)
    print(decoded)

def tell_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush() 
    
def getListFreq(lower, upper, num_points):
    spacing = np.log((upper/lower)) / (num_points - 1)
    print(spacing)
    listfreq = [np.exp(i*spacing + np.log(lower)) for i in range (num_points)]
    return listfreq

def manual_scan(freq):
    ctr=0
    while ctr<len(freq):
        i = freq[ctr] 
        tell_lockin('FREQ'+str(i))
        print('At: ' + str(i) + 'Hz')
        while True:
            k = input('press n to go to the next frequency, b to go back to the last frequency or o to the computers v3w output')
            print('')
            if k == 'o':
                ask_lockin('OUTP?1')
            elif k == 'n':
                ctr += 1
                break
            elif k == 'b':
                ctr = ctr - 1
                break
            
lock = serial.Serial('COM5', baudrate=19200, parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)  

tell_lockin('HARM3')
tell_lockin('SLVL3')

lf = [400,450]
lf.extend(getListFreq(500,3700,15))
lf.append(3750)
lf.append(3800)
print(lf)
manual_scan(lf)


    