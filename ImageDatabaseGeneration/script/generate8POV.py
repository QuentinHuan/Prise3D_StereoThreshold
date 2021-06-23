import os
import sys
import utility as u

print("-----------------------------------")
print("generate 8pov images")
print("-----------------------------------")
print("")
# folder path
sceneFolder="/home/huan/p3d_Stereo_scenes"
outFolderPath="/home/huan/pbrtOut/8pov"
pbrtFolder="/home/huan/git/Stage/pbrt-v4/build"
rawlsToolsFolder="/home/huan/git/Stage/rawls-tools/run"
# parameters
resolution=[720,360]
sppPerImage=20
numberOfImage=10
imageExtention=".rawls"
bGPU=False
#camera selection
numberOfPOV=8

# scenelist
#sceneList=["arcsphere","caustic-view0","contemporary-bathroom","crown"]
sceneList=["crown"]
sceneFilePrefix="8pov_"

namesPrefix="p3d_"

print("looking for scene files in "+sceneFolder)
print("resolution is "+str(resolution))
print("scene list is "+str(sceneList))
print("")

if(not os.path.isdir(outFolderPath+"/rawls")):
    os.mkdir(outFolderPath+"/rawls")
if(not os.path.isdir(outFolderPath+"/png")):
    os.mkdir(outFolderPath+"/png")

for s in sceneList:
    print("rendering: "+sceneFilePrefix+s)
    sceneFilePath=sceneFolder+"/"+s+"/"+sceneFilePrefix+s+".pbrt"
    # set resolution
    u.changeParam(sceneFilePath,"integer yresolution",str(resolution[1]))
    u.changeParam(sceneFilePath,"integer xresolution",str(resolution[0]))

    # render
    for i in range(1,numberOfPOV+1):
        # set view number
        u.changeParam(sceneFilePath,"integer view",str(i))

        # render command
        gpu=" --gpu" if bGPU else ""
        cmd = pbrtFolder+"/pbrt"+gpu+ " --spp "+str(sppPerImage)+" --nimages "+str(numberOfImage)+" --outfile "+namesPrefix+s+imageExtention+" --folder "+outFolderPath+"/rawls"+" "+sceneFilePath
        os.system(cmd)
        
        # merge into .png
        print("merging...")
        cmd="bash "+" reconstruct_png_all_incr.sh "+outFolderPath+"/rawls/"+namesPrefix+s+"-0"+str(i)+" "+outFolderPath+"/png"+" 1"
        os.system("cd "+rawlsToolsFolder+ " && "+cmd)




