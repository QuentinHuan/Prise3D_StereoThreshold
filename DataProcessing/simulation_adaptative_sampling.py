from time import sleep
from numpy.random import random
import process_data as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import sys

# simulate an stimulus response
# at spp sample
# response follows a logistic probability distribution of parameters (k,x0)
def newObservation(spp,k,x0):

    e=np.random.binomial(1, 0.05, 1)[0]
    p=pd.sigmoid(-k*(spp-x0))

    obs=np.random.binomial(1, p, 1)[0]
    if e==1:
        obs=abs(obs-1)
    return obs

# simulate the whole MLE threshold seeking procedure
# x0_ref and k_ref the real values of the parameters to estimate
# N the amount of step to simulate
def MLE_simulation(x0_ref,k_ref,N):
    X=[250]
    Y=[]
    X0_estimated=0
    k_estimated=0
    dataX=[]
    dataY=[]
    for i in range(N):
        # simulate test result
        obs = newObservation(X[i],k_ref,x0_ref)
        Y.append(obs)

        # convert to float 32
        dataX=np.asarray(X,dtype=np.float32)
        dataY=np.asarray(Y,dtype=np.float32)

        # fit new logistic curve to data
        params = pd.fit_logisticFunction_MLE(dataX[0:i+1],dataY)
        X0_estimated=params[1]
        k_estimated=params[0]

        # next stimulus will be at estimated threshold
        X.append(int(X0_estimated))

    return [X0_estimated,k_estimated,dataX,dataY]

# launch a batch MLE threshold seeking procedure to evaluate precision
# B is the amount of procedures to simulate
# N is the number of observation per procedure
def test_MLE_procedure(B,N,bShowPlots):

    dataX=[]
    dataY=[]
    ERROR_X0_MLE=[]
    ERROR_K_MLE=[]
    print("simulation running...")
    for i in range(B):
        SPP=np.random.randint(1,500,(N))
        k_ref=5*np.random.random()
        x0_ref=np.random.randint(3,500)

        x0_estimated, k_estimated,dataX ,dataY = MLE_simulation(x0_ref,k_ref,N)

        ERROR_X0_MLE.append(abs(int(x0_estimated)-x0_ref))
        ERROR_K_MLE.append(abs(k_estimated-k_ref))
        
        sys.stdout.write((str((int((i/B)*100)))+ "%\r"))

    print("-----------------------------------")
    print("RESULTS : ")
    print("-----------------------------------")
    print("number of simulations = "+str(B))
    print("number of observations per simulations = "+str(N))
    print("")
    print("mean X0 error = "+str(np.mean(ERROR_X0_MLE)))
    print("median X0 error = "+str(np.median(ERROR_X0_MLE)))
    print("")
    print("mean K error = " + str(np.mean(ERROR_K_MLE)))
    print("median K error = " + str(np.median(ERROR_K_MLE)))
    print("-----------------------------------")

    if(bShowPlots==True):
        fig, axs = plt.subplots(2,1)

        # fit and data
        X=np.linspace(0,500,1000)

        Y_fit=pd.sigmoid(-k_ref*(X-x0_ref))
        axs[0].plot(X,Y_fit,"g")

        for i in range(N):
            Y_fit=pd.sigmoid(-k_estimated*(X-int(x0_estimated)))
            axs[0].plot(X,Y_fit,color=(1,0,0,0.1))
            axs[0].plot(dataX,dataY,"kx")
            if(i==N-1):
                axs[0].plot(X,Y_fit,"--",color=(1,0,0,1))
            #plt.pause(0.1)
        
        axs[1].plot(ERROR_X0_MLE,"k.")

        plt.show()
    return np.mean(ERROR_X0_MLE)

B=200
L=[10,20,30,40,50]
result=[]
for N in L:
    result.append(test_MLE_procedure(B,N,False))

fig, axs = plt.subplots(1,1)
axs.plot(L,20*np.asarray(result),"k")
axs.set_xlabel("number of observations")
axs.set_ylabel("threshold estimation precision (in spp)")
plt.show()