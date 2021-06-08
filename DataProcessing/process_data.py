import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from scipy.special import expit

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

# format data into 2 arrays: dataX(SPP) and dataY(detectedLabel)
def sortDataToXY(resultFilePath):
    result=sort_data(resultFilePath)
    R=[]
    for r in range(16):
        dataX=[]
        dataY=[]
        for i in range(len(result[r])):
            dataX.append(result[r][i][0])
            dataY.append(result[r][i][1])
        R.append((dataX,dataY))
    return R

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
            
    return (SPP,P)
    
# return a list of all the 16 couples [P,spp] (see utility.XYtoID() for order)
def compute_probabilities(resultFilePath):
    thresholds=[]
    for i in range(16):
        thresholds.append(compute_probability(i,resultFilePath))
    
    return thresholds

# sigmoid function
def sigmoid(x):
    #y = 1 / (1 + np.exp(-x))
    y=expit(x)
    return y

# logistic function
def logistic(x,k,x0):
    y = 1 / (1 + np.exp(k*(x-x0)))
    return y

def logistic_likelihood(x,*args):
    THETA = x
    X=np.asarray(args[0],dtype=np.float32)
    Y=np.asarray(args[1],dtype=np.float32)
    S=0
    epsilon = 1e-1
    for i in range(len(args[0])):
        Sig=sigmoid(THETA[0]*(X[i]-THETA[1]))
        logSig=np.log(Sig+epsilon)
        logOneMinusSig=np.log(1.0-Sig+epsilon)
        S=S+((Y[i]*logSig) + ((1-Y[i])*logOneMinusSig))
    return S

# fits a logistic function to dataX and dataY
# uses Maximood likelihood Estimation
def fit_logisticFunction_MLE(dataX,dataY):
    # initial guess
    x0 = [1,np.median(dataX)]
    # bounds for k and x0
    l_u_bounds = [(0,2),(1,500)]
    res = minimize(logistic_likelihood,x0,args=(dataX,dataY),bounds=l_u_bounds)
    return res.x

