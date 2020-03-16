#!/usr/bin/python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio

#find better solution
def convert_to_values(i, j):
    first_value = i * 60
    return first_value + j
    
settings = Gio.Settings.new("com.github.Latesil.theme-switcher")
desktop_settings = Gio.Settings.new("org.gnome.desktop.interface")
background_settings = Gio.Settings.new("org.gnome.desktop.background")
terminal_settings = Gio.Settings.new("org.gnome.Terminal.ProfilesList")

current_time = datetime.datetime.now()

#find better solution
current_values = convert_to_values(current_time.hour, int(str(current_time.minute)[:-1]+'0'))

terminal_dark = '88173e30-df6e-4442-b012-4e1119c7385f'
terminal_light = 'b4bd0ffd-117e-4778-82ef-da4ccdf4cb2c'

night_values = settings.get_int("nighttime-values")
day_values = settings.get_int("daytime-values")

night_wallpapers = settings.get_string("path-to-night-wallpaper")
day_wallpapers = settings.get_string("path-to-day-wallpaper")

light_theme = settings.get_string("light-theme")
dark_theme = settings.get_string("dark-theme")

if ((current_values <= day_values or current_values >= night_values)):
    desktop_settings.set_string("gtk-theme", dark_theme)
    if night_wallpapers is not None:
        background_settings.set_string("picture-uri", night_wallpapers)
    terminal_settings.set_string("default", terminal_dark)
else:
    desktop_settings.set_string("gtk-theme", light_theme)
    if day_wallpapers is not None:
        background_settings.set_string("picture-uri", day_wallpapers)
    terminal_settings.set_string("default", terminal_light)
