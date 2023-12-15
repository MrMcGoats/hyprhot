#!/bin/bash

# Assign the first command-line argument to a variable
filePath=$1

if [ $# -eq 0 ]
  then
    echo "Path to config.json must be provided as argument."
    exit 2
fi


handle() {
  case $1 in
    monitoradded*) echo $1; python change_monitor.py $filePath;;
    monitorremoved*) echo $1; python change_monitor.py $filePath;;
  esac
}

socat -U - UNIX-CONNECT:/tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do handle "$line"; done
