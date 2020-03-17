from .theme_switcher_constants import theme_switcher_constants as constants
import locale
import subprocess
import datetime
import os
from locale import gettext as _
from .helper_functions import _get_valid_themes, init_de

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

desktop = init_de()
themes = sorted(_get_valid_themes())

@Gtk.Template(resource_path = constants["UI_PATH"] + 'ui/middle_box.ui')
class MiddleGrid(Gtk.Grid):

    __gtype_name__ = "MiddleGrid"
    
    _dark_theme_label = Gtk.Template.Child()
    _light_theme_label = Gtk.Template.Child()
    _light_combo_box = Gtk.Template.Child()
    _dark_combo_box = Gtk.Template.Child()
    _light_tree_model = Gtk.Template.Child()
    _dark_tree_model = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.set_margin_top(10)

        self.current_theme = desktop.get_current_theme()

        self.cur_light_theme, self.cur_dark_theme = desktop.get_current_themes()

        #self.main_settings.connect("changed::light-theme", self.on_light_theme_change, self._light_combo_box)
        #self.main_settings.connect("changed::dark-theme", self.on_dark_theme_change, self._dark_combo_box)

        self._light_theme_label.set_halign(Gtk.Align.START)
        self._dark_theme_label.set_halign(Gtk.Align.START)
        self._light_combo_box.set_margin_end(10)
        self._light_combo_box.set_name("light_box")
        self._dark_combo_box.set_name("dark_box")
        # if self.current_theme not in themes:
        #     self._light_tree_model.append([self.current_theme])

        #populate theme list
        for i in themes:
            self._light_tree_model.append([i])
            self._dark_tree_model.append([i])

        #retrieve current light\dark theme and set it as a default option in combo box
        self.retrieve_light_theme(self._light_combo_box)
        self.retrieve_dark_theme(self._dark_combo_box)

        #init light box
        self._light_combo_box.connect("changed", self.combo_box_changed)
        renderer_text = Gtk.CellRendererText()
        self._light_combo_box.pack_start(renderer_text, True)
        self._light_combo_box.add_attribute(renderer_text, "text", 0)

        #init dark box
        self._dark_combo_box.connect("changed", self.combo_box_changed)
        renderer_text = Gtk.CellRendererText()
        self._dark_combo_box.pack_start(renderer_text, True)
        self._dark_combo_box.add_attribute(renderer_text, "text", 0)

    def on_light_theme_change(self, settings, key, box):
        self.cur_light_theme = desktop.get_current_themes()[0]
        self.retrieve_light_theme(box)

    def on_dark_theme_change(self, settings, key, box):
        self.cur_dark_theme = desktop.get_current_themes()[1]
        self.retrieve_dark_theme(box)

    def retrieve_light_theme(self, box):
        self._light_model = box.get_model()
        for row in self._light_model:
            if row[0] == self.cur_light_theme:
                box.set_active_iter(row.iter)

    def retrieve_dark_theme(self, box):
        self._dark_model = box.get_model()
        for row in self._dark_model:
            if row[0] == self.cur_dark_theme:
                box.set_active_iter(row.iter)


    def combo_box_changed(self, combo):
        name = combo.get_name()
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            combo.set_active_iter(tree_iter)
            theme = model[tree_iter][0]

            if name == 'light_box':
                desktop.set_value('light-theme', theme)
                current_time = datetime.datetime.now()
                if (current_time.hour <= desktop.get_value("daytime")):
                    desktop.set_current_theme(self.theme_settings, theme)

            if name == 'dark_box':
                desktop.set_value('dark-theme', theme)
                current_time = datetime.datetime.now()
                if (current_time.hour >= desktop.get_value("nighttime")):
                    desktop.set_current_theme(self.theme_settings, theme)
