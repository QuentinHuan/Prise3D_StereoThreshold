Prise3D_StereoThreshold experiment repository: constains source of various tools used during my 2021 internship (LISIC, Calais, France)

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

* Download the experiment binaries [here](TODO)
* Download the image Database [here](TODO)
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

Download the project [here](TODO)

Or alternatively, you can import the files manually in a blank UE4 project (not advised though, it's rather teddious...)

# DataProcessing scripts:
see ```DataProcessing/readme```

# ImageDatabaseGeneration:
see ```ImageDatabaseGeneration/readme```
