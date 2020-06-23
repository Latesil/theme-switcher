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
from astral import LocationInfo
from astral.sun import sun
import pytz
import sys
import random
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio
from Themeswitcher.helper_functions import init_de, Helper

helper = Helper()
current_desktop = init_de()
current_time = datetime.datetime.now()
current_values = helper.convert_to_values(current_time.hour, current_time.minute)
    
def get_values():
    day_hour_values = current_desktop.get_value("daytime-hour")
    day_minutes_values = current_desktop.get_value("daytime-minutes")
    night_hour_values = current_desktop.get_value("nighttime-hour")
    night_minutes_values = current_desktop.get_value("nighttime-minutes")
    return day_hour_values, day_minutes_values, night_hour_values, night_minutes_values

def change_wallpaper():
    day_wp = current_desktop.get_value('day-wallpapers-from-folder')
    night_wp = current_desktop.get_value('night-wallpapers-from-folder')
    values = get_values()
    day_values = helper.convert_to_values(values[0], values[1])
    night_values = helper.convert_to_values(values[2], values[3])
    night_wallpapers = random.choice(night_wp)
    day_wallpapers = random.choice(day_wp)
    current_wp = current_desktop.get_wallpapers()
    
    if night_wallpapers == current_desktop.get_wallpapers() or day_wallpapers == current_desktop.get_wallpapers():
        while night_wallpapers == current_wp:
            night_wallpapers = random.choice(night_wp)
        while day_wallpapers == current_wp:
            day_wallpapers = random.choice(day_wp)
            
    current_desktop.set_value("path-to-day-wallpaper", day_wallpapers)
    current_desktop.set_value("path-to-night-wallpaper", night_wallpapers)
            
    if ((current_values <= day_values or current_values >= night_values)):
        current_desktop.set_wallpapers(night_wallpapers)
    else:
        current_desktop.set_wallpapers(day_wallpapers)
    
def trigger_script():
    night_wallpapers = current_desktop.get_value("path-to-night-wallpaper")
    day_wallpapers = current_desktop.get_value("path-to-day-wallpaper")
    is_terminal = current_desktop.get_value("terminal")
    day_terminal_profile = current_desktop.get_value("active-day-profile-terminal")
    night_terminal_profile = current_desktop.get_value("active-night-profile-terminal")
    theme = current_desktop.get_current_theme()
    light_theme, dark_theme = current_desktop.get_current_themes()
    is_night_light = current_desktop.get_value("night-light")
    
    if is_night_light:
        if current_desktop.check_night_light():
            if current_desktop.is_night_light_auto():
                current_timezone = current_desktop.get_timezone()
                coords = current_desktop.get_coordinates()
                location = LocationInfo('name', 'region', current_timezone, coords[0], coords[1])
                s = sun(location.observer, date=current_time.date(), tzinfo=pytz.timezone(location.timezone))
                day = s["sunrise"].strftime("%H:%M").split(':')
                night = s["sunset"].strftime("%H:%M").split(':')
                day_values = helper.convert_to_values(int(day[0]), int(day[1]))
                night_values = helper.convert_to_values(int(night[0]), int(night[1]))
            else:
                times = current_desktop.get_night_light_manual()
                day_values = helper.convert_to_values(times[0], times[1])
                night_values = helper.convert_to_values(times[2], times[3])
    else:
        values = get_values()
        day_values = helper.convert_to_values(values[0], values[1])
        night_values = helper.convert_to_values(values[2], values[3])
        
    if ((current_values <= day_values or current_values >= night_values)):
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

freq = current_desktop.get_value("advanced-wallpapers-day-trigger-mode")
afm = current_desktop.get_value('advanced-wallpapers-management')
if afm:
    if freq == 'sync':
        trigger_script()
        sys.exit(0)
    elif freq == '10 min':
        change_wallpaper()
        trigger_script()
        sys.exit(0)
    elif freq == '30 min':
        if (current_time.minute - current_time.minute % 10) % 30 == 0:
            change_wallpaper()
            trigger_script()
            sys.exit(0)
    elif freq == '1 hour':
        if (current_time.minute == 00):
            change_wallpaper()
            trigger_script()
            sys.exit(0)
    elif freq == '2 hour':
        if (current_time.hour % 2 == 0):
            change_wallpaper()
            trigger_script()
            sys.exit(0)
    elif freq == '3 hour':
        if (current_time.hour % 3 == 0):
            change_wallpaper()
            trigger_script()
            sys.exit(0)
    elif freq == '6 hour':
        if (current_time.hour % 6 == 0):
            change_wallpaper()
            trigger_script()
            sys.exit(0)
    elif freq == '12 hour':
        if (current_time.hour % 12 == 0):
            change_wallpaper()
            trigger_script()
            sys.exit(0)
else:
    trigger_script()
    sys.exit(0)

