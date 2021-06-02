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
from scipy.optimize import curve_fit


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
    for spp in range(1,501):
        p=computeProbability_spp(data[cellID],spp)
        if(p!=-1):
            P.append(p)
            SPP.append(spp)
            
    return (P,SPP)
    
# return a list of all the 16 couples [P,spp] (see utility.XYtoID() for order)
def compute_probabilities(resultFilePath):
    thresholds=[]
    for i in range(16):
        thresholds.append(compute_probability(i,resultFilePath))
    
    return thresholds

# logistic function
def sigmoid(x,x0, k):
    y = 1 / (1 + np.exp(k*(x-x0)))
    return (y)

# fits a logistic function to dataX and dataY
def fit_logisticFunction(dataX,dataY):
    p0 = [np.median(dataX),1] # this is an mandatory initial guess
    upBounds=[500,np.inf]
    lowBounds=[1,0]
    popt, pcov = curve_fit(sigmoid,dataX, dataY,p0, method='trf',maxfev=5000,bounds=(lowBounds,upBounds))
    return (popt, pcov)

# return a list of the perceptive thresholds (refers to the image ID)
# threshold_spp = 20*(threshold_ID+1)
def compute_thresholds(resultFilePath):
    result = compute_probabilities(resultFilePath)
    T=[]
    for i in range(4):
        for j in range(4):
            dataX = result[i+4*j][1]
            dataY = result[i+4*j][0]
            #logistic curve fitting
            params, cov = fit_logisticFunction(dataX,dataY)
            print(str(i)+","+str(j)+":")
            if(cov[0,0] == np.inf):
                print("unable to fit")
                T.append(1)
            else:
                print("parameters = ")
                print(params)
                print("perr  = ")
                print(np.sqrt(np.diag(cov)))
             
                T.append(int(np.round(params[0])))
            print("")
    return T
    
# show the probability plots and threshold values
def showResult(resultFilePath):
    result = compute_probabilities(resultFilePath)
    
    fig, axes = plt.subplots(4,4, sharex=True, sharey=True)
    fig.suptitle(resultFilePath, fontsize=16)
    for i in range(4):
        for j in range(4):
            dataX = result[i+4*j][1]
            dataY = result[i+4*j][0]
            #logistic curve fitting
            params, cov = fit_logisticFunction(dataX,dataY)
            print(str(i)+","+str(j)+":")
            if(cov[0,0] == np.inf):
                print("unable to fit")
            else:
                print("parameters = ")
                print(params)
                print("perr  = ")
                print(np.sqrt(np.diag(cov)))
                X = np.linspace(1,501,501)
                Y = sigmoid(X,params[0],params[1])
                axes[i,j].plot(X,Y,"r",linewidth=1)
                axes[i,j].plot(params[0],0.5,"rx")
                axes[i,j].axvline(params[0],ls="--",color="r",ymin=0,ymax=0.5,linewidth=0.5)
                axes[i,j].set_xlabel("seuil("+str(i)+","+str(j)+")="+str(20*int(np.round(params[0])+1))) 
            print("")
            #data points

            axes[i,j].set_ylim([0,1.05])
            axes[i,j].plot(dataX,dataY,"k.")
            
#    plt.setp(axes[-1, :], xlabel='spp')
    plt.setp(axes[:, 0], ylabel='P_detection(spp)')

    plt.show()

# generate an image made of all the threshold images
def show_thresholdImage(resultFilePath,imgDataBasePath):
    T = compute_thresholds(resultFilePath)
    sceneName=resultFilePath.replace("data/p3d_","").replace("_results.log","")
    side = "right"
    imgOut=Image.new('RGB', (800, 800))
    for i in range(4):
        for j in range(4):
            print((i,j))
            
            im = Image.open(imgDataBasePath+"/p3d_"+sceneName+"-"+side+"/p3d_"+sceneName+"-"+side+"_"+  str(T[i+4*j]).zfill(5) +".png")
            region = im.crop((i*200, j*200, (i+1)*200, (j+1)*200))
            
            imgOut.paste(region,(i*200, j*200))
    imgOut.show()
    imgOut.save("output.png")

path="data/p3d_arcsphere_results.log"
#path="data/p3d_contemporary-bathroom_results.log"
#path="data/p3d_caustic-view0_results.log"
#path="data/p3d_crown_results.log"
#path="data/p3d_indirect_results.log"
show_thresholdImage(path,"E:/image")
showResult(path)








