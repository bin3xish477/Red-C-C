#!/bin/bash

docker pull ubuntu
docker pull alpine
docker pull debian

# Run all the Linux containers.
docker container run ubuntu
docker container run alpine
docker container run debian
