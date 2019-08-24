
import serial
import numpy as np
import time
import winsound
import csv
import matplotlib.pyplot as plt
import os   
#######################################################
#these functions communicate with the lock-in
#####################################################################
def ask_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush()
    state = lock.readline()  
    decoded = bytes.decode(state)
    return(decoded)

def tell_lockin(cmd):
    lock.write(str.encode(cmd+'\n'))  
    lock.flush() 
    
#####################################################################
#these functions read and write to CSV
#####################################################################
def csv_writer(filename,data,title):
    write_to = direc + filename + '.csv'
    data = check_data(data)
    with open(write_to, 'w',newline='') as csvfile:
        
        datal = zip(*data)
        
        filewriter = csv.writer(csvfile)
        filewriter.writerow(title)
        
        filewriter.writerows(datal)

def create_folder(foldername,directory):
    ctr = 0
    while True:
        ctr += 1
        name = foldername + '(' + str(ctr) + ')'
        try:
            os.mkdir(directory + name)
            return name
            break
        except FileExistsError:
            pass
        
def check_data(data):
    size = [None for i in data]
    for i in range(len(data)):
        size[i] = len(data[i])
    largest = max(size)
    for i in range(len(data)):
        while len(data[i]) < largest:
            data[i] = np.append(data[i],0)
    return data
#####################################################################
#this function records the settings (in the future a dictionary will convert the indexes to English)
#####################################################################
def setting():
    a = ask_lockin('RMOD?') #returns dynamic reserve mode (high reserve/normal/low noise)
    b = ask_lockin('OFLT?') #returns the time constant (10microsec-30kilosec)
    c = ask_lockin('OFSL?') #returns low pass filter slope (6/12/18/24 dB/oct) 
    d = ask_lockin('SYNC?') #returns synchronous filter (Off/On) 
    e = ask_lockin('IGND?') #returns input shield grounding (GROUND/FLOATING)
    f = ask_lockin('ICPL?') #returns input coupling (AC/DC)
    g = ask_lockin('ILIN?') #returns line notch filters (Out, Line in, 2xLine in, Both In)
    h = 22
    data = [a,b,c,d,e,f,g]
    
    title = ['dynamic reserve mode','time constant','low pass filter slope',
             'synchronous filter','input shield grounding','input coupling',
             'line notch filters','sensitivity']
    
    csv_writer('SR830_settings',data,title)

###########################################################
#these functions are for scanning and returning data values
###########################################################
def scan(harm,scan_v_or_f,stb_cond,stb_time): 
#harm is the harmonic being scanned
#scan_v_or_f is whether v is being scanned or f. True for v, False for f
#val_f_or_v is the value of the characteristic being held constant. Should be opposite of ^
    
    tell_lockin('HARM'+str(harm))
    
    output_x = []   
    output_y = []                                   #volt_q=True if scanning volts false if scanning freq
    stdv_x = []
    stdv_y = []
    f = 0
    
    #tt = 3 time that is averaged over for mean
    tt = 10 #5
    
    if scan_v_or_f == 1:
        lc_list = listvolts
        lc_cmd = 'SLVL'
        na = 'V'
    else:
        lc_list = listfreq
        lc_cmd = 'FREQ'
        na = 'Hz'

    #t = calibrate(lc_list,lc_cmd,stb_cond,stb_time)
    t = 15 #15
    

    est_time = (t+tt)*len(lc_list)
    print('estimated time for scan: ' + str(est_time) + ' seconds')
    tot_time = time.time()
    print('')
    print('scanning whole range')
    print('')
    
    tell_lockin('REST') #clears and pauses buffer
    tell_lockin(lc_cmd+str(lc_list[0]))
    ti=time.time()
    time.sleep(t)
    
    for i in range(len(lc_list)):
        if ((i+1)==len(lc_list)):
            break
        
        while f == 0:
            tell_lockin(lc_cmd+str(lc_list[0]))
            ti=time.time()
            time.sleep(t)
            
            f+=1
            if f>1:
                print('''SOMETHING IS VERY WRONG 
                      ############################
                      #############################
                      ############################''')
                for i in range(100):
                    beep()
                
        tii = time.time()-ti
        if (t-tii > 0):
            time.sleep(t-tii)
        
        #MAKE INTO A FUNCTION and take away while loop
        tell_lockin('STRT')
        time.sleep(tt)
        tell_lockin('PAUS')
        
        tell_lockin(lc_cmd+str(lc_list[i+1]))
        ti = time.time()
        num_points = ask_lockin('SPTS?')
        x = ask_lockin('TRCA?1,0,'+str(num_points))  #outputs buffer
        x =  x[:len(x)-2]                                #investigate why -1 here and -2 in calb
        
        y = ask_lockin('TRCA?2,0,'+str(num_points)) 
        y = y[:len(y)-2]
        
        x = x.split(',')
        y = y.split(',')
       
        x_split = [float(i) for i in x]
        y_split = [float(i) for i in y]
        
        x_split = np.array(x_split) 
        y_split = np.array(y_split)
        print('For:   ' + str(lc_list[i]))
        print('x:  ')
        #print(x)
        
        out_x = x_split.mean()
        out_y = y_split.mean()
        sd_x = x_split.std()
        sd_y = y_split.std()
        
        print("output mean:  "+str(out_x))
        print("standard deviation:  "+ str(sd_x))
        print('')
        
        
        output_x.append(out_x)
        output_y.append(out_y)
        stdv_x.append(sd_x)
        stdv_y.append(sd_y)
        tell_lockin('REST')
        
    print('done scanning')
    print('total time scanning:  ' +str(tot_time-time.time()))
    return output_x,stdv_x,output_y,stdv_y
   

