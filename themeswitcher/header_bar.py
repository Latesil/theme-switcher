import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .theme_switcher_constants import theme_switcher_constants as constants
from .helper_functions import init_de
from .popover import Popover
import subprocess
import os

desktop = init_de()

@Gtk.Template(resource_path = constants["UI_PATH"] + 'ui/header_bar.ui')
class HeaderBar(Gtk.HeaderBar):

    __gtype_name__ = "HeaderBar"

    _left_label = Gtk.Template.Child()
    _left_switch = Gtk.Template.Child()
    _main_button = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        #connect signal for tracking changes in both directions
        #from programm to GSettings, and vice versa
        #self.settings.connect("changed::auto-switch", self.on__left_switch_change, self._left_switch)

        #get state of switch from gsettings
        self._left_switch.set_active(desktop.get_value("auto-switch"))

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
        button.set_active(desktop.get_value("auto-switch")) ######

    def on_time_visible_change(self, settings, key, button):
        pass

    #if switch state is off
    def state_off(self):
        desktop.set_value("auto-switch", False)
        desktop.set_value("time-visible", False)
        subprocess.call(['systemctl','--user','stop','theme-switcher-auto.timer'])
        subprocess.call(['systemctl','--user','disable', 'theme-switcher-auto.timer'])

    #if switch state is on
    def state_on(self):
        desktop.set_value("auto-switch", True)
        desktop.set_value("time-visible", True)
        subprocess.call(['systemctl','--user','start','theme-switcher-auto.timer'])
        subprocess.call(['systemctl','--user','enable','theme-switcher-auto.timer'])
