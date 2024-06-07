#!/bin/bash
#this script resets docker and fixes existing network 
#over lap errors 
cd ~
cd ~/Documents/lab-content
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
yes | docker network prune 
