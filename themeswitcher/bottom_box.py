import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from .theme_switcher_constants import theme_switcher_constants as constants
import os
import datetime
from .helper_functions import set_theme, convert_to_values
from .gnome import Gnome

desktop = Gnome()

@Gtk.Template(resource_path = constants["UI_PATH"] + 'ui/bottom_box.ui')
class BottomBox(Gtk.Box):

    __gtype_name__ = "BottomBox"

    _bottom_label = Gtk.Template.Child()
    _day_hour_spin_button = Gtk.Template.Child()
    _day_minutes_spin_button = Gtk.Template.Child()
    _night_hour_spin_button = Gtk.Template.Child()
    _night_minutes_spin_button = Gtk.Template.Child()
    _bottom_box_day_label = Gtk.Template.Child()
    _bottom_box_night_label = Gtk.Template.Child()
    _main_bottom_grid = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        #init settings
        desktop.init_settings()
        desktop.get_current_themes()
        self.set_margin_top(20)
        self.cur_light_theme, self.cur_dark_theme = desktop.get_current_themes()

        #unused yet, but who knows
        # self._day_scale.set_name("day scale")
        # self._night_scale.set_name("night scale")

        #monitor changes in gsettings
        if isinstance(desktop, Gnome):
            desktop.start_monitor_settings()

        #get values from gsettings after start programm
        desktop.get_scales_values()
        get_values()
        self.on_combo_box_changed()

        self._bottom_box_day_label.set_halign(Gtk.Align.START)
        self._bottom_box_night_label.set_halign(Gtk.Align.START)


    #set active state for scales
    """def on_time_visible_change(self, settings, key, button):
        if settings.get_boolean("time-visible"):
            self._main_bottom_grid.set_visible(True)
        else:
            self._main_bottom_grid.set_visible(False)"""

    """def get_scales_values(self):
        self.on__day_hour_spin_button_value_changed(self.settings, "daytime-hour", self._day_hour_spin_button)
        self.on__day_minutes_spin_button_value_changed(self.settings, "daytime-minutes", self._day_minutes_spin_button)
        self.on__night_hour_spin_button_value_changed(self.settings, "nighttime-hour", self._night_hour_spin_button)
        self.on__night_minutes_spin_button_value_changed(self.settings, "nighttime-minutes", self._night_minutes_spin_button)
        self.on_time_visible_change(self.settings, None, None)"""
        
    def get_values(self):
        day_hour_values = self.settings.get_int("daytime-hour")
        day_minutes_values = self.settings.get_int("daytime-minutes")
        night_hour_values = self.settings.get_int("nighttime-hour")
        night_minutes_values = self.settings.get_int("nighttime-minutes")
        return day_hour_values, day_minutes_values, night_hour_values, night_minutes_values

    def on_combo_box_changed(self):
        current_time = datetime.datetime.now()
        values = self.get_values()
        
        #find better solution
        current_values = convert_to_values(current_time.hour, int(str(current_time.minute)[:-1]+'0'))
        
        day_values = convert_to_values(values[0], values[1])
        night_values = convert_to_values(values[2], values[3])
        
        if ((current_values <= day_values or current_values >= night_values)):
            set_theme(self.theme_settings, self.cur_dark_theme)
        else:
            set_theme(self.theme_settings, self.cur_light_theme)
            
    #____functions for local changes from dconf____#
    
    """def on__spin_button_value_changed(self, settings, key, button):
        button.set_value(settings.get_int(key))"""
    
    """def on__day_minutes_spin_button_value_changed(self, settings, key, button):
        self._day_minutes_spin_button.set_value(self.settings.get_int("daytime-minutes"))
    
    def on__night_minutes_spin_button_value_changed(self, settings, key, button):
        self._night_minutes_spin_button.set_value(self.settings.get_int("nighttime-minutes"))
    
    def on__night_hour_spin_button_value_changed(self, settings, key, button):
        self._night_hour_spin_button.set_value(self.settings.get_int("nighttime-hour"))"""
        
    #___adjustment callbacks____#
        
    @Gtk.Template.Callback()
    def on__day_hour_adjustment_value_changed(self, scale):
        self.settings.set_int("daytime-hour", scale.get_value())
        self.on_combo_box_changed()
        
    @Gtk.Template.Callback()
    def on__day_minutes_adjustment_value_changed(self, scale):
        self.settings.set_int("daytime-minutes", scale.get_value())
        self.on_combo_box_changed()
        
    @Gtk.Template.Callback()
    def on__night_minutes_adjustment_value_changed(self, scale):
        self.settings.set_int("nighttime-minutes", scale.get_value())
        self.on_combo_box_changed()
    
    @Gtk.Template.Callback()
    def on__night_hour_adjustment_value_changed(self, scale):
        self.settings.set_int("nighttime-hour", scale.get_value())
        self.on_combo_box_changed()
        
