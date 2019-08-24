"""
First iterations of DRDT calculations
"""

from scipy.interpolate import interp1d
import scipy.signal as sig
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

#######First read data from files#######

direc = r"C:/Users/Pedro/Dropbox/1-Three Omega with Ara/new_python/3omega-lockin-Pedro/TARA8/DRDT"

temp_data = pd.read_csv(direc + '/' + 'temp_taramethod_4.csv')
T = temp_data['Temp'].values
time_T = temp_data['Time'].values

volt_data = pd.read_csv(direc +'/'+'voltA1_taramethod_4.csv')
V = volt_data['volt'].values
time_V = volt_data['time'].values

shunt_data = pd.read_csv(direc + '/' + 'vshA1_taramethod_4.csv')
Vsh = shunt_data['volt'].values
plt.plot(Vsh)
Vsh=Vsh[:100]
#######Calculate Resistance from Volt and Shunt measurement#######
Vsh_avg = Vsh.mean()
Vsh = np.array([Vsh_avg for i in V])
R_shunt = 0.099
I = Vsh/R_shunt
R = V/I
#######Interpolate#######

if time_T[-1] > time_V[-1]:
	time = time_V[2:]
else:
	time = time_T

#time = time[100:400]
#time = [i*0.1 for i in range(5,1351)]
fT = interp1d(time_T, T,'quadratic')
fR = interp1d(time_V, R,'quadratic')
temp = np.array([fT(t) for t in time])
resist = np.array([fR(t) for t in time])

r1 = resist[1:len(resist)]
r2 = resist[:-1]

del_r = r1 - r2

t1 = temp[1:len(temp)]
t2 = temp[:-1]

del_t = t1 - t2

fig1 = plt.figure()
fig1.suptitle('Temp fitted data', fontsize=26)
plt.plot(time,temp)

plt.plot(time_T,T)



fig3 = plt.figure()
fig3.suptitle('Resist fitted data', fontsize=26)
plt.plot(time,resist)
plt.plot(time_V,R)


fig5 = plt.figure()
fig5.suptitle('\u0394R', fontsize=26)
plt.plot(time[:-1],del_r)

fig6 = plt.figure()
fig6.suptitle('\u0394T', fontsize=26)
plt.plot(time[:-1],del_t)
plt.show()

DRDT = del_r/del_t
DRDT_org = DRDT

fig2 = plt.figure()
fig2.suptitle('raw drdt', fontsize=26)
plt.plot(DRDT_org)


DRDT_avg = DRDT.mean()
T2 = sig.savgol_filter(T,window_length =875 ,polyorder = 4)
R2 = sig.savgol_filter(R,window_length = 1399,polyorder = 4)

fT = interp1d(time_T, T2,'quadratic')
fR = interp1d(time_V, R2,'quadratic')

temp = np.array([fT(t) for t in time])
resist = np.array([fR(t) for t in time])

fig2 = plt.figure()
fig2.suptitle('Temp raw data', fontsize=26)
plt.plot(time_T,T)

fig4 = plt.figure()
fig4.suptitle('Resist raw data', fontsize=26)
plt.plot(time_V,R)

fig = plt.figure()
fig.suptitle('Temp savitzky-golay filter interpolated')
plt.plot(time,temp)
plt.plot(time_T,T)

fig = plt.figure()
fig.suptitle('Resist savitzky-golay filter interpolated')
plt.plot(time,resist)
plt.plot(time_V,R)

r1 = resist[1:len(resist)]
r2 = resist[:-1]

del_r = np.diff(resist)
del_t = np.diff(temp)

DRDT = del_r/del_t

fig = plt.figure()
fig.suptitle('\u0394R savitzky-golay')
plt.plot(del_r)

fig = plt.figure()
fig.suptitle('\u0394T savitzky-golay')
plt.plot(del_t)

fig2 = plt.figure()
fig2.suptitle('savitzky-golay drdt', fontsize=26)
plt.plot(time[:-1],DRDT)

print('DRDT_avg: ' + str(DRDT_avg))
print('raw DRDT: ' + str(DRDT_org.mean()))
print('DRDT_median: ' + str(np.median(DRDT)))
print('savitzky-golay drdt' + str(DRDT.mean()))
'''
for i in range(20):
    ma = a.max()
    mi = a.min()
    m1 = np.where(a==ma)
    m1 = m1[0][0]
    m2 = np.where(a==mi)
    m2= m2[0][0]
    a=np.delete(a,m1)
    a=np.delete(a,m2)
'''
'''
for i in range(20):
    loc_max = np.where(DRDT==DRDT.max())
    DRDT = np.delete(DRDT,loc_max)
    loc_min = np.where(DRDT==DRDT.min())
    DRDT = np.delete(DRDT,loc_min)
    fig3 = plt.figure()
    fig3.suptitle('fix drdt'+str(i) + ' , DRDT: ' +str(DRDT.mean()), fontsize=26)
    plt.plot(DRDT)

plt.show()
'''