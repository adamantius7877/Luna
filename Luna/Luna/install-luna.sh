#!/usr/bin/env bash

# Install Prereqs
sudo apt-get install libgfortran3 libasound2 libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
pip3 install redis
pip3 install vosk
pip3 install nltk
pip3 install pyglet
pip3 install ratcave
pip3 install pyaudio
pip3 install pyttsx3

# Download and unpack Luna and all associated files
curl http://87.87.10.38/downloads/luna.tar.gz > luna.tar.gz
tar -xvf luna.tar.gz
mv var/jenkins_home/workspace/* ./
rm -r var

curl http://87.87.10.38/downloads/model_small.zip > model_small.zip
unzip model_small.zip
mv model_small/ luna/Luna/Luna/
rm model_small.zip

cd luna/Luna/Luna
mv Luna.py luna.py
python3 lunamain.py
