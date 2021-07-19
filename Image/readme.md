Image database [HERE](https://pcsbox.univ-littoral.fr/d/14c0dfa2e07148d98b84/)

# description:
Images generated for threshold mesurement. The images are organized by *scene name* and by *point of view* (ex: ``p3d_arcsphere-right`` contains all the images of the scene "arcsphere" for the right point of view). Image quality is progressive (1 images correspond to an increase 20 spp), maximum spp is 10.000 spp (image #500). 

* 8pov folder contains images for an autostereoscopic screen (alioscopy screen). See [this repo](https://github.com/QuentinHuan/Prise3d_StereoThreshold_Alioscopy)
Format: png
Dimensions: 360*360
* stereo folder contains images for a VR headset (HTC Vive). See [Prise3D_StereoThreshold/P3d_Expe1](https://github.com/QuentinHuan/Prise3D_StereoThreshold/tree/main/P3d_Expe1)
Format: png
Dimensions: 800*800
* ODS folder countains images for a VR headset visualizing 360deg stereo images (Omni Directionnal Stereo, see https://developers.google.com/vr/jump/rendering-ods-content.pdf).

# Generation:
Images were generated using the custom P3D_pbrt-v4 pathtracing engine ([see](https://github.com/prise-3d/pbrt-v4)).
OSD content can be rendered with a specific camera model implemented in the dev branch.

You can use the python scripts in this repo to generate a set of images for a selected list of scenes.
