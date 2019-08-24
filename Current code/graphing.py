import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from tc3omega.datareader import Data  # reads data from .csv
from tc3omega.constants import Constants  # read sample data from .yml
from tc3omega.analysis import Analyzer  # fits linear approx. or 2D model
from tc3omega.logmaker import Logmaker  # creates plots and log files


def check_zeros(datas):
	'''makes sure any dataset parameter does not contain 0 or NaN'''
	for i,dat in enumerate(datas):
		if np.isnan(dat) or dat == 0:
			datas = datas[:i]
			return datas
	return datas


def graph_multivolt(data):
	'''data is a list of [lc_list, v3w_x, v3w_avg, v1w_x,v1w_sh_x ,lc_const]
	which is the same as data4ped

	if instead you want to read from a csv file put in the filename and directory'''
	['freq','v3w','v3w_avg','v1w','v1w_sh','volt']
	if type(data) == str:
		data = pd.read_csv(data)
		freqs = data['freq']
		v1w = data['v1w']
		v3w = data['v3w']
		v3w_avg = data['v3w_avg']
		v1sh = data['v1w_sh']
		volts = data['volt'] 
	elif type(data)==list:
		for dat in data:
			freqs,v3w,v3w_avg,v1w,v1sh,volts = data
	else:
		raise TypeError('invalid input')

	freqs = check_zeros(freqs)
	v3w = check_zeros(v3w)
	v1w = check_zeros(v1w)
	v3w_avg = check_zeros(v3w_avg)
	v1sh = check_zeros(v1sh)
	volts = check_zeros(volts)

	n_points = len(freqs)
	n_sweeps = [sweep for sweep in range(int(len(v3w)/n_points))]
	n_lc_const = [volt for volt in range(len(volts))]
	fig = plt.figure()

	for i in range(int(len(v3w)/len(freqs))):
	    plt.errorbar(np.log(freqs),v3w[i*n_points:(i+1)*n_points],fmt='o')

	data = Data('TARA8-SiOx-5.csv')
	
	#get constants from txt file and format them as needed
	constants = Constants.fromFile('siox_si_siox.txt').getvals()
	constants['heater_dRdT']= 0.09

	#provide initial guess and fitting indices
	kappas0 = np.array([1.5, 130, 1.5], dtype=np.double)  # use np.double!
	fit_indices = [0, 1, 2]

	
	#data['sample_V1w_imag'] = np.array([0 for i in avg[0]])
	data['input_frequencies'] = np.array(freqs)
	data['sample_V1w_imag'] = np.array([0 for i in freqs])
	for i in n_lc_const:
	    data['sample_V3w_real'] = v3w[i*n_points:(i+1)*n_points]
	    data['sample_V1w_real'] = v1w[i*n_points:(i+1)*n_points]
	    data['shunt_V1w_real'] = v1sh[i*n_points:(i+1)*n_points]
	    A = Analyzer(constants,data,kappas0,fit_indices,boundary_typ='isothermal')
	    
	    k_film, k_sub = A.LinApproxFit(const_eta=None)
	    LogA = Logmaker(A)
	    LogA.make_LAfit_plot()
	    print('Voltage: ' + str(volts[i]))
	    print("film thermal conductivity: {:.2f}".format(k_film))
	    print("substrate thermal conductivity: {:.2f}".format(k_sub))
	    print()
	print('heater dRdT used:')
	print(constants['heater_dRdT'])
	plt.show()


