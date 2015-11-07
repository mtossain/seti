import matplotlib.pyplot as plt
import numpy as np
import time
import sys
import os
import datetime
from datetime import datetime

###############################################################################
# Configuration variables
FFTSize=2028 #Number of FFT bins
fc=1420e6 #Center frequency
fs=2.4e6 #Sampling rate
RBW = fs / FFTSize # Resolution bandwidth
StartFreq = (fc - FFTSize / 2 * RBW)/1e6 # Start frequency FFT
StopFreq = (fc + FFTSize / 2 * RBW)/1e6 # Start frequency FFT
DataDir = '/media/michel/SETI/'
###############################################################################
# Functions
def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))
###############################################################################
# Main

fig = plt.figure()
ax = fig.add_subplot(111)

# Get last filename of day
files = sorted_ls(DataDir+datetime.now().strftime("%Y/%Y%m%d"))
DataFile = DataDir+datetime.now().strftime("%Y/%Y%m%d/")+files[-1]

# some X and Y data
x=np.zeros(FFTSize)
for i in range(0,FFTSize):
    x[i] = round(StartFreq*1e6 + i * RBW)/1e6 # in MHz
os.system('tail -c '+str(FFTSize*4*2)+' '+DataFile+ ' > datatail.bin')
y = np.fromfile('datatail.bin', dtype=float)
if len(x)==len(y):
    li, = ax.plot(x, y)

# draw and show it
fig.canvas.draw()
plt.grid(b=True, which='both', color='0.65',linestyle='-')
plt.show(block=False)

# loop to update the data
while True:
    try:
        files = sorted_ls(DataDir+datetime.now().strftime("%Y/%Y%m%d"))
        DataFile = DataDir+datetime.now().strftime("%Y/%Y%m%d/")+files[-1]

        os.system('tail -c '+str(FFTSize*4*2)+' '+DataFile+ ' > datatail.bin')
        y = np.fromfile('datatail.bin', dtype=float)

        # set the new data
        if len(x)==len(y):
            li.set_ydata(y)
            ax.relim()
            ax.autoscale_view(True,True,True)
            fig.canvas.draw()
        
        time.sleep(0.5)
    except KeyboardInterrupt:
        break
