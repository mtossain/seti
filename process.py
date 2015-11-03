import time
import struct
import numpy as np
import subprocess
import os
import xml.dom.minidom
import math
import datetime
from datetime import datetime
import mysql.connector
from array import array

###############################################################################
# Configuration variables

Receiver = 'rtlsdr'
FFTSize=1024 #Number of FFT bins
fc=1420e6 #Center frequency
fs=3.2e6 #Sampling rate
DataDir = '/media/michel/SETI/' # Where to put recorded files
UpdateRateFFTFiles = 15*60 # In seconds
ThresholdPower = -100 # Threshold for power detection
NumSamplesRecord = 10e6 # Number of IQ samples to record

###############################################################################
# Derived parameters from configuration

RBW = fs / FFTSize # Resolution bandwidth
StartFreq = fc - FFTSize / 2 * RBW # Start frequency FFT

###############################################################################
def UploadAlarmDB(FileName):

    # Upload it to the database
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cnx = mysql.connector.connect(host="panyagua.nl", # your host, usually localhost
	        port=3306, # port name
	        user="seti", # your username
	        passwd="seti1", # your password
	        database="seti") # name of the data base
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO candidates (DateTimeInsert, DishLocation, DataFileName) " +
		                  "VALUES ('" + now + "','" + 'Ijsselstein' + "','" + FileName + "')")
        cnx.commit()
        cursor.close()
        cnx.close()
        print('Data uploaded to database [OK]')
    except mysql.connector.Error as err:
        print(err)
        print("Could not connect to database [NOK]")
     
                
###############################################################################
# Main
    
# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse("mask.xml")
collection = DOMTree.documentElement
if collection.hasAttribute("Mask"):
   print ("Root element : %s" % collection.getAttribute("Mask"))

# Get all the masks in the collection
Masks = collection.getElementsByTagName("MaskEntry")
MaskStart=[]
MaskStop=[]
for Mask in Masks: 
   StartFreqMHz = Mask.getElementsByTagName('StartFreqMHz')[0]
   print ("StartFreqMHz: %s" % StartFreqMHz.childNodes[0].data)
   StopFreqMHz = Mask.getElementsByTagName('StopFreqMHz')[0]
   print ("StopFreqMHz: %s" % StopFreqMHz.childNodes[0].data)
   MaskStart.append(float(StartFreqMHz.childNodes[0].data))
   MaskStop.append(float(StopFreqMHz.childNodes[0].data))

# Convert from Mask array to FFT bin array
MaskOut=[]
for i in range(0,FFTSize):
	Frequency = round(StartFreq + i * RBW) / 1e6
	for j in range (0,len(MaskStart)):
		if (Frequency > MaskStart[j]) and (Frequency < MaskStop[j]):
			MaskOut.append(-10) # Offset value to apply
		else:
			MaskOut.append(0)


os.system('mknod MYPIPEFFT p') # Make a named pipe on Linux
p = subprocess.Popen('exec python collect_gnu.py', stdout=subprocess.PIPE, shell=True) # Start recording with gnuradio top_block.py
FileHandleFFTin = open ("MYPIPEFFT", "rb") # Open the pipe

PowerSpectrum = range(0,FFTSize)
FileNameOut = DataDir+datetime.now().strftime("%Y/%Y%m%d")+'/DataFFT_'+datetime.now().strftime("%Y%m%d_%H%M%S"+'.bin')
FileHandleFFTout = open (FileNameOut, "w+b")
while True:   
    
    PowerSpectrum = struct.unpack('f'*FFTSize, FileHandleFFTin.read(4*FFTSize)) # float is 4 bytes
    
    if (int(time.strftime("%M"))*60+int(time.strftime("%S"))) % UpdateRateFFTFiles ==0:
        FileHandleFFTout.close() # close current file
        FileNameOut = DataDir+datetime.now().strftime("%Y/%Y%m%d")+'/DataFFT_'+datetime.now().strftime("%Y%m%d_%H%M%S"+'.bin')
        FileHandleFFTout = open (FileNameOut, "w+b") # open new file
        time.sleep(1)
            
    if len(PowerSpectrum)>0:
            
        PowerSpectrum = np.roll(PowerSpectrum, FFTSize/2) # FFTW produces half offset FFT
        for i in range(0,FFTSize):
            PowerSpectrum[i]=PowerSpectrum[i]+MaskOut[i] # Take out the premask
        float_array = array('d', PowerSpectrum) # Apparently fastest way to write binary array to file
        float_array.tofile(FileHandleFFTout) # Write to fft output file
        MaxPower = np.amax(PowerSpectrum) # Find the strongest signal
        print('Read FFT, average: '+str(MaxPower))
        
        if MaxPower > ThresholdPower: # Signal detected
            
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Signal detected at :'+str(MaxPower))
            p.kill()
            FileNameRecord = DataDir +datetime.now().strftime("%Y/%Y%m%d")+ '/SigDet_'+ datetime.now().strftime("%Y%m%d_%H%M%S"+'.bin')
            if Receiver=='rtlsdr':
                os.system('rtl_sdr '+FileNameRecord+' -n '+str(NumSamplesRecord)+' -f '+str(fc)+' -s '+str(fs))
            if Receiver=='airspy':
                os.system('airspy_rx '+FileNameRecord+' -n '+str(NumSamplesRecord)+' -f '+str(fc)+' -s '+str(fs))
            p = subprocess.Popen('exec python collect_gnu.py', stdout=subprocess.PIPE, shell=True)
            UploadAlarmDB(FileNameRecord)
            time.sleep(3)
            
FileHandleFFTin.close()
FileHandleFFTout.close()
