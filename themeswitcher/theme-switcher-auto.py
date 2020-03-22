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
from themeswitcher.helper_functions import init_de, convert_to_values

desktop = init_de()
    
def get_values():
    day_hour_values = desktop.get_value("daytime-hour")
    day_minutes_values = desktop.get_value("daytime-minutes")
    night_hour_values = desktop.get_value("nighttime-hour")
    night_minutes_values = desktop.get_value("nighttime-minutes")
    return day_hour_values, day_minutes_values, night_hour_values, night_minutes_values
    
desktop = init_de()
theme = desktop.get_current_theme()
light_theme, dark_theme = desktop.get_current_themes()

current_time = datetime.datetime.now()

values = get_values()

#find better solution
current_values = convert_to_values(current_time.hour, int(str(current_time.minute)[:-1]+'0'))

day_values = convert_to_values(values[0], values[1])
night_values = convert_to_values(values[2], values[3])

night_wallpapers = desktop.get_value("path-to-night-wallpaper")
day_wallpapers = desktop.get_value("path-to-day-wallpaper")

if ((current_values <= day_values or current_values >= night_values)):
    desktop.set_current_theme(dark_theme)
    if night_wallpapers is not None:
        desktop.set_wallpapers(night_wallpapers)
else:
    desktop.set_current_theme(light_theme)
    if day_wallpapers is not None:
        desktop.set_wallpapers(day_wallpapers)
    
