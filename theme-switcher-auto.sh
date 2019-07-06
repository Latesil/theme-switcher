#!/usr/bin/bash

time=$(date +"%H")

# List and set your gnome-terminal profiles:
# gsettings get org.gnome.Terminal.ProfilesList list
terminal_dark='88173e30-df6e-4442-b012-4e1119c7385f'
terminal_light='b4bd0ffd-117e-4778-82ef-da4ccdf4cb2c'
night=$(gsettings get org.theme-switcher nighttime)
daytime=$(gsettings get org.theme-switcher daytime)
night_wallpapers=$(gsettings get org.theme-switcher path-to-night-wallpaper)
day_wallpapers=$(gsettings get org.theme-switcher path-to-day-wallpaper)

if (( $time >= $night )) || (( $time <= $daytime )); then
    gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita-dark'
    if [ "$night_wallpapers" != "''" ]; then
        gsettings set org.gnome.desktop.background picture-uri "$night_wallpapers"
    fi
    gsettings set org.gnome.Terminal.ProfilesList default $terminal_dark
    exit 0
else
    gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'
    if [ "$day_wallpapers" != "''" ]; then
        gsettings set org.gnome.desktop.background picture-uri "$day_wallpapers"
    fi
    gsettings set org.gnome.Terminal.ProfilesList default $terminal_light
    exit 0
fi
