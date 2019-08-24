# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 10:30:25 2019

@author: Pedro
"""

import pyvisa as visa

deviceGPIB = '8'
sr830 = visa.Instrument('GPIB::' + deviceGPIB)
deviceID = sr830.ask("SLVL?")
print(deviceID)
