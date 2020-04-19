import itertools
import os
import gi
from gi.repository import Gtk, Gio, GLib

from .theme_switcher_constants import theme_switcher_constants as constants
from .desktop import Desktop

class Gnome(Desktop):

    def __init__(self):
        self.init_settings()
        
    def init_settings(self):
        self.settings = Gio.Settings.new(constants["BASE_KEY"])
        
    def get_value(self, key):
        return self.settings.get_value(key).unpack()
        
    def set_value(self, key, value):
        if isinstance(value, float):
            self.settings.set_int(key, value)
            
        if isinstance(value, bool):
            self.settings.set_boolean(key, value)
            
        if isinstance(value, int):
            self.settings.set_int(key, value)
            
        if isinstance(value, str):
            self.settings.set_string(key, value)
            
    def reset_value(self, key):
        self.settings.reset(key)
            
    def set_wallpapers(self, wallpaper):
        wallpaper_settings = Gio.Settings.new(constants["WALLPAPER_KEY"])
        wallpaper_settings.set_string("picture-uri", wallpaper)
        
    def start_systemd_timers(self):
        GLib.spawn_async(['/usr/bin/systemctl','--user','start','theme-switcher-auto.timer'])
        GLib.spawn_async(['/usr/bin/systemctl','--user','enable','theme-switcher-auto.timer'])
        
    def stop_systemd_timers(self):
        GLib.spawn_async(['/usr/bin/systemctl','--user','stop','theme-switcher-auto.timer'])
        GLib.spawn_async(['/usr/bin/systemctl','--user','disable', 'theme-switcher-auto.timer'])
        
    def get_current_themes(self):
        current_light_theme = self.settings.get_string('light-theme')
        current_dark_theme = self.settings.get_string('dark-theme')
        return current_light_theme, current_dark_theme
        
    def set_current_theme(self, theme):
        theme_settings = Gio.Settings.new(constants["THEME_KEY"])
        theme_settings.set_string("gtk-theme", theme)
        
    def get_current_theme(self):
        theme_settings = Gio.Settings.new(constants["THEME_KEY"])
        current_theme = theme_settings.get_string("gtk-theme")
        return current_theme
        
    def get_all_values(self):
        values = {}
        for k in self.settings.list_keys():
            values[k] = self.settings.get_value(k).unpack()
        return values
        
    def get_terminal_profiles(self):
        terminal_settings = Gio.Settings.new('org.gnome.Terminal.ProfilesList')
        return terminal_settings.get_value('list').unpack()
        
    def set_terminal_profile(self, profile):
        terminal_settings = Gio.Settings.new('org.gnome.Terminal.ProfilesList')
        terminal_settings.set_string("default", profile)
        
    #taken from GNOME Tweaks
    #by John Stowers.

    def get_resource_dirs(self, resource):
        dirs = [os.path.join(dir, resource)
                for dir in itertools.chain(GLib.get_system_data_dirs())]
        dirs += [os.path.join(os.path.expanduser("~"), ".{}".format(resource))]

        return [dir for dir in dirs if os.path.isdir(dir)]

    def _get_valid_themes(self):
        gtk_ver = Gtk.MINOR_VERSION
        if gtk_ver % 2: # Want even number
            gtk_ver += 1

        valid = ['Adwaita', 'HighContrast', 'HighContrastInverse']
        valid += self.walk_directories(self.get_resource_dirs("themes"), lambda d:
                    os.path.exists(os.path.join(d, "gtk-3.0", "gtk.css")) or \
                         os.path.exists(os.path.join(d, "gtk-3.{}".format(gtk_ver))))
        return set(valid)
        
    def walk_directories(self, dirs, filter_func):
        valid = []
        try:
            for thdir in dirs:
                if os.path.isdir(thdir):
                    for t in os.listdir(thdir):
                        if filter_func(os.path.join(thdir, t)):
                            valid.append(t)
        except:
            pass

        return valid

        
