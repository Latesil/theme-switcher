#!/bin/bash

time=$(date +"%H:%M")

if [[ $time > '19:00' ]] || [[ $time < '06:00' ]]; then
    gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita-dark'
    exit 0
else
    gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'
    exit 0
fi
