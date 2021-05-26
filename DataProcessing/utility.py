# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 11:12:09 2021

@author: Quentin
"""
import sys
from time import sleep
import os

    
# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "="*block + " "*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
    
# return a list of the name of all the files in path
# with all the strings in lookFor in their name
def listFiles(path,lookFor):
    fileList = os.listdir(path)
    matching=[]
    for f in fileList:
        condition=1
        for i in range(len(lookFor)):
            if lookFor[i] not in f:
                condition=condition*0
        if condition==1:
            matching.append(f)
    return matching
            
            
