# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:12:44 2019

@author: Pedro

For sampling v1w sample and shunt for DRDT
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

direc = r'C:\Users\Pedro\Dropbox\1-Three Omega with Ara\new_python\3omega-lockin-Pedro\TARA8\DRDT\Old_Fashion'

print('running...')
tell_lockin('HARM1')
tell_lockin('FREQ250')
tell_lockin('SLVL0.1')
tell_lockin('SRAT7')
tell_lockin('REST')
pre = input('do you want to preset? (y/n). Make sure BNCs are set before entering')

if pre == 'y':
    time.sleep(20)
elif pre == 'n':
    pass
else:
    raise TypeError('invalid input')
    
input('Press enter to start measurement')
print('Measuring...')
t = time.time()
tell_lockin('STRT')
n = input("press enter to stop measurement")
t2 = time.time()-t
tell_lockin('PAUS')
num_points = ask_lockin('SPTS?')
x1 = ask_lockin('TRCA?1,0,'+str(num_points))  #outputs buffer
x1 = x1[:len(x1)-2]  
x1 = x1.split(',')
volt = [float(i) for i in x1]
num_points = int(num_points.rstrip())
inc = t2/num_points
ttime = [inc*i for i in range(num_points)]
v_data = [ttime,volt]
title = ['time','volt']
#######################CHANGE BEFORE RUNNING##############################
if n != 'n':
    csv_writer('\\200_v',v_data,title,direc=direc)
else:
    sys.exit()

n = input("press enter to start shunt measurement or n to cancel")
print('measuring...')
if n == 'n':
    sys.exit()

tell_lockin('REST')
tell_lockin('STRT')
if t2 > 120:
    t2 = 120

time.sleep(t2)
  #outputs buffer

while True:
    try:
        x2 = ask_lockin('TRCA?1,0,'+str(t2))
        x2 = x2[:len(x2)-2]  
        x2 = x2.split(',')
        vsh = [float(i) for i in x2]
    except:
        print('not enough points in buffer reading again')
    else:
        break
vsh_data = [ttime,vsh]
#######################CHANGE BEFORE RUNNING##############################
csv_writer('\\200_vsh',vsh_data,title,direc=direc)

fig = plt.figure()
fig.suptitle('V1w vs Time', fontsize=20)
plt.xlabel('Time[s]')
plt.ylabel('V1W[V]') 
plt.errorbar(ttime,volt, fmt='o')


fig = plt.figure()
fig.suptitle('Shunt vs Time', fontsize=20)
plt.xlabel('Time[s]')
plt.ylabel('Shunt[V]') 
plt.errorbar([i for i in range(len(vsh))],vsh, fmt='o')
plt.show()

print('Done measurement')
lock.close()




