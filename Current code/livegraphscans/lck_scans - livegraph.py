# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 08:42:33 2019

@author: Pedro
"""
import serial
import pandas as pd
import numpy as np
import time
import winsound
import csv
import matplotlib.pyplot as plt
import os   
#####################################################################################################
##################   THESE FUNCTIONS CONTROL THE LOCKIN   ###########################################
#####################################################################################################
def ask_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush()
    state = lock.readline()  
    decoded = bytes.decode(state)
    return(decoded)

def tell_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush() 

def open_lockin():
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
#####################################################################################################
##################   THESE FUNCTIONS SCAN FREQS OR VOLTS  ###########################################
#####################################################################################################    
def beep():
    f=500
    dur=1000
    winsound.Beep(f,dur)
    
def scan(lc_list,scan_v_or_f='freq',harm=3,stb_time=9,averaged_time=1,lc_const=3): 
    '''returns in phase and out of phase voltages in an array'''
    
#harm is the harmonic being scanned
#scan_v_or_f is whether v is being scanned or f. True for v, False for f
#lc_const is the variable being held constant. IF frequency is being scanned voltage is held constant
#if voltage is being scanned frequency is held constant.
#the value of that will be held constant is stored in lc_const. The variable itself is the oppposite 
#scan_v_or_f
    
    
    out_x = []   
    out_y = []
    
    tell_lockin('HARM'+str(harm))
    
    while True:
        if scan_v_or_f == 'volt':
            lc_cmd = 'SLVL'
            tell_lockin('FREQ'+str(lc_const))
            print('Frequency: ' + str(lc_const))
            break
        elif scan_v_or_f == 'freq':
            lc_cmd = 'FREQ'
            tell_lockin('SLVL'+str(lc_const))
            print('Voltage: ' + str(lc_const))
            break
        
    tell_lockin(lc_cmd+str(lc_list[0]))

    #t = calibrate(lc_list,lc_cmd,stb_cond,stb_time)
    t = stb_time #15
    
     #tt = 3 time that is averaged over for mean
    tt = averaged_time #5
    

    est_time = (t+tt)*len(lc_list)
    print('estimated time for scan: ' + str(est_time) + ' seconds')
    tot_time = time.time()
    print('')
    print('scanning whole range')
    print('')
    ti = time.time()
    for i in range(1,len(lc_list)+1):
               
        tii = time.time()-ti
        if (t-tii > 0):
            time.sleep(t-tii)
        
        tell_lockin('REST')
        tell_lockin('STRT')
        time.sleep(tt)
        tell_lockin('PAUS')
        try:
            tell_lockin(lc_cmd+str(lc_list[i])) 
        except IndexError:
            pass
            
        ti = time.time()
        print('For:   ' + str(lc_list[i-1]))
        a,b = getData()
        csv_writer(filename='livecsvfile',data=[lc_list[i-1],a])
        out_x.append(a) 
        out_y.append(b)
        print('')
        print('')
    print('done scanning')
    print('total time scanning:  ' +str(tot_time-time.time()))
    return out_x,out_y

def getData():
        '''returns all the in-phase and out-of-phase values from the buffer'''
        num_points = ask_lockin('SPTS?')
        x = ask_lockin('TRCA?1,0,'+str(num_points))  #outputs buffer
        x = x[:len(x)-2]                                 #investigate why -1 here and -2 in calb
        
        y = ask_lockin('TRCA?2,0,'+str(num_points)) 
        y = y[:len(y)-2]
        
        x = x.split(',')
        y = y.split(',')
       
        x_split = [float(i) for i in x]
        y_split = [float(i) for i in y]
        
        x_split = np.array(x_split) 
        y_split = np.array(y_split)
        
        print('x:')
        print(x_split)
        out_x = x_split.mean()
        out_y = y_split.mean()
                
        print("output mean:  "+str(out_x))
        print('')
        
        return out_x,out_y
    
def n_scans(lc_list=[100],scan_v_or_f='freq',harm=3,stb_time=9,averaged_time=1,n_sweeps=1,lc_const=3):
    '''runs scans function n_sweep number of times and puts the results of scans
    in a list'''
    
    scan_val_x = []
    scan_val_y = []
    for ctr in range(n_sweeps):
        a,b = scan(lc_list,scan_v_or_f,harm,stb_time,averaged_time,lc_const)
        scan_val_x.append(a)
        scan_val_y.append(b)
    
    return scan_val_x, scan_val_y

def mn_scans(lc_list,scan_v_or_f='freq',harm=3,stb_time=9,averaged_time=1,n_sweeps=1,lc_const=[1,2,3]):
   '''scans n_sweep number of times and does this for varying constant freq/volt. This is for testing multiple
   constant frequencies with varying voltage for step 1 and multiple constant voltages to avoid step 1'''
   
   scan_val_x = []
   scan_val_y = []
   if type(lc_const) != list:
       lc_const = [lc_const]
   for ctr in lc_const:
       a,b = n_scans(lc_list,scan_v_or_f,harm,stb_time,averaged_time,n_sweeps,ctr)
       scan_val_x.append(a)
       scan_val_y.append(b)
    
   return scan_val_x, scan_val_y

#####################################################################################################
##################   THESE FUNCTIONS AVERAGE SWEEPS   ###############################################
#####################################################################################################   
        

def avg_sweeps(scan_val_x,scan_val_y):
    '''takes inputs from n_scans and averages them. outputing the average of the in-phase, out-of-phase and the 
    stdev for each'''
    
    
    len_scan = len(scan_val_x)
    
    #here i preallocate memory. This is faster computationally then appending to an empty list 
    avged_x = np.array([None for i in range(len_scan)])
    avged_y = np.array([None for i in range(len_scan)])
    avg_val_x = np.array([None for i in range(len(scan_val_x[0]))])
    avg_val_y = np.array([None for i in range(len(scan_val_x[0]))])
    sd_x = np.array([None for i in range(len(scan_val_x[0]))])
    sd_y = np.array([None for i in range(len(scan_val_x[0]))])
    
    for i in range(len(scan_val_x[0])):
        for j in range(len_scan):
            avged_x[j] = scan_val_x[j][i] 
            if False:
                avged_y[j] = scan_val_y[j][i]
            
        avg_val_x[i] = avged_x.mean()
        sd_x[i] = avged_x.std()
        
        if False:
            avg_val_y[i] = avged_y.mean()
            sd_y[i] = avged_y.std()
    
    return avg_val_x, avg_val_y, sd_x, sd_y

def mn_avg_sweeps(x_val,y_val):
    '''This function was made to simplifiy avg_sweeps for multiple lc_const'''
    val_x = []
    val_y = []
    sd_x = []
    sd_y = []
    
    for ctr in range(len(x_val)):
        a, b, c, d = avg_sweeps(x_val[ctr],y_val[ctr])
        val_x.append(a)
        val_y.append(b)
        sd_x.append(c)
        sd_y.append(d)
        
    return val_x, val_y, sd_x, sd_y

#####################################################################################################
##################   THESE FUNCTIONS SET AND RECORD SETTINGS   ######################################
#####################################################################################################

def rec_settings():
    a = ask_lockin('RMOD?') #returns dynamic reserve mode (high reserve/normal/low noise)
    b = ask_lockin('OFLT?') #returns the time constant (10microsec-30kilosec)
    c = ask_lockin('OFSL?') #returns low pass filter slope (6/12/18/24 dB/oct) 
    d = ask_lockin('SYNC?') #returns synchronous filter (Off/On) 
    e = ask_lockin('IGND?') #returns input shield grounding (GROUND/FLOATING)
    f = ask_lockin('ICPL?') #returns input coupling (AC/DC)
    g = ask_lockin('ILIN?') #returns line notch filters (Out, Line in, 2xLine in, Both In)
    
    
    data = settings_dict(a,b,c,d,e,f,g)
    
    title = ['dynamic reserve mode','time constant','low pass filter slope',
             'synchronous filter','input shield grounding','input coupling',
             'line notch filters']
    
    csv_writer('SR830_settings',data,title)

def settings_dict(a, b, c, d, e, f, g):
    out = []
    RMOD = {0:'High Reserve',1:'Normal',2:'Low Noise'}
    out.append('ROMD: ' + RMOD[a])
    OLFT = {0:'10 µs',1: '30 µs',2: '100 µs', 3: '300 µs', 4: '1 ms', 
            5: '3 ms', 6: '10 ms', 7 : '30 ms', 8: '100 ms', 
            9 : '300 ms', 10 : '1 s', 11: '3 s',12: '10 S', 13 : '30 s', 
            14 : '100 s', 15: '300', 16: '1 ks', 17 : '3 ks', 
            18 : '10 ks', 19 : '30 ks'}
    out.append('OLFT: '+ OLFT[b])
    OFSL = {0: '6 dB/oct', 1: '12 dB/oct', 2: '18 dB/oct', 3: '24 dB/oct'}
    out.append('OFSL: '+ OFSL[c])
    SYNC = {0: 'Off', 1 : 'below 200 Hz'}
    out.append('SYNC: ' + SYNC[d])
    IGND = {0 : 'Float', 1: 'Ground'}
    out.append('IGNDL: ' + IGND[e])
    ICPL = {0:'AC', 1 : 'DC'}
    out.append('ICPL: ' + ICPL[f])
    ILIN = {0 : 'No Filters',1 : 'Line Notch in', 2 : '2xline Notch in', 
            3:'BOth Notch Filters in'}
    out.append('ILIN: ' + ILIN[g])
    return out

def set_settings():
    '''sets lockin settings. OUTX0 command is used to make sure it is in the 
    right serial communication mode. SRAT9 is a set of programmable settings'''
    
    tell_lockin("OUTX0")
    tell_lockin('SRAT9')

#####################################################################################################
##################   THESE FUNCTIONS SAVE FILES TO CSV   ############################################
#####################################################################################################
    
def csv_writer(filename,data,title,direc='',flatten = 'n'):
    '''expects filename as a string, data as a list or list of lists, 
    title as a list and directory'''
    data = check_flat(data)
        
    write_to = direc + '/' +  filename + '.csv'
    data = check_data(data)
    with open(write_to, 'w',newline='') as csvfile:
        
        datal = zip(*data)
        
        filewriter = csv.writer(csvfile)
        filewriter.writerow(title)
        
        filewriter.writerows(datal)

def create_folder(foldername,directory=''):
    '''creates a folder to save files in'''
    ctr = 0
    while True:
        ctr += 1
        name = foldername + '(' + str(ctr) + ')'
        try:
            os.mkdir(directory + '/' + name)
            return directory + '/' + name
            break
        except FileExistsError:
            pass
        
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

def check_flat(data):
    '''if data is a list in a list (like the output from n_scans) flatten list'''
    ctr = 0
    for i in data:
        try:
            data[ctr] = np.array(i)
            data[ctr] = data[ctr].flatten()
        except:
            pass
        ctr += 1
    return data
    
def getListFreq(lower, upper, num_points):
    spacing = np.log((upper/lower)) / (num_points - 1)
    print(spacing)
    listfreq = [np.exp(i*spacing + np.log(lower)) for i in range (num_points)]
    return listfreq

def getListVolt(lower, upper, num_points):
    spacing = (upper - lower) / (num_points - 1)
    listvolt = [lower + i*spacing for i in range(num_points)]
    return listvolt

#####################################################################################################
##################   THIS FUNCTION GENERALLY SCANS FOR STEP 1 and 2   ###############################
#####################################################################################################

def fullScan(start,end,num_points,scan_v_or_f,stb_time,averaged_time,n_sweeps,lc_const):
    '''returns all you need for step1'''
    #set_settings()    
    #rec_settings()    #make list of values one will scan over
    lc_list = getListFreq(start,end,num_points)
    
    beep()
    beep()
    beep()
    input('make sure bnc are set to sample')
    #first do v3w scan
    tell_lockin('SENS22')
    v3w_x, v3w_y = mn_scans(lc_list,scan_v_or_f = scan_v_or_f,harm = 3, stb_time = stb_time, averaged_time = averaged_time
                            , n_sweeps = n_sweeps,lc_const = lc_const) 
    v3w_avg = mn_avg_sweeps(v3w_x, v3w_y)
    
    #proceed to v1w scan
    tell_lockin('SENS26')
    v1w_x, v1w_y = mn_scans(lc_list,scan_v_or_f = scan_v_or_f,harm = 1, stb_time = stb_time, averaged_time = averaged_time
                            , n_sweeps = 1,lc_const = lc_const) 
    
    beep()
    beep()
    beep()
    input('change bnc to shunt')
    #proceed to v1w shunt scan
    tell_lockin('SENS22')
    v1w_sh_x,v1w_sh_y = mn_scans(lc_list,scan_v_or_f = scan_v_or_f,harm = 1, stb_time = stb_time, averaged_time = averaged_time
                            , n_sweeps = 1,lc_const = lc_const) 
    
    ###Fix later###
    #v1w_sd????????
    
    '''
    data = {'f_all':lc_list,'Vs_3w':v3w_avg[0],'Vs_1w':v1w_x,'Vs_1w_o':v1w_y,'Vsh_1w':v1w_sh_x}
    
    if scan_v_or_f == 'freq':
        scan_name = 'Frequencies'
    elif scan_v_or_f == 'volt':
        scan_name = 'Voltages'
    
    output = {scan_name:lc_list,'Data Dict':data}
    '''
    
    output = [lc_list,v3w_avg[0],v1w_x,v1w_y,v1w_sh_x]
    data = [lc_list, v3w_x, v1w_x, v1w_sh_x]
    
    return output, data

print('running')
try:
    lock = serial.Serial('COM16', baudrate=19200, parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)
except:
    lock.close()
    lock = serial.Serial('COM16', baudrate=19200, parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)

#tell_lockin('RSET1')
tell_lockin('SRAT9')
#set_settings()

#set directory and make new folder to save files in
direc = r'C:/Users/Pedro/Dropbox/1-Three Omega with Ara/new_python/3omega-lockin-Pedro/BCB Measurements'
direc = create_folder('BCB_Scan1-2019-08-06',direc)

#remove file if already exists
if os.isfile('livecsvfile.csv') == True:
    os.remove('livecsvfile.csv')
else:
#make file where livegraph data will be saved
    csv_writer(filename = 'livecsvfile' ,title = ['x', 'y'])

