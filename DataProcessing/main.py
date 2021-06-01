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
import matplotlib.pyplot as plt

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
# return a list of list. Each list contains all the patches in this image section (see utility.XYtoID() for order)
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

# given a list of all patch in a given image portion, compute the probablity for sampling spp
# data=[[spp,detected],[spp,detected],...]
def computeProbability_spp(data,spp):
    N=0
    P=0
    for i in range(len(data)):
        if(data[i][0] == spp):
            N = N + 1
            P = P+data[i][1]
    if N != 0:
        P=P/N
    else:
        P=-1
    return P

# compute probability of detection for each spp level
# return [array P, array SPP]
def compute_probability(cellID,resultFilePath):
    data = sort_data(resultFilePath)
    
    P=[]
    SPP=[]
    

    for spp in range(1,150):
        P.append(computeProbability_spp(data[cellID],spp))
        SPP.append(spp)
            
    return (P,SPP)
    
# return a list of all the 16 couples [P,spp] (see utility.XYtoID() for order)
def compute_probabilities(resultFilePath):
    thresholds=[]
    for i in range(16):
        thresholds.append(compute_probability(i,resultFilePath))
    
    return thresholds


# TODO
def showResult(resultFilePath):
    result = compute_probabilities(resultFilePath)
    
    fig, axes = plt.subplots(4,4, sharex=True, sharey=True)
    for i in range(4):
        for j in range(4):
            axes[i,j].set_ylim([0,1.05])
            axes[i,j].plot(result[i+4*j][1],result[i+4*j][0],".")

    plt.show()
    


#process_log("../ExperimentData/Resultats 20052021")
#print(compute_threshold("data/p3d_arcsphere_results.log"))
showResult("data/p3d_contemporary-bathroom_results.log")

