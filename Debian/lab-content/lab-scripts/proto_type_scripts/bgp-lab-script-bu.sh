#! /bin/bash

export STARTUP_STATUS_LOG="/home/seed/Documents/lab-content/team-network/bgp_lab_status.log"

export DOCKER_LOG="/home/seed/Documents/lab-content/team-network/docker-up.log"

cd ~/Documents/lab-content
source development.env
cd team-network
rm -r output_new
rm -f bgp_lab_status.log
rm -f docker-up.log
touch bgp_lab_status.log
touch docker-up.log

python3 ./netBuild.py
sleep 5

cd output_new
cp -a ../../lab-scripts/bgp-atk-lab-sub-scripts/. .

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
#yes | docker network prune

gnome-terminal --tab -- bash -c "\
cd ~/Documents/lab-content/client; \
docker-compose build; \
docker-compose down; \
docker-compose up; \
exec bash" &

./docker-build.sh
#docker-compose down
./docker-up.sh

#gnome-terminal --tab -- bash -c "\
#cd ~/Documents/lab-content/client; \
#docker-compose build; \
#docker-compose down; \
#docker-compose up; \
#exec bash"

gnome-terminal --tab -- bash -c "\
cd ~/Documents/lab-content/team-network; \
while ! grep -q 'bird: Started' \"$DOCKER_LOG\"; do \
	sleep 5; \
done; \
firefox http://127.0.0.1:8080/map.html; \
wmctrl -r "Mozilla Firefox" -e 0,0,0,960,1080; \
exec bash"




