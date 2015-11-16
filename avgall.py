#!/usr/bin/env python

import os
import glob
import sys

listnames =  glob.glob('DataFFT*')

for files in listnames:
    os.system('average.py '+files+' 100')
