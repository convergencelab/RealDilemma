#!bin/bash

# on a fresh pi:
pip3 install virtualenv
cd ./envs/tf1_stable_baselines
virtualenv tf1_stable_baselines
cd tf1_stable_baselines/bin
source ./activate
cd ../../
pip install -r requirements.txt
pip3 install -U numpy

# https://github.com/sophiagu/stable-baselines-tf2
# find the installation of stable_baselines
cd ~
path=$(find . -type d -name "stable_baselines")
echo $path
rm -r $path
# install tf2 version
git clone https://github.com/sophiagu/stable-baselines-tf2
# copy the installation and remove from download location
mkdir $path
cp -r stable-baselines-tf2/* $path
sudo rm -r stable-baselines-tf2

# lastly install tf2
pip3 install https://github.com/bitsy-ai/tensorflow-arm-bin/releases/download/v2.4.0-rc2/tensorflow-2.4.0rc2-cp37-none-linux_armv7l.whl
