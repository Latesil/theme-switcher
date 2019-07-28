import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

from src.theme_switcher_constants import theme_switcher_constants as constants
from .popover import Popover
import subprocess
import os

resource = Gio.Resource.load("/home/lateseal/Documents/prog/python/pygtk/theme-switcher/data/theme-switcher.gresource")
resource._register()

@Gtk.Template(resource_path = constants["UI_PATH"] + 'ui/header_bar.ui')
class HeaderBar(Gtk.HeaderBar):

    __gtype_name__ = "HeaderBar"

    _left_label = Gtk.Template.Child()
    _left_switch = Gtk.Template.Child()
    _main_button = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        #init main settings
        self.settings = Gio.Settings.new(constants["BASE_KEY"])

        #connect signal for tracking changes in both directions
        #from programm to GSettings, and vice versa
        self.settings.connect("changed::auto-switch", self.on__left_switch_change, self._left_switch)

        #get state of switch from gsettings
        self._left_switch.set_active(self.settings.get_boolean("auto-switch"))

        #add popover menu to main_button
        self._main_button.set_popover(Popover())

    #send information about state of switch
    @Gtk.Template.Callback()
    def on__left_switch_active_notify(self, settings, key):
        if self._left_switch.get_active():
            #state = "on"
            self.state_on()
        else:
            #state = "off"
            self.state_off()

    #if we touch switch in gsettings it change state in program
    def on__left_switch_change(self, settings, key, button):
        self._left_switch.set_active(settings.get_boolean("auto-switch"))

    #if switch state is off
    def state_off(self):
        self.settings.set_boolean("auto-switch", self._left_switch.get_active())
        subprocess.call(['systemctl','--user','stop','theme-switcher-auto.timer'])
        subprocess.call(['systemctl','--user','disable', 'theme-switcher-auto.timer'])

    #if switch state is on
    def state_on(self):
        self.settings.set_boolean("auto-switch", self._left_switch.get_active())
        subprocess.call(['systemctl','--user','start','theme-switcher-auto.timer'])
        subprocess.call(['systemctl','--user','enable','theme-switcher-auto.timer'])
