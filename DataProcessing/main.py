# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 11:43:03 2021

@author: Quentin
"""
import process_log as pl
import utility as u
import os
import time
import shutil
import errno
import glob

import numpy as np
from PIL import Image

# process log files located in logPath
# save the dataset in ./data
def process_log(logPath):
    
    print("##########################")
    print("  begin data processing   ")
    print("##########################")
    path=logPath
    # list all .log files in PATH
    logs=u.listFiles(path,[".log"])
    print(str(len(logs))+" .log files detected in " + path)
    
    # remove old files
    files = glob.glob('./results/*')
    for f in files:
        os.remove(f)
       
    # ------------------------------------
    # clean all logs file (remove all the irrelevant UE4 system logs)
    # ------------------------------------
    for f in logs:   
        pl.prune_logFile(path,f)
    
    print("cleaning all files done")
    print("")
    path="data"
    
    # list all .log files in ./logs
    logs=u.listFiles(path,["prune_"])
    print(str(len(logs))+" clean .log files detected in "+ path)
    
    # ------------------------------------
    # split log files by scene
    # ------------------------------------
    for f in logs: 
        pl.split_logFile(path,f)
    
    print("split all files by scene done")
    
    # ------------------------------------
    # analyze each files
    # ------------------------------------
    logs=u.listFiles(path,[".log","_2"])
    print(str(len(logs))+" files in "+ path)
    i=0
    for f in logs: 
        pl.analyze_logFile(path,f)
        i=i+1
        print("file annalysis : "+str(i)+"/"+str(len(logs)))
    
    print("-------------------------")
    print("file annalysis done   ")
    print("-------------------------")
    
    # ------------------------------------
    # get scenelist
    # ------------------------------------
    logs=u.listFiles(path,[".log"])
    sceneList=[]
    for f in logs:
        name = f.split("_20")[0] 
        if name not in sceneList:
            sceneList.append(name)
    
    # ------------------------------------
    # merge files by scene
    # ------------------------------------
    logs=u.listFiles(path,[".log","results"])
    pl.merge_logFile(path,sceneList)

    logs=u.listFiles(path,[".log"])
    for f in logs:
        print("generated: " + f)


# sort the data of the scene 'sceneName'
# return a list of list of all the detected sample for each patch (see utility.XYtoID() for order)
# generate the dataset by using process_log() before hand
def sort_data(resultFilePath):
    path="data"
    thresholds=[[] for i in range(16)]
    with open(resultFilePath,"r") as F:
        data = F.readlines()
        for l in data:
            l=l.replace("\n","")
            lSplit=l.split(";")
            
            ID=int(float(lSplit[0]))
            spp=int(float(lSplit[1]))
            detected=int(float(lSplit[2]))
            
            thresholds[ID].append([spp,detected])
    return thresholds





#TODO

# compute the perceptive thresholds for the scene 'sceneName'
# return a list of 4x4 int (see utility.XYtoID() for order)
# generate the dataset by using process_log() before hand
def compute_threshold(resultFilePath):
    path="data"
    thresholds=[[] for i in range(16)]
    with open(resultFilePath,"r") as F:
        data = F.readlines()
        for l in data:
            l=l.replace("\n","")
            lSplit=l.split(";")
            if(lSplit[2] == "1"):
                ID=int(float(lSplit[0]))
                spp=int(float(lSplit[1]))
                detected=int(float(lSplit[2]))
                thresholds[ID].append(0)
    return thresholds
    
# TODO
def showResult(resultFilePath):
    result = sort_data(resultFilePath)
    print(result)
    


#process_log("../ExperimentData/Resultats 20052021")
#print(compute_threshold("data/p3d_arcsphere_results.log"))
showResult("data/p3d_contemporary-bathroom_results.log")

