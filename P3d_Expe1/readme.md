# Open the project:

Download project full [here](https://drive.google.com/file/d/1TRB8mbDN4n1Vy9b0KTbXfPOhJEo_GYa_/view?usp=sharing) (~2Go)
(Opens with UE4.26)

Or start from a blank project (not advised...):

* create a new c++ blank project
* add a new actorComponent c++ class, name it "P3dComponent"
* copy the content of P3dComponent.h and P3dComponent.cpp in corresponding files (Don't forget to replace "P3D_EXPE1_API" by "YOUR_PROJECT_NAME_API").
* rebuild project
* copy the folder Content in the corresponding folder of your Ue4 project
* restart the editor and open Blueprint/Manager
* change the type of component/P3dComponent to P3dComponent
* delete, recreate and relink the blocks Log, Random2d, readFile, and getImagePath
* compile and check for errors
* do the same for Blueprint/ManagerTutorial, and ManagerSpherical 

# Project structure:

3 levels: Main, *StereoThreshold* and *Tutorial*
* Main level blueprint opens either *StereoThreshold* or *Tutorial* depending on the value of ```sceneID``` (value stored in ```.\WindowsNoEditor\P3d_Expe1\Content\data\sceneId.txt```)
* When started, *StereoThreshold* reads the value of ```.\WindowsNoEditor\P3d_Expe1\Content\data\sceneId.txt``` and load the corresponding scene from the list in file ```.\WindowsNoEditor\P3d_Expe1\Content\data\scenes.txt```
* *Tutorial* always opens the scene ```p3d_pavilion```

2 blueprint classes are important: Manager and PawnHMD
* Manager manage the whole experiment: drop it in a level and call StartExperiment() to begin the experiment
* PawnHMD keeps track of user's head direction (forward ray attached to HMD, cast against the manager screen) in UV coordinates. It can be configured to return the gaze direction in spherical coordinates (param ```ActivateSphericalScreen=1```)
* ManagerTutorial is a strip down version of Manager: it won't produce any recordings, and always opens the scene ```p3d_pavilion```

The rendering of the image is taken care of by M_PatchPlane (or M_PatchSphere if using the spherical display option): 
* if using M_PatchPlane, patches will have a square shape (```NoisePatchPos``` in UV coordinate)
* if using M_PatchSphere, patches will have a round shape (```NoisePatchPos``` in spherical coordinate)

When exported, the ```.\WindowsNoEditor\P3d_Expe1\Content\data``` folder should contains 4 files:
* ```config.txt``` (Manager blueprint needs to read this file to load its parameters)
* ```config_tutorial.txt``` (ManagerTutorial blueprint needs to read this file to load its parameters)
* ```sceneId.txt``` (used by Manager bluerprint to open the scene selected in Main level)
* ```scenes.txt``` (list of scene, sceneId correspond to the line of this text file, starting at 0)

The ```packProjectFolder\WindowsNoEditor\P3d_Expe1\Content\script\``` folder is a copy of DataProcessing folder (check readme.md for more info)

Some Blueprint classes call c++ functions: these are implemented in the ```P3dComponent``` class

# MLE sampling strategy

MLE sampling strategy use the previous results (stored in ```.\WindowsNoEditor\P3d_Expe1\Content\script\data```) to compute new noise values to test for each block. This happens at the start of the program (p3d_component will calls ```.\WindowsNoEditor\P3d_Expe1\Content\script\ComputeNewStimulusSet.py``` in a new terminal). If the program holds on when starting a new experiment, check that:
* python version 3 is installed (version 2 does work, but you'll need to manualy close the terminal each time...)
* that the MLE scripts are working properly (see DataProcessing/readme.md for more info)

After the experiment is done, press ```escape``` (or ```menu``` button of the Vive controller) to quit and save the results. 

# Working with the unreal project:

Since the project uses various external ressources, it is advised to package the game everytime you want to test something (alt+P is likely to cause a crash, or missing ressources). A painless way to setup everything is to download the binaries somewhere, and package the project in this folder (UE4 editor will update the files without breaking the folder hierarchy).




