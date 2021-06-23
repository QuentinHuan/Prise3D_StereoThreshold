import os
import sys


# modify param in a .pbrt scene file
def changeParam(filePath,paramName,paramValue):
    # read
    with open(filePath, 'r') as F:
        filedata = F.readlines()
    
    # replace param
    fileOut=""
    for s in filedata:
        #integer
        if(paramName.split(" ")[0]=="integer"):
            if(paramName in s):
                fileOut=fileOut+"\""+paramName+"\" ["+paramValue+"]\n"
            else:
                fileOut=fileOut+s
        #string
        else:
            if(paramName in s):
                fileOut=fileOut+"\""+paramName+"\" \""+paramValue+"\"\n"
            else:
                fileOut=fileOut+s
    
    # write back
    with open(filePath, 'w') as F:
        F.write(fileOut)

