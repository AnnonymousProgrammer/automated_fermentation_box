#!/bin/sh

sudo apt update

# install opencv
sudo apt install build-essential python-dev python-openssl git-core
sudo apt install python3-opencv

# install streamlit for webinterface
sudo apt install cmake
sudo apt install python3-pandas
pip3 install protobuf==3.20.0
pip3 install streamlit==0.62.0

# install DHT22 lib
cd ~
mkdir git
cd git
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python3 setup.py install
