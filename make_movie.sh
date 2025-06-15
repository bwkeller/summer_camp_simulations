#!/usr/bin/env bash
SNAPDIR=$1
MOVIENAME=$2

if [ $# -ne 2 ]; then
	echo "usage: make_movie.sh simulation_directory movie_name"
	exit 1
fi

rm -rf images
mkdir images
./make_frames.py $SNAPDIR

ffmpeg -i images/im%05d.png -c:v libx264 -pix_fmt yuv420p -r 25 $MOVIENAME.mp4
rm -rf images
