from scipy.interpolate import interp1d
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
Vsh =Vsh[220:-1]
Vsh = Vsh*-1
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
time[200:400]
a2,a1,a0 = np.polyfit(time_T,T,2)
b2,b1,b0 = np.polyfit(time_V,R,2)
time=np.array([i*0.1 for i in range(1350)])
temp = a2*time**2 + a1*time + a0
resist = b2*time**2 + b1*time + b0






fig2 = plt.figure()
fig2.suptitle('Temp raw data', fontsize=26)
plt.plot(time_T,T)
plt.plot(time,temp)


fig4 = plt.figure()
fig4.suptitle('Resist raw data', fontsize=26)
plt.plot(time_V,R)
plt.plot(time,resist)

del_r = np.diff(resist)
del_t = np.diff(temp)




fig5 = plt.figure()
fig5.suptitle('del_r', fontsize=26)
plt.plot(time[:-1],del_r)

fig6 = plt.figure()
fig6.suptitle('del_t', fontsize=26)
plt.plot(time[:-1],del_t)


DRDT = del_r/del_t

fig7 = plt.figure()
plt.plot(DRDT)
plt.show()





print('DRDT_avg: ' + str(DRDT.mean()))
print('DRDT_median: ' + str(np.median(DRDT)))

