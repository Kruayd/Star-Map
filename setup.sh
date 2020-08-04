#!/bin/bash

version=$(pip -V | grep -Po '(?<=\(python )[0-9]*\.[0-9]*(?=\))') || (echo 'Check if pip is installed!' ; exit)
main=$(echo $version | grep -Po '[0-9]*(?=\.)')

if (( $(echo "$version == 3.8" |bc -l) )); then
  echo 'Your python version is 3.8 and no standard pygame module is available for this version, do you wish to install the dev version? [Y/n]'
  read choice

  if [ $choice = "y" ]; then
    pip install pygame==2.0.0.dev10
    install -r requirements.txt
  else
    (python3.7 -m pip install pygame && python3.7 -m pip install -r requirements.txt) || (echo 'Check if python3.7 is installed!' ; exit)
  fi
elif (( $(echo "$version < 3.8" |bc -l) && $main > 2 )); then
  pip install pygame
  pip install -r requirements.txt
else
  pip3 install pygame
  pip3 install -r requirements.txt
fi
