# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 17:13:46 2019

@author: Pedro
"""

import numpy as np
import csv
import serial
import time
import matplotlib.pyplot as plt
import sys
def ask_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush()
    state = lock.readline()  
    decoded = bytes.decode(state)
    return(decoded)

def tell_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush() 
    
def csv_writer(filename,data,title,direc=''):
    '''expects filename as a string, data as a list, title as a list and directory'''
    write_to = direc + filename + '.csv'
    data = check_data(data)
    with open(write_to, 'w',newline='') as csvfile:
        
        datal = zip(*data)
        
        filewriter = csv.writer(csvfile)
        filewriter.writerow(title)
        
        filewriter.writerows(datal)
        
def check_data(data):
    '''checks that all lists in data are of equal size to ensure proper output to csv file'''
    size = [None for i in data]
    for i in range(len(data)):
        size[i] = len(data[i])
    largest = max(size)
    for i in range(len(data)):
        while len(data[i]) < largest:
            data[i] = np.append(data[i],0)
    return data

try:
    lock = serial.Serial('COM5', baudrate=19200, parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)
except:
    lock.close()
    lock = serial.Serial('COM5', baudrate=19200, parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)
tell_lockin('REST')
tell_lockin('STRT')
input('plot')
tell_lockin('PAUS')
num_points = ask_lockin('SPTS?')
x1 = ask_lockin('TRCA?1,0,'+str(num_points))  #outputs buffer
x1 = x1[:len(x1)-2]  x1 = x1.split(',')
volt = [float(i) for i in x1]

fig = plt.figure()
x=[i for i in range(len(volt))]
'''
plt.errorbar(x,volt,fmt='o')
data = [x,volt]
title=['sample number','v1w']
csv_writer('\\DRDT34_38_V',data,title,direc=direc)
'''