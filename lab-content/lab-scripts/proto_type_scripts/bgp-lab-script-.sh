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

python3 ./netBuild.py > "$DOCKER_LOG" 2>&1
sleep 5

if grep -q "adding dummy service" "$DOCKER_LOG"; then
	echo "TEAM NETWORK COMPILED" >> "$STARTUP_STATUS_LOG"
	echo "TEAM NETWORK COMPILED"
else
	echo "NETWORK COMPILE FAILED"
fi

cd output_new
sudo service docker restart
#cp -a ../../lab-scripts/bgp-atk-lab-sub-scripts/. .

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
sudo service docker restart
#gnome-terminal --tab -- bash -c "\
#cd ~/Documents/lab-content/client; \
#docker-compose build; \
#docker-compose down; \
#docker-compose up; \
#exec bash" &

if grep -q "TEAM NETWORK COMPILED" "$STARTUP_STATUS_LOG"; then
	docker-compose build > "$DOCKER_LOG" 2>&1
fi

while ! grep -q "Successfully tagged output_new_rs_ix_ix104:latest" "$DOCKER_LOG"; do
	sleep 5;
done

echo "DOCKER BUILD SUCCESS" >> "$STARTUP_STATUS_LOG"
echo "DOCKER BUILD SUCCESS"

gnome-terminal --tab -- bash -c "\
cd ~/Documents/lab-content/client; \
docker-compose build; \
docker-compose up > \"$DOCKER_LOG\" 2>&1; \
exec bash" 

gnome-terminal --tab -- bash -c "\
cd ~/Documents/lab-content/team-network; \
while ! grep -q 'bird: Started' \"$DOCKER_LOG\" || ! grep -q 'Attaching to seedemu_client' \"$DOCKER_LOG\"; do \
        sleep 5; \
done; \
firefox http://127.0.0.1:8080/map.html; \
wmctrl -r "Mozilla Firefox" -e 0,0,0,960,1080; \
exec bash" 

if grep -q "DOCKER BUILD SUCCESS" "$STARTUP_STATUS_LOG"; then
        docker-compose up > "$DOCKER_LOG" 2>&1
fi

#./docker-build.sh
#docker-compose down
#./docker-up.sh

#gnome-terminal --tab -- bash -c "\
#cd ~/Documents/lab-content/client; \
#docker-compose build; \
#docker-compose down; \
#docker-compose up; \
#exec bash"





