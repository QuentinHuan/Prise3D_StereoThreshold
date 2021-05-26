# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 11:43:03 2021

@author: Quentin
"""
import process_log as pl
import utility as u
import os
import time

print("##########################")
print("  begin data processing   ")
print("##########################")
path="../ExperimentData/Resultats 20052021"
# list all .log files in PATH
logs=u.listFiles(path,[".log"])
print(str(len(logs))+" .log files detected in " + path)

# clean all logs file (remove all the irrelevant UE4 system logs)
for f in logs:    
    pl.prune_logFile(path,f)
print("-------------------------")
print("cleaning all files done")
print("-------------------------")
print("")
path="logs"
# list all .log files in ./logs
logs=u.listFiles(path,["prune_"])
print(str(len(logs))+" clean .log files detected in "+ path)

# split log files by scene
for f in logs: 
    pl.split_logFile(path,f)
print("-------------------------")
print("split all files by scene done")
print("-------------------------")
print("")

# analyze each files
logs=u.listFiles(path,[".log"])
print(str(len(logs))+" files in "+ path)
for f in logs: 
    pl.analyze_logFile(path,f)

print("-------------------------")
print("file annalysis done   ")
print("-------------------------")
print("")
