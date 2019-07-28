import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from .theme_switcher_constants import theme_switcher_constants as constants
from locale import gettext as _

from .header_bar import HeaderBar
from .upper_grid import UpperGrid
from .middle_box import MiddleGrid
from .bottom_box import BottomBox

resource = Gio.Resource.load("/home/lateseal/Documents/prog/python/pygtk/theme-switcher/data/theme-switcher.gresource")
resource._register()

@Gtk.Template(resource_path = constants["UI_PATH"] + 'ui/main_window.ui')
class AppWindow(Gtk.ApplicationWindow):

    __gtype_name__ = "AppWindow"

    _main_box = Gtk.Template.Child()

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, title=_("Theme Switcher"), application=app)

        self._main_box.set_border_width(10)
        self.set_default_geometry(1000, 200)

        self.settings = Gio.Settings.new(constants["BASE_KEY"])

        #init header_bar
        self.header_bar = HeaderBar()
        self.set_titlebar(self.header_bar)
        self.header_bar.show()

        #init two containers for our widgets
        self.upper_grid = UpperGrid()
        self.middle_box = MiddleGrid()
        self.bottom_box = BottomBox()

        #add our containers to the main one
        self._main_box.add(self.upper_grid)
        self._main_box.add(self.middle_box)
        self._main_box.add(self.bottom_box)
