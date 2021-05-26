import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import fileinput
import os
import utility
import sys

#distance function
def phi(blockPos, gazePos, size):
    out = []
    
    for i in range(size):
        v = blockPos[i,:] - gazePos[i,:]
        r = np.max(np.abs(v))
        out.append(r)

    return np.asarray(out).astype(np.float64)

# convert (X,Y) position (0.0 to 1.0) into 0-15 id (represents a 4x4 grid)
#
#    0-------------------> [x=1]
#    | ------------------
#    | | 0 | 1 | 2 | 3  |
#    | ------------------
#    | | 4 | 5 | 6 | 7  |
#    | ------------------
#    | | 8 | 9 |10 |11  |
#    | ------------------
#    | |12 |13 |14 |15  |
#    | ------------------
#    V [y=1]
def XYtoID(position):
    x=position[0]
    y=position[1]
    
    x=np.ceil((x+0.05)*4 -1)
    y=np.ceil((y+0.05)*4 -1)
    
    
    return np.abs(x+(4*y))

# removes all the irrelevant text from the log file
# save the clean file in ./logs/prune_filename.log
# path is the path to the source log files
def prune_logFile(path,fileName):
    file = open(path+"/"+fileName, 'r')
    Lines = file.readlines()
    
    outFile = open("logs/prune_"+fileName,"w")
    
    for l in Lines:
        if( (l[0] != "#") and ("p3d:" in l) and ("p3d:FIN" not in l) ):
            outFile.write(l.split("p3d:")[1])
    outFile.close()
    file.close()


# should be executed after prune_logFile()
# split the file by scenes: prune_file.log ==> scene1_file.log, scene2_file.log ...
# each line is : timestamp;patchPos.X patchPos.Y;gazePos.X gazePos.Y;spp;detected
def split_logFile(path,fileName):
    #check correct file
    if("prune_" not in fileName):
        print("incorrect file: "+fileName)
        print("split_logFile() should be executed after prune_logFile()")
        
    else:
        file = open(path+"/"+fileName, 'r')
        Lines = file.readlines()
        fileName_striped = fileName.replace("prune_","") #remove prune_
        fileName_striped = fileName_striped.replace("P3d_Expe1-backup-","") #remove prune_
        scene = "NULL"
        for l in Lines:
            l_split = l.split(";")
            #detect scene change: create scene_filename.log
            if( l_split[0] != scene):
                if(scene !="NULL"):
                    outFile.close()
                scene = l_split[0]
                outFile = open("logs/"+scene+"_"+fileName_striped,"w")
            #rewrite without the scene name at the begining of each line
            outFile.write(l.replace(l_split[0]+";",""))
        outFile.write("-1;X=-1 Y=-1;X=-1 Y=-1;-1;0")
        outFile.close()
        file.close()
        os.remove(path+"/"+fileName)

# should be executed after split_logFile()
# for each patch, write down in the file: cellID;spp;bDetected(1 or 0)
def analyze_logFile(path,fileName):
    file = open(path+"/"+fileName, 'r')
    Lines = file.readlines()
    
    # ARRAYS
    T = [] # timestamps
    blockPos = []
    gazePos = []
    spp = [] 
    detected = [] # vive controller trigger press (1 if pressed, 0 otherwise)
    
    # DATA EXTRACTION
    for l in Lines:
        #split on ";"
        split = l.split(";")
        t = split[0]
        
        patchPos =  split[1].split(" ")
        patchX = patchPos[0].split("=")[1]
        patchY = patchPos[1].split("=")[1]

        gaze = split[2].split(" ")
        gazeX = gaze[0].split("=")[1]
        gazeY = gaze[1].split("=")[1]

        detect = int(split[4])

        T.append(t)
        blockPos.append((patchX,patchY))
        gazePos.append((gazeX,gazeY))
        spp.append(split[3])
        detected.append(detect)
    # convert to array
    blockPos = np.asarray(blockPos).astype(np.float64)
    gazePos = np.asarray(gazePos).astype(np.float64)
    T = np.asarray(T).astype(np.float64)
    spp = np.asarray(spp).astype(np.float64)
    PHI = phi(blockPos,gazePos,blockPos.shape[0])
    detected = np.asarray(detected).astype(np.float64)
    
    # DATA PROCESSING
    R=[]
    previousSpp=0
    previousID=0
    bDetected=0
    score=0
    for i in range(T.size):
        #detect block change: save result
        if( XYtoID(blockPos[i]) != previousID or spp[i] != previousSpp ):
            if score > (0.5/0.01): #detected for more than 0.5 second
                bDetected=1
            if (15 >= previousID and previousID >= 0 and i>0):
                R.append(str(previousID)+";"+str(previousSpp)+";"+str(bDetected)+"\n")
            bDetected=0
            score=0
        else:
            if PHI[i]<=0.25 and detected[i]==1:
                score=score+1
                
        previousSpp=spp[i]
        previousID=XYtoID(blockPos[i])
        
    
    # save into file
    file.close()
    file = open(path+"/"+fileName, 'w')#erase file
    file.writelines(R)
    file.close()
    return 0


