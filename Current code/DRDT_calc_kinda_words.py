"""
I don't know what this is revisit later
"""

from scipy.interpolate import interp1d
import scipy.signal as sig
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#######First read data from files#######

direc = r"C:/Users/Pedro/Dropbox/1-Three Omega with Ara/new_python/3omega-lockin-Pedro/TARA8/New folder"

temp_data = pd.read_csv(direc + '/' + 'temp_28_39.csv')
T = np.array(temp_data['Temp'])
time_T = np.array(temp_data['time'])


volt_data = pd.read_csv(direc +'/'+'avolt_28_39.csv')
V = np.array(volt_data['volt'])
time_V = np.array(volt_data['time'])

shunt_data = pd.read_csv(direc + '/' + 'avsh_28_39.csv')
Vsh = np.array(shunt_data['volt'])
time_Vsh = np.array(shunt_data['time'])
Vsh= Vsh[200:-1]*-1
plt.plot(Vsh)
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

#time = time[100:400]
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

T2 = sig.savgol_filter(T,window_length = len(T),polyorder = 3)

fig1 = plt.figure()
fig1.suptitle('Temp fitted data', fontsize=26)
plt.plot(time_T,T2)

fig2 = plt.figure()
fig2.suptitle('Temp raw data', fontsize=26)
plt.plot(time_T,T)



fig3 = plt.figure()
fig3.suptitle('Resist fitted data', fontsize=26)
plt.plot(time,resist)

fig4 = plt.figure()
fig4.suptitle('Resist raw data', fontsize=26)
plt.plot(time_V,R)


fig5 = plt.figure()
fig5.suptitle('del_r', fontsize=26)
plt.plot(time[:-1],del_r)

fig6 = plt.figure()
fig6.suptitle('del_t', fontsize=26)
plt.plot(time[:-1],del_t)
plt.show()




DRDT = del_r/del_t
DRDT_org = DRDT

fig2 = plt.figure()
fig2.suptitle('raw drdt', fontsize=26)
plt.plot(DRDT_org)

for i in range(20):
    loc_max = np.where(DRDT==DRDT.max())
    DRDT = np.delete(DRDT,loc_max)
    loc_min = np.where(DRDT==DRDT.min())
    DRDT = np.delete(DRDT,loc_min)
    fig3 = plt.figure()
    fig3.suptitle('fix drdt'+str(i) + ' , DRDT: ' +str(DRDT.mean()), fontsize=26)
    plt.plot(DRDT)

plt.show()


DRDT_avg = DRDT.mean()


print('DRDT_avg: ' + str(DRDT_avg))
print('raw DRDT: ' + str(DRDT_org.mean()))
print('DRDT_median: ' + str(np.median(DRDT)))
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