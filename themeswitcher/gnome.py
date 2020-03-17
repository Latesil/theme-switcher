import gi
from gi.repository import Gio, GLib

from .theme_switcher_constants import theme_switcher_constants as constants
from .desktop import Desktop

class Gnome(Desktop):
        
    def init_settings(self):
        self.settings = Gio.Settings.new(constants["BASE_KEY"])
        #self.theme_settings = Gio.Settings.new(constants["THEME_KEY"])
        
    def get_init_settings(self):
        print('get_init settings')
        
    def get_value(self, key):
        return self.settings.get_value(key).unpack()
        
    def set_value(self, key, value):
        return self.settings.set_value(key, GLib.Variant.new_variant(value))
        
    def connect_wallpapers(self):
        print('connect wallpapers')
        
    def connect_daytime(self):
        print('connect_daytime')
        
    def connect_nighttime(self):
        print('connect_nighttime')
        
    def connect_time_visible(self):
        print('connect_time_visible')
        
    def connect_autoswitch(self):
        print('connect_autoswitch')
        
    def set_wallpapers(self, wallpapers):
        wallpaper_settings = Gio.Settings.new(constants["WALLPAPER_KEY"])
        wallpaper_settings.set_string("picture-uri", wallpaper)
        
    def start_systemd_timers(self):
        print('start_systemd_timers')
        
    def stop_systemd_timers(self):
        print('stop_systemd_timers')
        
    def get_current_themes(self):
        self.current_light_theme = self.settings.get_string('light-theme')
        self.current_dark_theme = self.settings.get_string('dark-theme')
        
    def set_current_theme(self):
        print('set current theme')
        
    def get_scales_values(self):
        self.on__day_hour_spin_button_value_changed(self.settings, "daytime-hour", self._day_hour_spin_button)
        self.on__day_minutes_spin_button_value_changed(self.settings, "daytime-minutes", self._day_minutes_spin_button)
        self.on__night_hour_spin_button_value_changed(self.settings, "nighttime-hour", self._night_hour_spin_button)
        self.on__night_minutes_spin_button_value_changed(self.settings, "nighttime-minutes", self._night_minutes_spin_button)
        self.on_time_visible_change(self.settings, None, None)
        
    def start_monitor_settings(self):
        self.settings.connect("changed::daytime-hour", self.on__spin_button_value_changed, self._day_hour_spin_button)
        self.settings.connect("changed::daytime-minutes", self.on__spin_button_value_changed, self._day_minutes_spin_button)
        self.settings.connect("changed::nighttime-hour", self.on__spin_button_value_changed, self._night_hour_spin_button)
        self.settings.connect("changed::nighttime-minutes", self.on__spin_button_value_changed, self._night_hour_spin_button)
        self.settings.connect("changed::time-visible", self.on_time_visible_change, None)
        
    def on__spin_button_value_changed(self, settings, key, button):
        button.set_value(settings.get_int(key))
        
    def on_time_visible_change(self, settings, key, button):
        if settings.get_boolean("time-visible"):
            self._main_bottom_grid.set_visible(True)
        else:
            self._main_bottom_grid.set_visible(False)
            
            
    def get_values(self):
        self.day_hour_values = self.settings.get_int("daytime-hour")
        self.day_minutes_values = self.settings.get_int("daytime-minutes")
        self.night_hour_values = self.settings.get_int("nighttime-hour")
        self.night_minutes_values = self.settings.get_int("nighttime-minutes")
