useful scripts for database generation:

# Environnement Setup:

* Install [P3d_PBRT_V4](https://github.com/prise-3d/pbrt-v4/tree/master)
* Install [Rawls Tools](https://github.com/prise-3d/rawls-tools)
* clone ```script``` folder on your computer, and fill in ```PBRT_Path.sh```

# Usage:
## RenderCmd folder:
Use these script to launch a batch of PBRT render
* ```pbrt_single.sh [spp] [out file name] [absolute scenePath]``` ==> render a single image
* ```pbrt_independant_stereo [spp] [N] [out file name] [absolute scenePath]``` ==> render a batch of N independant stereo (left and right) images: each image is [spp] samples. Images are saved in ```/output``` folder defined in ```PBRT_Path.sh```
When .rawls are converted to .png, the images are merged and will have increasing amount of sample (image_k.png have k*[spp] samples)
* ```generateStereoDatabase.sh [spp] [N]``` edit the script sceneList and run. Execute the command ```pbrt_independant_stereo``` for each scene in sceneList.
.rawls and .png are both saved to disk. .png are in ```/$output/StereoDataBase_merged_png```

## mergeIntoStereoCmd folder:
* lr_to_stereo.sh [filename] [N] ==> this script merge left and right images made by <pbrt_independant_stereo.sh> into a single stereo image. Uses .png images.


