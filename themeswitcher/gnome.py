import gi
from gi.repository import Gio, GLib

from .theme_switcher_constants import theme_switcher_constants as constants
from .desktop import Desktop
import subprocess

class Gnome(Desktop):
        
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
        
