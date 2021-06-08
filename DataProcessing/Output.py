import process_data as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import minimize

# return a list of the perceptive thresholds (refers to the image ID)
# threshold_spp = 20*(threshold_ID+1)
def compute_thresholds(resultFilePath,bUseMLE):
    if(bUseMLE==True):
        result=pd.sortDataToXY(resultFilePath)
    else:
        result = pd.compute_probabilities(resultFilePath)
    T=[]
    dataX=[]
    dataY=[]
    for i in range(4):
        for j in range(4):
            dataX = np.asarray(result[i+4*j][0],dtype=np.float32)
            dataY = np.asarray(result[i+4*j][1],dtype=np.float32)
            #logistic curve fitting
            params, success = pd.fit_logisticFunction(dataX,dataY,bUseMLE)

            
            if(success == 0):
                print("!!! WARNING !!!")
                print("cell "+str(i)+","+str(j)+":")
                print("unable to fit")

            print("cell "+str(i)+","+str(j)+":")
            print("parameters = ")
            print(params)
            T.append(int(params[1]))
    return T
    
# show the probability plots and threshold values
def showResult(resultFilePath,bUseMLE):
    if(bUseMLE==True):
        result=pd.sortDataToXY(resultFilePath)
    else:
        result = pd.compute_probabilities(resultFilePath)

    T = compute_thresholds(resultFilePath,bUseMLE)

    fig, axes = plt.subplots(4,4, sharex=True, sharey=True)
    fig.suptitle(resultFilePath+"_bUseMLE="+str(bUseMLE), fontsize=16)
    for i in range(4):
        for j in range(4):
            dataX = np.asarray(result[i+4*j][0],dtype=np.float32)
            dataY = np.asarray(result[i+4*j][1],dtype=np.float32)
            params = T[i+4*j]

            #logistic curve plot
            X = np.linspace(1,501,501)
            Y = pd.logistic(X,params[0],params[1])
            axes[i,j].plot(X,Y,"r",linewidth=1)
            axes[i,j].plot(params[1],0.5,"rx")
            axes[i,j].axvline(params[1],ls="--",color="r",ymin=0,ymax=0.5,linewidth=0.5)
            axes[i,j].set_xlabel("seuil("+str(i)+","+str(j)+")="+str(20*int(np.round(params[1])+1))) 
            print("")
            #data points plot
            axes[i,j].set_ylim([0,1.05])
            axes[i,j].plot(dataX,dataY,"k.")
    plt.setp(axes[:, 0], ylabel='P_detection(spp)')

# generate an image made of all the threshold images
def show_thresholdImage(resultFilePath,imgDataBasePath,bStereo,bUseMLE):
    T = compute_thresholds(resultFilePath,bUseMLE)
    sceneName=resultFilePath.replace("data/p3d_","").replace("_results.log","")
    side = "right"
    if(bStereo==True):
        imgOut=Image.new('RGB', (800*2, 800))
    else:
        imgOut=Image.new('RGB', (800, 800))
        
    for i in range(4):
        for j in range(4):
            print((i,j))
            side="right"
            im_l = Image.open(imgDataBasePath+"/p3d_"+sceneName+"-"+side+"/p3d_"+sceneName+"-"+side+"_"+  str(T[i+4*j]).zfill(5) +".png")
            region_l = im_l.crop((i*200, j*200, (i+1)*200, (j+1)*200))

            imgOut.paste(region_l,(i*200, j*200))
            
            if(bStereo==True):
                side="left"
                im_r = Image.open(imgDataBasePath+"/p3d_"+sceneName+"-"+side+"/p3d_"+sceneName+"-"+side+"_"+  str(T[i+4*j]).zfill(5) +".png")
                region_r = im_r.crop((i*200, j*200, (i+1)*200, (j+1)*200))
    
                imgOut.paste(region_r,(i*200+800, j*200))
    imgOut.save("./img/Thresh_"+sceneName+"_MLE_"+str(bUseMLE)+".png")