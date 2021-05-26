#render $N independant images of $spp samples each.
#does right and left eye, and save each images to rawls format
#then convert the rawls images to png and merge them (first image will have spp samples, last image will have N*spp samples)

#syntax: bash pbrt_independent_stereo.sh [spp] [N] [filename] [scenepath]

#!/bin/bash
DIR=/home/qhuan/script
source $DIR/pbrt_path.sh
cd $scripts

spp=$1
N=$2
filename="${3%.*}"
scenePath=$4

#make sure pov is right in scene file
sed -i -e 's/"string view" "left"/"string view" "right"/g' $scenePath

#render right eye
#$pbrt --spp $spp --nimages $N --outfile "${filename}.rawls"  --folder "$output" $scenePath
echo "----------------"
echo "right image DONE"

#change pov in scene file
sed -i -e 's/"string view" "right"/"string view" "left"/g' $scenePath

#render left eye
#$pbrt --spp $spp --nimages $N --outfile "${filename}.rawls" --folder "$output" $scenePath
echo "----------------"
echo "left image DONE"

#revert pov in scene file
sed -i -e 's/"string view" "left"/"string view" "right"/g' $scenePath

#convert to png and merge samples
mkdir $output/StereoDataBase_merged_png/$filename-right-png
$rawls2png $output/$filename-right $output/StereoDataBase_merged_png/$filename-right-png 1

mkdir $output/StereoDataBase_merged_png/$filename-left-png
$rawls2png $output/$filename-left $output/StereoDataBase_merged_png/$filename-left-png 1

