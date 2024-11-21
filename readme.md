Prise3D_StereoThreshold experiment repository: constains source of various tools used during my 2021 internship (LISIC, Calais, France)

Path tracing methods for photorealistic image synthesis allows the production of realistic images from a 3D scene. 
Their progressive nature implies, in many cases, a high number of sample per pixels (spp) to achieve noise free images.
The lower spp limit required to achieve imperceptible noise level is generally highly dependent of the geometry of the scene, its lighting, the materials, etc...  

The goal of this 6-month internship was to measure the perceptive limit for the spp necessary to obtain noise free stereoscopic images observed through a VR headset, and compare it to the perceptive threshold of the same image observed on a regular screen.

# Directories description :

* P3d_StereoThreshold: binary version of experiment \#1 (capture of perceptive thresholds for noisy pathtraced stereo images)
* Image: link to the image dataBase (800x800 .png images, increment of 20 spp per image)
* P3d_StereoThreshold_VR: Ue4 v4.26 project of experiment \#1
* ExperimentData: experimental data (gaze Tracking)
* DataProcessing: Python scripts used to process gaze Tracking data
* ImageDatabaseGeneration: scripts used for the generation of the experiment dataset

# Experiment \#1 Set Up:
First, make sure you have steamVR installed and that you're HMD is configured properly (tested with Vive Pro and Cosmos).
The experiment requires one controller (either right or left).

* Download the experiment binaries [here](https://pcsbox.univ-littoral.fr/f/ac96fe78a1e1446d94b4/?dl=1)
* Download the image Database [here](https://pcsbox.univ-littoral.fr/d/851527b2b18a4f81aebf/)
* Open the file ```config.txt```  in ```.\P3D\WindowsNoEditor\P3d_Expe1\Content\data``` 
* Change the line ```ImagePath=E:\image\```  to the corresponding path in your system
* Do the same for ```config_tutorial.txt```

# Experiment \#1 usage:

* Launch ```.\P3D\WindowsNoEditor\P3d_Expe1```
* Use keys [<-] and [->] to select a scene. Select the tutorial scene first.
* Press space to start the experiment (or press Controller trackPad)
* Make sure the user has understood the instructions correctly
* When all scenes have been exhausted, press [esc] to quit

Tracking results are saved in: ```.\P3D\WindowsNoEditor\P3d_Expe1\Saved\Logs```

# Setting Up the Unreal Project:

Download the project [here](https://pcsbox.univ-littoral.fr/d/6f101579cefe4e4493dd/?dl=1)

Or alternatively, you can probably import the files manually in a blank UE4 project (not advised though, it may be teddious...)

# DataProcessing scripts:
see ```DataProcessing/readme```

# ImageDatabaseGeneration:
see ```ImageDatabaseGeneration/readme```
