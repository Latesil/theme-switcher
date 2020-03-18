import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .theme_switcher_constants import theme_switcher_constants as constants
from .helper_functions import init_de
from .popover import Popover
from .bottom_box import BottomBox

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
    def on__left_switch_state_set(self, widget, state):
        desktop.set_value("auto-switch", state)
        
        bottom_box = self.get_parent().get_children()[0].get_children()[2]
        bottom_box._main_bottom_grid.set_visible(state)
        
        if state:
            desktop.start_systemd_timers()
        else:
            desktop.stop_systemd_timers()