### TO BE DELETED
def parse_logFile(path,fileName,save):
    
    file = open(path+"/"+fileName, 'r')
    Lines = file.readlines()
    
    sceneName=""
    
    T = []
    blockPos = []
    gazePos = []
    spp = []
    detection = []
    
    #sampling freq
    fs = 1/0.01
    #patch movement freq
    f = 4
    maxSpp=500
    patchSize = 0.2
    #aspect ratio
    ar = 1920/1080
    
    #distance function
    def phi(blockPos, gazePos, size):
        out = []
        
        for i in range(size):
            v = blockPos[i,:] - gazePos[i,:]
            v[0] = v[0] * ar
            p = 2
            r = np.power(v[0]**p + v[1]**p,1/p)
            out.append(r)
    
        return np.asarray(out).astype(np.float64)
    
    ##--------------------------------------------
    ##              main script
    ##--------------------------------------------
    #-----------------
    #parse log file
    #-----------------
    i = 0
    for l in Lines:
        if(l[0] != "#" and "p3d" in l):
            #extract data
            l=l.split("p3d:")[1]
            #split on ";"
            split = l.split(";")
            sceneName = split[0]
            t = split[1]
            patchPos =  split[3].split(" ")
            patchX = patchPos[0].split("=")[1]
            patchY = patchPos[1].split("=")[1]
    
            gaze = split[2].split(" ")
            gazeX = gaze[0].split("=")[1]
            gazeY = gaze[1].split("=")[1]
    
            detect = int(split[5])
    
            T.append(t)
            blockPos.append((patchX,patchY))
            gazePos.append((gazeX,gazeY))
            spp.append(split[4])
            detection.append(detect)
            i=i+1
    
    print("--------------------")
    print("processing scene <" + sceneName + ">")
    print("--------------------")
    # convert to array
    blockPos = np.asarray(blockPos).astype(np.float64)
    gazePos = np.asarray(gazePos).astype(np.float64)
    T = np.asarray(T).astype(np.float64)
    spp = np.asarray(spp).astype(np.float64)
    PHI = phi(blockPos,gazePos,blockPos.shape[0])
    detection = np.asarray(detection).astype(np.float64)
    
    #-----------------
    #processing
    #-----------------
    #number of samples in a patch lifetime
    N = int(f*fs)
    
    # saturation: if gaze point is near enough, score = 1
    # else score = 0 
    score = []
    for i in range(T.size):
        
        if(PHI[i]<patchSize):
            #score.append( (1 - (PHI[i]/np.sqrt(1+(ar*ar)))) * detection[i] )
            score.append( (1 - (PHI[i]/patchSize)) * detection[i] )
        else:
            score.append(0)
        #sleep(0.0001)
    #convert to array
    score = np.asarray(score)
    
    #---------------------------
    #create data structs
    #---------------------------
    
    print("agregating results...")
    dataStructs = []
    
    currentSpp = 0
    lastSpp = -1
    
    s = []
    #score
    for t in range(T.size):
        currentSpp = spp[t]
        #new patch, save current one
        if(currentSpp != lastSpp):
            if(len(s) > 0):
                dataStructs.append(data(blockPos[t,0],blockPos[t,1],lastSpp,max(s)))
                s = []
        else:
            s.append(score[t])
        
        lastSpp = currentSpp

    #   gaze position when detecting
    gazeDetect = []
    for i in range(detection.size):
        if(detection[i]==1):
            gazeDetect.append(gazePos[i])
    

    #---------------------------
    #save detecting gaze position into database
    #---------------------------
    filename = sceneName + "_Gaze.txt"
    filename = os.path.join("results",filename)
    if(save):
        if(os.path.exists(filename)):
            F = open(filename,"a")
        else:
            F = open(filename,"w")
    
        for i in range(len(gazeDetect)):
            F.write(str(gazeDetect[i][0]) + ";" + str(gazeDetect[i][1]) + ";\n")
    
        print("results saved into <"+filename+">\n")
        F.close()
    else:
        print("results discarded\n")


    #---------------------------
    #save result into database
    #---------------------------
    filename = sceneName + "_Data.txt"
    filename = os.path.join("results",filename)
    if(save):
        if(os.path.exists(filename)):
            F = open(filename,"a")
        else:
            F = open(filename,"w")
    
        for i in range(len(dataStructs)):
            F.write(dataStructs[i].toString())
    
        print("results saved into <"+filename+">\n")
        F.close()
    else:
        print("results discarded\n")

