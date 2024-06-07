#!/bin/bash

#creating variable for path to custom docker log file
export DOCKER_LOG="/home/seed/Documents/lab-content/team-network/docker-up.log"

#navigate to project network folder, ensure dependencies,
#then clean up existing logs and docker output
cd ~/Documents/lab-content
source development.env
cd team-network
rm -r output_new
rm -f docker-up.log
touch docker-up.log

#compile python script to start process of building network
python3 ./netBuild.py

#in a new terminal move to python script output folder
#make sure potentially existing docker network is removed and reset
#then build and start up desired network redirecting output to log
sleep 3
gnome-terminal --tab -- bash -c "\
cd output_new; \
docker stop $(docker ps -aq); \
sleep 15; \ 
docker rm $(docker ps -aq); \
sleep 10; \
yes | docker network prune; \
sleep 5; \
docker-compose build; \
docker-compose up > \"$DOCKER_LOG\" 2>&1; \
exec bash" &

#navigate to client folder in a new terminal
#then build and start up front end internet visualizer 
gnome-terminal --tab -- bash -c "\
cd ~/Documents/lab-content/client; \
docker-compose build; \
docker-compose down; \
docker-compose up; \
exec bash"

#navigate to log file and start looping until network is ready
#once network is ready open visualizer using firefox
gnome-terminal --tab -- bash -c "\
cd ~/Documents/lab-content/team-network; \
while ! grep -q 'bird: Started' \"$DOCKER_LOG\"; do \
	sleep 5; \
done; \
firefox http://127.0.0.1:8080/map.html; \
wmctrl -r "Mozilla Firefox" -e 0,0,0,960,1080; \
exec bash"

#minimize all terminals then open lab guide
gnome-terminal --tab -- bash -c 'for window in $(xdotool search --onlyvisible --class ".*"); do xdotool windowminimize "$window"; done; okular ~/Documents/lab-content/lab-guides/bgp-attack-lab-guide.pdf' &

