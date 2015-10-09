# -*- coding: utf-8 -*-
"""
Created on Mon May  4 14:22:07 2015

@author: Michel Tossaint
"""
import glob
import os
import time

FileNames = glob.glob('data_*.csv')
for File in FileNames:
    command = "python heatmap.py --ytick 60s "+File+" power"+File[4:16]+".png"
    print (time.strftime("%Y-%m-%d %H:%M:%S ") + command)
    os.system(command)
