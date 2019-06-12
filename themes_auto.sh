#!/bin/bash

current_time=$(date +"%H")

#get time from night light
time_evening=$(gsettings get org.gnome.settings-daemon.plugins.color night-light-schedule-from)
time_morning=$(gsettings get org.gnome.settings-daemon.plugins.color night-light-schedule-to)

#convert from float to int 
hours_from=${time_evening%.*}
hours_to=${time_morning%.*}

if [ $current_time -gt $hours_from ] || [ $current_time -lt $hours_to ]; then
    gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita-dark'
    exit 0
else
    gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'
    exit 0
fi
