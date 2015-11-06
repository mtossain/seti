
import xml.dom.minidom
import numpy as np

###############################################################################

Receiver = 'rtlsdr'
FFTSize=1024 #Number of FFT bins
fc=1420e6 #Center frequency
fs=3.2e6 #Sampling rate
DataDir = '/media/michel/SETI/' # Where to put recorded files
ThresholdPower = -72 # Threshold for power detection
NumSamplesRecord = 100e6 # Number of IQ samples to record

RBW = fs / FFTSize # Resolution bandwidth
StartFreq = fc - FFTSize / 2 * RBW # Start frequency FFT

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

def UpdateCollectGnuradio(FileNameGnuradio):
    
    f = open(FileNameGnuradio,'r')
    filedata = f.read()
    f.close()

    newdata = filedata.replace("old data","new data")

    f = open(FileNameGnuradio,'w')
    f.write(newdata)
    f.close()    

###############################################################################

test = GetFreqMask('mask.xml')
print(test)

UpdateCollectGnuradio('collect_gnu.py')

    
