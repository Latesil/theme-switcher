from .theme_switcher_constants import theme_switcher_constants as constants
from .helper_functions import init_de
import locale
import subprocess
import os
from locale import gettext as _

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

desktop = init_de()

@Gtk.Template(resource_path = constants["UI_PATH"] + 'ui/popover.ui')
class Popover(Gtk.PopoverMenu):

    __gtype_name__ = "Popover"

    _change_theme_button = Gtk.Template.Child()
    _reset_all_button = Gtk.Template.Child()
    _reset_time_button = Gtk.Template.Child()
    _reset_themes = Gtk.Template.Child()
    _reset_wallpapers = Gtk.Template.Child()
    _about_button = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

    #callback for change theme now
    @Gtk.Template.Callback()
    def on__change_theme_button_clicked(self, button):
        try:
            subprocess.call(['theme-switcher-manual.py'])
        except:
            pass

    #other callbacks in our popover menu

    @Gtk.Template.Callback()
    def on__reset_time_button_clicked(self, button):
        desktop.set_value("nighttime", 20)
        desktop.set_value("daytime", 6)

    @Gtk.Template.Callback()
    def on__reset_themes_clicked(self, button):
        desktop.set_value("light-theme", constants["default_light_theme"])
        desktop.set_value("dark-theme", constants["default_dark_theme"])

    @Gtk.Template.Callback()
    def on__reset_wallpapers_clicked(self, button):
        desktop.set_value("path-to-night-wallpaper", "")
        desktop.set_value("path-to-day-wallpaper", "")

    @Gtk.Template.Callback()
    def on__reset_all_button_clicked(self, button):
        self.on__reset_time_button_clicked(button)
        self.on__reset_wallpapers_clicked(button)
        self.on__reset_themes_clicked(button)
        desktop.set_value("auto-switch", True)

    @Gtk.Template.Callback()
    def on__about_button_clicked(self, button):
        about = Gtk.AboutDialog()
        about.set_program_name(_("Theme Switcher"))
        about.set_version("1.0.0")
        about.set_authors(["Letalis", "Artem Polishchuk", "@DarthL1ne (Telegram)", "@dead_mozay"])
        about.set_artists(["Raxi Petrov"])
        about.set_logo_icon_name(constants["APP_ID"])
        about.set_copyright("GPLv3+")
        about.set_comments(_("A global automated switcher for dark/light GTK theme during day/night and more."))
        about.set_website("https://github.com/Latesil/theme-switcher")
        about.set_website_label(_("Website"))
        about.set_wrap_license(True)
        about.set_license_type(Gtk.License.GPL_3_0)
        about.run()
        about.destroy()
