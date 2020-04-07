#!/bin/bash

VERSION=$(lsb_release -a)
UBUNTU='Ubuntu'
KALI='Kali'

if [[ "$VERSION" == *"$UBUNTU"* ]];
then
    sudo apt-get install python3.6
fi

if [[ "$VERSION" == *"$KALI"* ]];
then
    sudo apt install python3.6
fi
