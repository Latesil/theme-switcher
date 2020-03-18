import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .theme_switcher_constants import theme_switcher_constants as constants
from .helper_functions import init_de
from .popover import Popover

desktop = init_de()

@Gtk.Template(resource_path = constants["UI_PATH"] + 'ui/header_bar.ui')
class HeaderBar(Gtk.HeaderBar):

    __gtype_name__ = "HeaderBar"

    _left_label = Gtk.Template.Child()
    _left_switch = Gtk.Template.Child()
    _main_button = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self._left_switch.set_active(desktop.get_value("auto-switch"))
        self._main_button.set_popover(Popover())


    @Gtk.Template.Callback()
    def on__left_switch_active_notify(self, settings, key):
        desktop.set_value("auto-switch", self._left_switch.get_active())
        
        bottom_box = self.get_parent().get_children()[0].get_children()[2]
        bottom_box._main_bottom_grid.set_visible(self._left_switch.get_active())
        if self._left_switch.get_active():
            #state = "on"
            desktop.start_systemd_timers()
        else:
            #state = "off"
            desktop.stop_systemd_timers()

    #if we touch switch in gsettings it change state in program
    def on__left_switch_change(self, settings, key, button):
        button.set_active(desktop.get_value("auto-switch")) ######
