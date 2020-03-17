import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os

from .theme_switcher_constants import theme_switcher_constants as constants
from .helper_functions import init_de
import datetime
from locale import gettext as _
import locale

desktop = init_de()

@Gtk.Template(resource_path = constants["UI_PATH"] + 'ui/upper_grid.ui')
class UpperGrid(Gtk.Grid):

    __gtype_name__ = "UpperGrid"

    _day_button = Gtk.Template.Child()
    _night_button = Gtk.Template.Child()
    _day_label = Gtk.Template.Child()
    _night_label = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self._day_button.set_name("day_button")
        self._night_button.set_name("night_button")

        self._day_button.connect("clicked", self.wallpaper_button_clicked)
        self._night_button.connect("clicked", self.wallpaper_button_clicked)

        #monitor changes in gsettings
        #self.settings.connect("changed::path-to-day-wallpaper", self.on__day_button_change, self._day_button)
        #self.settings.connect("changed::path-to-night-wallpaper", self.on__night_button_change, self._night_button)

        #init button names
        self.set_day_button_label()
        self.set_night_button_label()

        self._day_label.set_halign(Gtk.Align.START)
        self._night_label.set_halign(Gtk.Align.START)
        self._day_button.set_margin_end(10)

    #callbacks for changes in wallpapers
    def on__day_button_change(self, settings, key, button):
        self.set_day_button_label()

    def on__night_button_change(self, settings, key, button):
        self.set_night_button_label()

    #get filename from path and set it to the button label
    def set_day_button_label(self):
        if not desktop.get_value("path-to-day-wallpaper"):
            self._day_button.set_label(_("Choose Day Wallpaper"))
        else:
            day_wallpaper = desktop.get_value("path-to-day-wallpaper")
            self._day_button.set_label(day_wallpaper.split("/")[-1])

    def set_night_button_label(self):
        if not desktop.get_value("path-to-night-wallpaper"):
            self._night_button.set_label(_("Choose Night Wallpaper"))
        else:
            night_wallpaper = desktop.get_value("path-to-night-wallpaper")
            self._night_button.set_label(night_wallpaper.split("/")[-1])

    def wallpaper_button_clicked(self, button):
        dialog = Gtk.FileChooserDialog(_("Choose a file"), None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            wallpaper = dialog.get_filename()
            name = button.get_name()
            if name == "night_button":
                desktop.set_value("path-to-night-wallpaper", wallpaper)
                self._night_button.set_label(wallpaper.split("/")[-1])
                current_time = datetime.datetime.now()
                if (current_time.hour >= desktop.get_value("nighttime")):
                    desktop.set_wallpapers(wallpaper)
            elif name == "day_button":
                desktop.set_value("path-to-day-wallpaper", wallpaper)
                self._day_button.set_label(wallpaper.split("/")[-1])
                current_time = datetime.datetime.now()
                if (current_time.hour <= desktop.get_value("daytime")):
                    desktop.set_wallpapers(wallpaper)
        dialog.destroy()

    #helper function for filter choosing file dialog
    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Pictures")
        filter_text.add_mime_type("image/jpeg")
        filter_text.add_mime_type("image/png")
        dialog.add_filter(filter_text)

