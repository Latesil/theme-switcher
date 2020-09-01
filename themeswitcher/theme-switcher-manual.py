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

from Themeswitcher.helper_functions import init_de

current_desktop = init_de()
theme = current_desktop.get_current_theme()
light_theme, dark_theme = current_desktop.get_current_themes()

is_terminal = current_desktop.get_value("terminal")
day_terminal_profile = current_desktop.get_value("active-day-profile-terminal")
night_terminal_profile = current_desktop.get_value("active-night-profile-terminal")

night_wallpapers = current_desktop.get_value("path-to-night-wallpaper")
day_wallpapers = current_desktop.get_value("path-to-day-wallpaper")

# known issue: wallpapers don't change. IDK why, cause there are no errors.
# so, right now it doesn't change wp
if theme == light_theme:
    current_desktop.set_current_theme(dark_theme)
    if bool(night_wallpapers):
        current_desktop.set_wallpapers(night_wallpapers)
    if is_terminal:
        current_desktop.set_terminal_profile(night_terminal_profile)
else:
    current_desktop.set_current_theme(light_theme)
    if bool(day_wallpapers):
        current_desktop.set_wallpapers(day_wallpapers)
    if is_terminal:
        current_desktop.set_terminal_profile(day_terminal_profile)
