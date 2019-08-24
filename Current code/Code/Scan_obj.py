# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:49:40 2019

@author: Pedro
"""
class ControlLock():
    def ask(self,cmd):
       lock.write(str.encode(cmd+'\n'))  
       lock.flush()
       state = lock.readline()  
       decoded = bytes.decode(state)
       return(decoded)

    def tell(self,cmd):
        lock.write(str.encode(cmd+'\n'))  
        lock.flush()
    

class Scan(object):
    import time
    import numpy as np
    import serial
        
    
    try:
        lock.close()
    except: 
        pass
        while True:
            try: 
                print('in 1')
                lock = serial.Serial('COM5', baudrate=19200, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)
            except:
                print('in 2')
                print('Something is wrong with the connection to lock-in amplifer')
                print('check it is on')
                time.sleep(5)
        else:
            break
    
                
                
    
    
    
            
    '''
    while True:
        try: 
            print('try to open port')
            lock = serial.Serial('COM5', baudrate=19200, parity=serial.PARITY_NONE,
                             stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)
        except:
            print('Something is wrong with the connection to lock-in amplifer')
            print('check it is on')
            time.sleep(5)
        else:
            print('breaking from looop....')
            break
    '''
        
    def tell(self,cmd):
        self.lockin.tell(cmd)
    
   
scan = Scan()
scan
'''
try to make it such that the ask and tell methods are in Scan and that they only run when scan is first initialized.
'''

