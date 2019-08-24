# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:12:44 2019

@author: Pedro
"""

import numpy as np
import csv

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


lock = serial.Serial('COM5', baudrate=19200, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)


input("press enter to start sample measurement (start when temp is stable))")
tell_lockin('SRAT7')
tell_lockin('REST')
tell_lockin('STRT')
input("press enter after 1.5 oscillations")
tell_lockin('PAUS')

num_points = ask_lockin('SPTS?')
x1 = ask_lockin('TRCA?1,0,'+str(num_points))  #outputs buffer
x1 = x1[:len(x1)-2]  
x1 = x1.split(',')
x_split1 = [float(i) for i in x1]

input("press enter to start shunt measurement (start when temp is stable))")

tell_lockin('REST')
tell_lockin('STRT')
input("press enter after 1.5 oscillations")
tell_lockin('PAUS')

num_points = ask_lockin('SPTS?')
x2 = ask_lockin('TRCA?1,0,'+str(num_points))  #outputs buffer
x2 = x2[:len(x2)-2]  
x2 = x2.split(',')
x_split2 = [float(i) for i in x2]

print('Done measurement')

lock.close()

temp = input('input temperature at top of oscillation')

temp = [temp for i in x1]
    
    
data = [temp,x1,x2]
data = check_data(data)
title = ['temp','sample', 'shunt']


#######################CHANGE BEFORE RUNNING##############################
csv_writer('dT_34_sh', data, title)
###########Change^^^^^^^######################################

# EXAMPLE FILENAMES  ####

'dT_temperature'

'dT_34'

