#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 09:37:00 2015

@author: Michel Tossaint
"""
import matplotlib.pyplot as plt
import numpy as np
import sys
###############################################################################
# Configuration variables

FFTSize=1024 #Number of FFT bins
fc=1420e6 #Center frequency
fs=3.2e6 #Sampling rate
DataFile = sys.argv[1]
#DataFile = 'data.bin' #Datafile
StartRowAvg = int(sys.argv[2]) #Start row for averaging from 
#StartRowAvg = 0 #Start row for averaging from 
StopRowAvg = int(sys.argv[3]) #Start row for averaging from 
#StopRowAvg = 200 #Start row for averaging from 
my_dpi=96 #Screen dpi


###############################################################################
# Derived parameters from configuration
RBW = fs / FFTSize # Resolution bandwidth
StartFreq = (fc - FFTSize / 2 * RBW)/1e6 # Start frequency FFT
StopFreq = (fc + FFTSize / 2 * RBW)/1e6 # Start frequency FFT

###############################################################################

# Plot the heatmap
PowerSpectrum = range(0,FFTSize)
data = np.fromfile(DataFile, dtype=float)
NumRowsInFile = data.size/FFTSize
if StopRowAvg > NumRowsInFile:
    StopRowAvg=NumRowsInFile
print('Reading file: '+DataFile)
print('Number of rows in file: '+str(NumRowsInFile))
data = data.reshape(NumRowsInFile,FFTSize)
data = data[list(range(StartRowAvg,StopRowAvg)),:]
NumRowsPlot = StopRowAvg - StartRowAvg
fig, ax = plt.subplots(1,1,figsize=(1600/my_dpi, 900/my_dpi), dpi=my_dpi)
heatmap = ax.pcolor(data, cmap=plt.cm.jet)
cbar = plt.colorbar(heatmap) # Colorbar title
cbar.set_label('Power level (dB)', rotation=270) # Colorbar
x1,x2,y1,y2 = plt.axis() # Change limits
plt.axis((x1,FFTSize,y1,NumRowsPlot)) # Change limits
plt.xlabel('FFTbins (-) '+str(StartFreq)+' - '+ str(StopFreq))
fig.savefig('data_heatmap.jpg')

# Plot average of x rows
fig = plt.figure(figsize=(1275/my_dpi, 900/my_dpi), dpi=my_dpi)
meandata = np.mean(data, axis=0)
dum = range(0,FFTSize)
x = [(x*RBW+StartFreq*1e6)/1e6 for x in dum]
plt.plot(x,meandata)
x1,x2,y1,y2 = plt.axis() # Change limits
plt.axis((StartFreq,StopFreq,y1,y2)) # Change limits
plt.xlabel('Frequency')
fig.savefig('data_fftaverage.jpg')
