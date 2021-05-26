#single scene render
#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source $DIR/pbrt_aliases_path.sh
cd $scripts

spp=$1
filename="${2%.*}"
scenePath=$3

$pbrt --spp $spp --outfile "${filename}.png" --folder "$output" $scenePath

echo "--------------------------"
echo "saved image in $output"
