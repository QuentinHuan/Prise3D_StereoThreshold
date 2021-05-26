#generate the Stereo images database
#right.rawls and left.rawls images are saved in $output/
#right.png and left.png images are saved in $output/StereoDataBase_merged_png
#
#edit the file to add or remove scenes


#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source /home/qhuan/script/pbrt_path.sh
cd $scripts/renderCmd

spp=$1
N=$2

#render stereo and create left.png and right.png
bash pbrt_independant_stereo.sh $spp $N p3d_arcsphere.rawls /home/qhuan/p3d_pbrt-v4-scenes-stereo/arcsphere/p3d_arcsphere.pbrt

bash pbrt_independant_stereo.sh $spp $N p3d_bunny-fur.rawls /home/qhuan/p3d_pbrt-v4-scenes-stereo/bunny-fur/p3d_bunny-fur-view0.pbrt

bash pbrt_independant_stereo.sh $spp $N p3d_caustic-view0.rawls /home/qhuan/p3d_pbrt-v4-scenes-stereo/caustic-view0/p3d_caustic-view0.pbrt

bash pbrt_independant_stereo.sh $spp $N p3d_contemporary-bathroom.rawls /home/qhuan/p3d_pbrt-v4-scenes-stereo/contemporary-bathroom/p3d_contemporary-bathroom.pbrt

bash pbrt_independant_stereo.sh $spp $N p3d_crown.rawls /home/qhuan/p3d_pbrt-v4-scenes-stereo/crown/p3d_crown.pbrt

bash pbrt_independant_stereo.sh $spp $N p3d_kitchen-view0.rawls /home/qhuan/p3d_pbrt-v4-scenes-stereo/kitchen/p3d_kitchen-view0.pbrt

bash pbrt_independant_stereo.sh $spp $N p3d_kitchen-view1.rawls /home/qhuan/p3d_pbrt-v4-scenes-stereo/kitchen/p3d_kitchen-view1.pbrt

bash pbrt_independant_stereo.sh $spp $N p3d_kitchen-view0.rawls /home/qhuan/p3d_pbrt-v4-scenes-stereo/pavilion-day-view0/p3d_pavilion-day-view0.pbrt

