#!/usr/bin/python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#test

import locale
import sys
import os
from locale import gettext as _
from .theme_switcher_constants import theme_switcher_constants as constants

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, GdkPixbuf

from .popover import Popover
from .main_window import AppWindow

#locales
locale.textdomain('com.github.Latesil.theme-switcher')

def main():
	app = Application()
	return app.run(sys.argv)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="com.github.Latesil.theme-switcher",
                        flags=Gio.ApplicationFlags.FLAGS_NONE, **kwargs)

        self.window = None

        GLib.set_application_name(_('Theme Switcher'))
        GLib.set_prgname(constants["APP_NAME"])

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(self)

        self.window.present()

    #test new branch
    def on_about(self, action, param):
        popover = Popover()
        popover.on__about_button_clicked(None)

    def on_quit(self, action, param):
        self.quit()

