#!/bin/sh
handle() {
  case $1 in
    monitoradded*) echo $1; python change_monitor.py $CONFIG_MONITOR_SWITCHER_HYPRLAND;;
    monitorremoved*) echo $1; python change_monitor.py $CONFIG_MONITOR_SWITCHER_HYPRLAND;;
  esac
}

socat -U - UNIX-CONNECT:/tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do handle "$line"; done
