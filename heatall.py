#!/usr/bin/env python

import os
import glob
import sys

listnames =  glob.glob('DataFFT*')

for files in listnames:
    os.system('heatmap.py '+files+' 0 10000')
    os.system('mv data_fftaverage.jpg data_fftaverage_' + files[8:19]+'.jpg')
    os.system('mv data_heatmap.jpg data_heatmap_' + files[8:19]+'.jpg')
