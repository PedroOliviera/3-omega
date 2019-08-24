# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 09:41:44 2019

@author: Pedro
"""

import serial
import time

def ask_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush()
    state = lock.readline()  
    decoded = bytes.decode(state)
    print(decoded)
    return(decoded)
    
def getVal():
    ask_lockin('REST')
    ask_lockin('STRT')
    ask_lockin('TRCA?1,0,40')

lock = serial.Serial('COM16', baudrate=19200, parity=serial.PARITY_NONE,
                             stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)