def beep():
    f=500
    dur=1000
    winsound.Beep(f,dur)

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
    T1 = [None for i in range(n_pt)]
    for i in range(n_pt):
        T1[i] = T[i*n_avg: (i+1)*n_avg ].mean()
    return T1

# main
lock = serial.Serial('COM5', baudrate=19200, parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)   

tell_lockin("OUTX0")
tell_lockin('SRAT9')

direc = 'C:/Users/Pedro/Dropbox/1-Three Omega with Ara/new_python/3omega-lockin-Pedro/Silicon/New scan method/New Multi Sweep Method/'
folder = create_folder('new folderssss',direc)
direc = 'C:/Users/Pedro/Dropbox/1-Three Omega with Ara/new_python/3omega-lockin-Pedro/Silicon/New scan method/New Multi Sweep Method/' + folder + '/'

tell_lockin('RSET1')

volt = -0.2
freq = 500
tell_lockin("SLVL"+str(volt))

tell_lockin('SENS22')       
##notify.send('doing 3w sample measurement')


















    
    filename = 'Sweep' + str(i+1)
    print(filename)
    sweep_title = ['freq','v3w','sd_v3w']
    print(sweep_title)
    sweep_data = [listfreq[:-1], v3w, sd_v3w]
    print(sweep_data)
    csv_writer(filename,sweep_data,sweep_title)
    print('done writing')
    

fig = plt.figure() 
plot_values(sc_ln2w,v3w,sd_v3w)
plot_labels_v3w_vs_ln2w(n_sweep)    
print('Done 3w sweeps')



tell_lockin('SLVL3')
tell_lockin('HARM3')
tell_lockin('SENS22')

#output,sd =  stuff()
#x = [i for i in range (len(output))]
#plt.errorbar(x,output,sd,fmt='o')



  
sc_sens_3w.append(sensitivity)
sc_volts.append(volt)
sc_temp.append(temp)
###############################################

tell_lockin('SENS26')      
#input("Adjust sensitivity and when ready for 1w sample measurement press enter")
sensitivity = int((ask_lockin('SENS?')).rstrip())
#notify.send('doing 1w sample measurement')
a, b, c, d = scan(1,0,0,stb_time)
v1w.extend(a)
sd_v1w.extend(b)
v1w_o.extend(c) 
sd_v1w_o.extend(d)

for i in range(len(listfreq)):
        sc_sens_1w.append(sensitivity)
        
print('done 1w sample measurement')


###############################################

tell_lockin('SENS22')
beep()
beep() 
beep()
#notify.send('COME SWITCH SHUNTTSSSS')
input("Adjust sensitivity and when ready for 1w shunt measurement press enter. make sure bannas are in place")
#change to input
sensitivity = int((ask_lockin('SENS?')).rstrip())
a, b, c, d = scan(1,0,0,stb_time)
v1w_sh.extend(a)
sd_v1w_sh.extend(b)
v1w_sh_o.extend(c) 
sd_v1w_sh_o.extend(d) 


for i in range(len(listfreq)):
        sc_sens_1w_sh.append(sensitivity)

print('done 1w shunt measurement')


  

data = [sc_volts,sc_freq,v3w,sd_v3w,v3w_o,sd_v3w_o,sc_sens_3w,v1w,sd_v1w, v1w_o, sd_v1w_o, sc_sens_1w,
        v1w_sh,sd_v1w_sh,v1w_sh_o,sd_v1w_sh_o,sc_sens_1w_sh] 

title = ['Ref_Volt', 'f_all', 'Vs_3w', 'sd_Vs_3w', 'Vs_3w_o', 'sd_Vs_3w_o','sens_3w',
         'Vs_1w', 'sd_Vs_1w', 'Vs_1w_o', 'sd_Vs_1w_o', 'sens_1w', 'Vsh_1w', 'sd_Vsh_1w',
         'Vsh_1w_o','sd_Vsh_1w_o','sens_1w_sh']



data.append(sc_temp)
title.append('temp(C)')
#notify.send('DONE SHUNT')
beep()
#filename = input('input filename for data from varying freq (format: material_freqscan_XV):   ')
filename = 'A1_freqscan'
csv_writer(filename,data,title)

print('csv_writer')

setting()
print('settings')
print('time')
print(t5-time.time())




filename += '_analysis'
print('filename')
title_analysis = ['f_all','Vs_3w','Vs_1w','Vs_1w_o','Vsh_1w']
print('title')
data_analysis = [np.array(sc_freq),v3w,v1w,v1w_o,v1w_sh] 
print('data_analysis')

csv_writer(filename,data_analysis,title_analysis)
print('csvwriter2')

plot_v3w_vs_freq(v3w,sd_v3w,np.array(sc_freq))
print('plot_v3w')

