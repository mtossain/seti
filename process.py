#!/usr/bin/env python

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
import matplotlib.pyplot as plt


###############################################################################
# Configuration variables

fc=1420e6 #Center frequency
fs=3.2e6 #Sampling rate
FFTSize=1024 #Number of FFT bins
DataDir = '/media/michel/SETI/' # Where to put recorded files
ThresholdPower = -50 # Threshold for power detection
Receiver = 'rtlsdr'
NumSamplesRecord = 100e6 # Number of IQ samples to record
DCOffset = 0 # 0 if not used, 1 manual, 2 if automatic
UseAGC = True # True if AGC to be used
Gain = 50 # LNA Gain in receiver
IFGain = 20 # IF Gain in receiver
BBGain = 20 # BB Gain in receiver
FFTFrameRate = 0.5 # How many FFT per second
FFTAverageAlpha = 0.01 # Averaging factor, smaller is more averaging

RBW = fs / FFTSize # Resolution bandwidth
StartFreq = fc - FFTSize / 2 * RBW # Start frequency FFT

###############################################################################

import subprocess as sub
import threading

class RunCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = sub.Popen(self.cmd)
        #self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()      #use self.p.kill() if process needs a kill -9
            self.join()

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

def GetFreqMask(FileNameMask):
    
    MaskOut = [0]*FFTSize # Output list
    
    # Get all masks from XML file
    Masks = xml.dom.minidom.parse(FileNameMask).documentElement.getElementsByTagName("MaskEntry")
       
    # Loop over the masks
    for Mask in Masks:
        
        StartFreqMHz = float(Mask.getElementsByTagName('StartFreqMHz')[0].childNodes[0].data)
        StopFreqMHz = float(Mask.getElementsByTagName('StopFreqMHz')[0].childNodes[0].data)
        Offset = float(Mask.getElementsByTagName('Offset')[0].childNodes[0].data)
        
        # Convert from Mask cell to FFT bin array
        for j in range(0,FFTSize):
            FrequencyMHz = round(StartFreq + j * RBW) / 1e6 # in MHz
            if (FrequencyMHz > StartFreqMHz) and (FrequencyMHz < StopFreqMHz):
                MaskOut[j]=Offset

    return MaskOut

###############################################################################

def UpdateCollectGnuradio(FileNameGnuradioIn, FileNameGnuradioOut):
    
    f = open(FileNameGnuradioIn,'r')
    filedata = f.read()
    f.close()

    filedata = filedata.replace('<SampleRate>',str(int(fs)))
    filedata = filedata.replace('<FFTSize>',str(int(FFTSize)))
    filedata = filedata.replace('<CenterFrequency>',str(int(fc)))
    filedata = filedata.replace('<DCOffset>',str(DCOffset))
    filedata = filedata.replace('<UseAGC>',str(UseAGC))
    filedata = filedata.replace('<Gain>',str(Gain))
    filedata = filedata.replace('<IFGain>',str(IFGain))
    filedata = filedata.replace('<BBGain>',str(BBGain))
    filedata = filedata.replace('<FFTFrameRate>',str(FFTFrameRate))
    filedata = filedata.replace('<FFTAverageAlpha>',str(FFTAverageAlpha))
    
    f = open(FileNameGnuradioOut,'w')
    f.write(filedata)
    f.close()    

###############################################################################

# Main

#RunCmd(["python", "plotfft.py "+str(fc)+" "+str(fs)+" "+str(FFTSize)+" "+DataDir], 10).run()
RunCmd(["python", "plotfft.py",str(fc),str(fs),str(FFTSize),DataDir], 10).run()

MaskOut = GetFreqMask('mask.xml') # Get the frequency masking file to be applied
UpdateCollectGnuradio('collect_gnu_template.py','collect_gnu.py') # Apply configuration settings to gnuradio top_block

os.system('mknod MYPIPEFFT p') # Make a named pipe on Linux
p = subprocess.Popen('exec python collect_gnu.py', stdout=subprocess.PIPE, shell=True) # Start recording with gnuradio top_block.py
FileHandleFFTin = open ("MYPIPEFFT", "rb") # Open the pipe

PowerSpectrum = range(0,FFTSize)
os.system('mkdir '+ DataDir+datetime.now().strftime("%Y/%Y%m%d")) # make directory if does not exist
FileNameOut = DataDir+datetime.now().strftime("%Y/%Y%m%d")+'/DataFFT_'+datetime.now().strftime("%Y%m%d_%H%M%S"+'.bin')
FileHandleFFTout = open (FileNameOut, "w+b")
LastHour = int(time.strftime("%H"))
while True:   
    
    PowerSpectrum = struct.unpack('f'*FFTSize, FileHandleFFTin.read(4*FFTSize)) # float is 4 bytes
    
    if int(time.strftime("%H"))<>LastHour: # Make a new file every hour
        FileHandleFFTout.close() # close current file
        os.system('mkdir '+ DataDir+datetime.now().strftime("%Y/%Y%m%d")) # make directory if does not exist
        FileNameOut = DataDir+datetime.now().strftime("%Y/%Y%m%d")+'/DataFFT_'+datetime.now().strftime("%Y%m%d_%H%M%S"+'.bin')
        FileHandleFFTout = open (FileNameOut, "w+b") # open new file
        LastHour = int(time.strftime("%H"))
            
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
            os.system('mkdir '+ DataDir+datetime.now().strftime("%Y/%Y%m%d")) # make directory if does not exist
            FileNameRecord = DataDir +datetime.now().strftime("%Y/%Y%m%d")+ '/SigDet_'+ datetime.now().strftime("%Y%m%d_%H%M%S"+'.bin')
            if Receiver=='rtlsdr':
                os.system('rtl_sdr '+FileNameRecord+' -n '+str(NumSamplesRecord)+' -f '+str(fc)+' -s '+str(fs))
            p = subprocess.Popen('exec python collect_gnu.py', stdout=subprocess.PIPE, shell=True)
            UploadAlarmDB(FileNameRecord)
            time.sleep(10)
         
            fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
            ax.plot(PowerSpectrum)
            fig.savefig('signal.png')   # save the figure to file
            plt.close(fig)    # close the figure
            
FileHandleFFTin.close()
FileHandleFFTout.close()
