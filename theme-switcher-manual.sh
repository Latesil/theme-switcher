#!/usr/bin/bash

theme=$(gsettings get org.gnome.desktop.interface gtk-theme)

# List and set your gnome-terminal profiles:
# gsettings get org.gnome.Terminal.ProfilesList list
terminal_dark='88173e30-df6e-4442-b012-4e1119c7385f'
terminal_light='b4bd0ffd-117e-4778-82ef-da4ccdf4cb2c'
light_theme=$(gsettings get com.github.Latesil.theme-switcher light-theme)
dark_theme=$(gsettings get com.github.Latesil.theme-switcher dark-theme)

if [[ $theme == $light_theme ]]; then #if light theme then set to dark
    gsettings set org.gnome.desktop.interface gtk-theme $dark_theme
    gsettings set org.gnome.Terminal.ProfilesList default $terminal_dark
    exit 0
else
    gsettings set org.gnome.desktop.interface gtk-theme $light_theme
    gsettings set org.gnome.Terminal.ProfilesList default $terminal_light
    exit 0
fi
