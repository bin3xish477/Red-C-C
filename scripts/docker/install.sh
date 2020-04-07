#!/bin/bash

# Get Docker quick install script.
curl -fsSL https://get.docker.com/ -o install-docker.sh

# Install docker from script.
bash install-docker.sh

# Pull the latest images from Docker hub.
docker pull ubuntu
docker pull alpine
docker pull debian

# Run all the Linux containers.
docker container run ubuntu
docker container run alpine
docker container run debian
