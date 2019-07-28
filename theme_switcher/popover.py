from .theme_switcher_constants import theme_switcher_constants as constants
import locale
import subprocess
import os
from locale import gettext as _

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GdkPixbuf

resource = Gio.Resource.load("/home/lateseal/Documents/prog/python/pygtk/theme-switcher/data/theme-switcher.gresource")
resource._register()

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

        #init settings
        self.settings = Gio.Settings.new(constants["BASE_KEY"])

    #callback for change theme now
    @Gtk.Template.Callback()
    def on__change_theme_button_clicked(self, button):
        try:
            subprocess.call(['theme-switcher-manual.sh'])
        except:
            pass

    #other callbacks in our popover menu

    @Gtk.Template.Callback()
    def on__reset_time_button_clicked(self, button):
        self.settings.set_int("nighttime", 20)
        self.settings.set_int("daytime", 6)

    @Gtk.Template.Callback()
    def on__reset_themes_clicked(self, button):
        self.settings.set_string("light-theme", constants["default_light_theme"])
        self.settings.set_string("dark-theme", constants["default_dark_theme"])

    @Gtk.Template.Callback()
    def on__reset_wallpapers_clicked(self, button):
        self.settings.set_string("path-to-night-wallpaper", "")
        self.settings.set_string("path-to-day-wallpaper", "")

    @Gtk.Template.Callback()
    def on__reset_all_button_clicked(self, button):
        self.on__reset_time_button_clicked(button)
        self.on__reset_wallpapers_clicked(button)
        self.on__reset_themes_button_clicked(button)
        self.settings.set_boolean("auto-switch", True)

    @Gtk.Template.Callback()
    def on__about_button_clicked(self, button):
        image = GdkPixbuf.Pixbuf.new_from_resource(constants["UI_PATH"] + "icons/theme-switcher-128.png")

        about = Gtk.AboutDialog()
        about.set_program_name(_("Theme Switcher"))
        about.set_version("0.9")
        about.set_authors(["Letalis", "Artem Polishchuk","@DarthL1ne (Telegram)"])
        about.set_artists(["Raxi Petrov"])
        about.set_logo(image)
        about.set_copyright("(c) Copylefted")
        about.set_comments(_("A global automated switcher for dark/light GTK theme during day/night and more."))
        about.set_website("https://github.com/Latesil/theme-switcher")
        about.set_website_label(_("Report bugs or ideas"))
        about.set_wrap_license(True)
        about.set_license_type(Gtk.License.GPL_3_0)
        about.run()
        about.destroy()