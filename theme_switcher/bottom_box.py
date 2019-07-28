import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from .theme_switcher_constants import theme_switcher_constants as constants
import os
import datetime
from .helper_functions import set_theme

resource = Gio.Resource.load("/home/lateseal/Documents/prog/python/pygtk/theme-switcher/data/theme-switcher.gresource")
resource._register()

@Gtk.Template(resource_path = constants["UI_PATH"] + 'ui/bottom_box.ui')
class BottomBox(Gtk.Box):

    __gtype_name__ = "BottomBox"

    _bottom_label = Gtk.Template.Child()
    _day_scale = Gtk.Template.Child()
    _night_scale = Gtk.Template.Child()
    _bottom_day_label = Gtk.Template.Child()
    _bottom_night_label = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        #init settings
        self.settings = Gio.Settings.new(constants["BASE_KEY"])
        self.theme_settings = Gio.Settings.new(constants["THEME_KEY"])
        self.set_margin_top(20)

        self.current_light_theme = self.settings.get_string('light-theme')
        self.current_dark_theme = self.settings.get_string('dark-theme')

        self._day_scale.set_name("day scale")
        self._night_scale.set_name("day scale")

        #monitor changes in gsettings
        self.settings.connect("changed::daytime", self.on__day_scale_change, self._day_scale)
        self.settings.connect("changed::nighttime", self.on__night_scale_change, self._night_scale)
        self.settings.connect("changed::time-visible", self.on_time_visible_change, None)

        #get values from gsettings after start programm
        self.get_scales_values()

        self._bottom_day_label.set_halign(Gtk.Align.START)
        self._bottom_night_label.set_halign(Gtk.Align.START)


    #set active state for scales
    def on_time_visible_change(self, settings, key, button):
        if self.settings.get_boolean("time-visible"):
            self._night_scale.set_state(Gtk.StateType.ACTIVE)
            self._day_scale.set_state(Gtk.StateType.ACTIVE)
        else:
            self._night_scale.set_state(Gtk.StateType.INSENSITIVE)
            self._day_scale.set_state(Gtk.StateType.INSENSITIVE)

    def on__day_scale_change(self, settings, key, button):
        self._day_scale.set_value(self.settings.get_int("daytime"))

    def on__night_scale_change(self, settings, key, button):
        self._night_scale.set_value(self.settings.get_int("nighttime"))

    def get_scales_values(self):
        self.on__day_scale_change(self.settings, "daytime", self._day_scale)
        self.on__night_scale_change(self.settings, "nighttime", self._night_scale)

    #set two callbacks for scale
    @Gtk.Template.Callback()
    def on__day_adjustment_value_changed(self, scale):
        self.settings.set_int("daytime", scale.get_value())
        self.on_combo_box_changed()

    @Gtk.Template.Callback()
    def on__night_adjustment_value_changed(self, scale):
        self.settings.set_int("nighttime", scale.get_value())
        self.on_combo_box_changed()

    def on_combo_box_changed(self):
        current_time = datetime.datetime.now()
        time_for_day = self.settings.get_int("daytime")
        time_for_night = self.settings.get_int("nighttime")
        if ((current_time.hour <= time_for_day or current_time.hour >= time_for_night)):
            set_theme(self.theme_settings, self.current_dark_theme)
        else:
            set_theme(self.theme_settings, self.current_light_theme)