# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 20:35:53 2019

@author: Pedro

'final' code for calculating DRDT and plotting results
"""

from scipy.interpolate import interp1d
import scipy.signal as sig
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#######First read data from files#######
direc = r'C:\Users\Pedro\Dropbox\1-Three Omega with Ara\new_python\3omega-lockin-Pedro\TARA8\DRDT\Old_Fashion'


higher_temp = 52

lower_temp = 28

sample = ''

filename = str(lower_temp) + '_' + str(higher_temp) + '.csv'

temp_data = pd.read_csv(direc + '/' + sample + '200_temp.csv')

T = temp_data['Temp'].values
time_T = temp_data['Time'].values

volt_data = pd.read_csv(direc +'/'+ sample + '200_v.csv')
V = volt_data['volt'].values
time_V = volt_data['time'].values

shunt_data = pd.read_csv(direc + '/' + sample + '200_vsh.csv')
Vsh = shunt_data['volt'].values
'''
temp_data = pd.read_csv(direc + '/' + 'temp_taramethod_' + '2' + '.csv')

T = temp_data['Temp'].values
time_T = temp_data['Time'].values

volt_data = pd.read_csv(direc +'/'+ 'voltA1_taramethod_' + '2' + '.csv')
V = volt_data['volt'].values
time_V = volt_data['time'].values

shunt_data = pd.read_csv(direc + '/' + 'vshA1_taramethod_' + '2' + '.csv')
Vsh = shunt_data['volt'].values
'''
Vsh = [i for i in Vsh if i!=0]
#this is to check how stable Vsh has been. Have had trouble with this in the past. 
fig = plt.figure()
plt.ion()
fig.suptitle('Vsh(V) vs sample number', fontsize=26)
plt.errorbar([n for n in range(len(Vsh))],Vsh, fmt='o')
Vsh=np.array( Vsh[80:120])
#######Calculate Resistance from Volt and Shunt measurement#######
Vsh_avg = Vsh.mean()
Vsh = np.array([Vsh_avg for i in V])
R_shunt = 0.099
I = Vsh/R_shunt
R = V/I

#######Interpolate#######

if len(time_T) > len(time_V):
	time = time_V
else:
	time = time_T

fig = plt.figure()
plt.ion()
fig.suptitle('Temp raw data (Temp(C) vs Time(s))', fontsize=26)
plt.errorbar(time_T,T)

fig = plt.figure()
fig.suptitle('Resist raw data (Resist(\u03A9) vs Time(s)', fontsize=26)
plt.plot(time_V,R)

plt.show()

try:
    print('to set to beginning of data input nothing')
    lower = float(input('Input lower bound on the range that will be fitted: '))
except:
    print('invalid input')
    print('setting to default lower range bound of the very beginning of data')
    lower = time_T[0]
    
try:
    print('to set to beginning of data input nothing')
    upper = float(input('Input upper bound on the range that will be fitted: '))
except:
    print('invalid input')
    print('setting to default higher range bound of the very end of data')   
    if time_T[-1] > time_V[-1]:
        upper = time_V[-1]
    else:
    	upper = time_T[-1]
    
timeV=[]
timeT=[]


for tV,tT in zip(time_V,time_T):
    if tV<upper and tV>lower:
        timeV.append(tV)
    if tT<upper and tT>lower:
        timeT.append(tT)

V_lower_ind = int(np.where(time_V == timeV[0])[0])
V_upper_ind = int(np.where(time_V == timeV[-1])[0])

T_lower_ind = int(np.where(time_T == timeT[0])[0])
T_upper_ind = int(np.where(time_T == timeT[-1])[0])
    
T = T[T_lower_ind:T_upper_ind + 1]    
R = R[V_lower_ind:V_upper_ind + 1]    
upper = timeT[-1]
lower = timeT[0]
spacing = (upper - lower) / (len(timeT) - 1)
for t in T:
    timeTT = [lower + i*spacing for i in range(len(timeT))]

timeT = timeTT
if len(T)%2==0:
    lenT = len(T)-1
else:
    lenT = len(T)

if len(R)%2==0:
    lenR = len(R)-1
else:
    lentR = len(R)

#apply savitzky-golay filter to smooth data
T2 = sig.savgol_filter(T, window_length = lenT, polyorder = 4)
R2 = sig.savgol_filter(R, window_length = lenR, polyorder = 4)

fig = plt.figure()
fig.suptitle('Temp data filtered (Temp(C) vs Time(s))', fontsize=26)
plt.plot(timeT,T2)

fig = plt.figure()
fig.suptitle('Resist data filtered (Resist(\u03A9) vs Time(s)', fontsize=26)
plt.plot(timeV,R2)

fT = interp1d(timeT, T2,'quadratic')
fR = interp1d(timeV, R2,'quadratic')

if timeT[0] < timeV[0]:
    time = timeV
    if timeV[-1] > timeT[-1]:
        time = time[:-2]
else:
    time = timeT
    if timeT[-1] > timeV[-1]:
        time = time[:-2]

temp = np.array([fT(t) for t in time])
resist = np.array([fR(t) for t in time])

fig = plt.figure()
fig.suptitle('Temp filted and interpolated (Temp(C) vs Time(s))')
plt.plot(time,temp)
plt.plot(timeT,T2)

fig = plt.figure()
fig.suptitle('Resist filtered and interpolated (Resist(\u03A9) vs Time(s)')
plt.plot(time,resist)
plt.plot(timeV,R2)

del_r = np.diff(resist)
del_t = np.diff(temp)

fig = plt.figure()
fig.suptitle('\u0394R', fontsize=26)
plt.plot(time[:-1],del_r)

fig = plt.figure()
fig.suptitle('\u0394T', fontsize=26)
plt.plot(time[:-1],del_t)
plt.show()

DRDT = del_r/del_t

fig = plt.figure()
fig.suptitle('\u0394R savitzky-golay')
plt.plot(del_r)

fig = plt.figure()
fig.suptitle('\u0394T savitzky-golay')
plt.plot(del_t)

fig2 = plt.figure()
fig2.suptitle('savitzky-golay drdt', fontsize=26)
plt.plot(DRDT)


print('DRDT_median: ' + str(np.median(DRDT)))
print('savitzky-golay drdt' + str(DRDT.mean()))