#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 09:37:00 2015

@author: Michel Tossaint
"""
import matplotlib.pyplot as plt
import numpy as np
import sys
import math

###############################################################################
# Configuration variables

FFTSize=1024 #Number of FFT bins
fc=1420e6 #Center frequency
fs=3.2e6 #Sampling rate
DataFile = sys.argv[1] #Name of data file
LenAvg = int(sys.argv[2]) #Start row for averaging from 
my_dpi=96 #Screen dpi

###############################################################################
# Derived parameters from configuration
RBW = fs / FFTSize # Resolution bandwidth
StartFreq = (fc - FFTSize / 2 * RBW)/1e6 # Start frequency FFT
StopFreq = (fc + FFTSize / 2 * RBW)/1e6 # Start frequency FFT

###############################################################################

# Read the data
PowerSpectrum = range(0,FFTSize)
data = np.fromfile(DataFile, dtype=np.float16)
NumRowsInFile = data.size/FFTSize
print('Reading file: '+DataFile)
print('Number of rows in file: '+str(NumRowsInFile))
data = data.reshape(NumRowsInFile,FFTSize)
NumAvg = int(math.floor(NumRowsInFile/LenAvg))
print('Number of averages: '+str(NumAvg))

# Plot average of x rows
for i in range(0,NumAvg):
    datawin = data[list(range(i*LenAvg,(i+1)*LenAvg)),:]
    fig = plt.figure(figsize=(1275/my_dpi, 900/my_dpi), dpi=my_dpi)
    meandata = np.mean(datawin, axis=0, dtype=float)
    dum = range(0,FFTSize)
    x = [(x*RBW+StartFreq*1e6)/1e6 for x in dum]
    plt.plot(x,meandata)
    x1,x2,y1,y2 = plt.axis() # Change limits
    plt.axis((StartFreq,StopFreq,y1,y2)) # Change limits
    plt.xlabel('Frequency')
    fig.savefig('data_fftaverage_'+ DataFile[8:23]+'_'+str(i)+'.jpg')
