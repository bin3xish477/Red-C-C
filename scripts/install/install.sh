#!/bin/bash

VERSION=$(lsb_release -a)
UBUNTU='Ubuntu'
KALI='Kali'

cd /tmp/

if [[ "$VERSION" == *"$UBUNTU"* ]];
then
    sudo apt-get install python3.6
    sudo apt-get install wget
fi

if [[ "$VERSION" == *"$KALI"* ]];
then
    sudo apt install python3.6
    sudo apt install wget
fi
