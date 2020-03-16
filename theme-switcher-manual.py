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

settings = Gio.Settings.new("com.github.Latesil.theme-switcher")
terminal_settings = Gio.Settings.new("org.gnome.Terminal.ProfilesList")
desktop_settings = Gio.Settings.new("org.gnome.desktop.interface")
theme = desktop_settings.get_string("gtk-theme")

terminal_dark = '88173e30-df6e-4442-b012-4e1119c7385f'
terminal_light = 'b4bd0ffd-117e-4778-82ef-da4ccdf4cb2c'

light_theme = settings.get_string("light-theme")
dark_theme = settings.get_string("dark-theme")

if theme == light_theme:
    desktop_settings.set_string("gtk-theme", dark_theme)
    terminal_settings.set_string("default", terminal_dark)
else:
    desktop_settings.set_string("gtk-theme", light_theme)
    terminal_settings.set_string("default", terminal_light)
