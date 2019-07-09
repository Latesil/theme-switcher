#!/usr/bin/python3

import subprocess
import datetime
from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class MyWindow(Gtk.Window):

    BASE_KEY = "org.theme-switcher"
    WALLPAPER_KEY = "org.gnome.desktop.background"
    current_time = datetime.datetime.now()

    def __init__(self):
    
        Gtk.Window.__init__(self, title=_("Theme Switcher"))
        
        self.set_border_width(10)
        self.set_default_size(400, 200)
        
        self.init_headerbar()
        self.set_titlebar(self.header_bar)
        
        self.box = Gtk.Box(spacing=6)
        self.box.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(self.box)
        
        self.init_upper_grid()
        self.init_bottom_grid()
        
        self.box.pack_start(self.upper_grid, True, True, 0)
        self.box.pack_start(self.bottom_grid, True, True, 0)
        
    def set_wallpaper(self, wallpaper):
        wallpaper_settings = Gio.Settings.new(self.WALLPAPER_KEY)
        wallpaper_settings.set_string("picture-uri", wallpaper)

    def on_about(self, button):
        about = Gtk.AboutDialog()
        about.set_program_name("Theme Switcher")
        about.set_version("0.1")
        about.set_authors(["Letalis", 'atim77'])
        # about.set_icon('light-dark-icon.png')
        about.set_copyright("(c) copylefted")
        about.set_comments("A global automated switcher for dark/light GTK theme during day/night and more.")
        about.set_website("https://github.com/Latesil/theme-switcher")
        about.set_wrap_license(True)
        about.set_license("""Theme Switcher is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Theme Switcher is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Theme Switcher; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.""")
        about.run()
        about.destroy()
        
    def state_off(self):
        self.settings.set_boolean("auto-switch", self.auto_button.get_active())
        subprocess.call(['systemctl','--user','disable', '--now','theme-switcher-auto.timer'])
        
    def state_on(self):
        self.settings.set_boolean("auto-switch", self.auto_button.get_active())
        subprocess.call(['systemctl','--user','enable', '--now','theme-switcher-auto.timer'])
        
    def on_day_wallpaper_choose(self, widget):
        dialog = Gtk.FileChooserDialog(_("Choose a file"), self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        self.add_filters(dialog)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            day_wallpaper = dialog.get_filename()
            self.settings.set_string("path-to-day-wallpaper", day_wallpaper)
            self.file_button_day.set_label(day_wallpaper.split("/")[-1])
            if (self.current_time.hour <= self.settings.get_int("daytime")):
                self.set_wallpaper(day_wallpaper)
        dialog.destroy()            
        
    def on_night_wallpaper_choose(self, widget):
        dialog = Gtk.FileChooserDialog(_("Choose a file"), self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        self.add_filters(dialog)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            night_wallpaper = dialog.get_filename()
            self.settings.set_string("path-to-night-wallpaper", night_wallpaper)
            self.file_button_night.set_label(night_wallpaper.split("/")[-1])
            if (self.current_time.hour >= self.settings.get_int("nighttime")):
                self.set_wallpaper(night_wallpaper)
        dialog.destroy()
            
    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("image/jpeg")
        filter_text.add_mime_type("image/png")
        dialog.add_filter(filter_text)
                
    def on_auto_toggled(self, auto_button, gparam):
        if self.auto_button.get_active():
            #state = "on"
            self.state_on()
        else:
            #state = "off"
            self.state_off()
            
    def on_auto_switch_change(self, settings, key, auto_button):
        self.auto_button.set_active(settings.get_boolean("auto-switch"))
        
    def on_main_button_clicked(self, button):
        self.popover.set_relative_to(button)
        self.popover.show_all()
        self.popover.popup()
        
    def on_change_theme_button(self, button):
        try:
            subprocess.call(['theme-switcher-manual.sh'])
        except:
            pass
        
    def on_reset_wallpapers(self, button):
        self.settings.set_string("path-to-night-wallpaper", "")
        self.settings.set_string("path-to-day-wallpaper", "")
        self.file_button_night.set_label(_("Choose Night Wallpaper"))
        self.file_button_day.set_label(_("Choose Day Wallpaper"))
        
    def reset_time(self, button):
        self.settings.set_int("nighttime", 20)
        self.settings.set_int("daytime", 6)
        self.day_scale.set_value(self.settings.get_int("daytime"))
        self.night_scale.set_value(self.settings.get_int("nighttime"))
        
    def reset(self, button):
        
        #maybe there is another way to reset?
        self.settings.set_int("nighttime", 20)
        self.settings.set_int("daytime", 6)
        self.settings.set_string("path-to-night-wallpaper", "")
        self.settings.set_string("path-to-day-wallpaper", "")
        self.settings.set_boolean("auto-switch", True)
        self.day_scale.set_value(self.settings.get_int("daytime"))
        self.night_scale.set_value(self.settings.get_int("nighttime"))
        self.auto_button.set_active(self.settings.get_boolean("auto-switch"))
        self.file_button_night.set_label(_("Choose Night Wallpaper"))
        self.file_button_day.set_label(_("Choose Day Wallpaper"))
        
    def init_headerbar(self):
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = _("Theme Switcher")
        
        header_box = Gtk.Box(spacing=6)
        header_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        
        header_label = Gtk.Label(label=_("Auto:"))
        header_box.add(header_label)
        
        self.auto_button = Gtk.Switch()
        
        self.settings = Gio.Settings.new(self.BASE_KEY)
        self.settings.connect("changed::auto-switch", self.on_auto_switch_change, self.auto_button)
        
        self.auto_button.set_active(self.settings.get_boolean("auto-switch"))
        self.auto_button.connect("notify::active", self.on_auto_toggled)
        header_box.add(self.auto_button)
        
        self.header_bar.pack_start(header_box)

        self.builder = Gtk.Builder()
        self.builder.add_from_file('ui/popover.ui')

        self.popover = self.builder.get_object('_main_popover')

        self.builder.connect_signals(self)
        
        main_button = Gtk.Button.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.BUTTON)

        main_button.connect("clicked", self.on_main_button_clicked)
        self.header_bar.pack_end(main_button)
        
    def init_upper_grid(self):
        self.upper_grid = Gtk.Grid()
        self.upper_grid.set_column_homogeneous(True)
        self.upper_grid.set_row_homogeneous(True)
        
        label_day = Gtk.Label(label=_("File for day:"))
        label_day.set_halign(Gtk.Align.START)
        self.upper_grid.add(label_day)
        
        self.file_button_day = Gtk.Button()
        if not self.settings.get_string("path-to-day-wallpaper"):
            self.file_button_day.set_label(_("Choose Day Wallpaper"))
        else:
            day_wallpaper = self.settings.get_string("path-to-day-wallpaper")
            self.file_button_day.set_label(day_wallpaper.split("/")[-1])
        self.file_button_day.set_margin_end(10)
        self.file_button_day.connect("clicked", self.on_day_wallpaper_choose)
        self.upper_grid.attach_next_to(self.file_button_day, label_day, Gtk.PositionType.BOTTOM, 1, 1)
        
        label_night = Gtk.Label(label=_("File for night:"))
        label_night.set_halign(Gtk.Align.START)
        self.upper_grid.attach_next_to(label_night, label_day, Gtk.PositionType.RIGHT, 1, 1)
        
        self.file_button_night = Gtk.Button()
        if not self.settings.get_string("path-to-night-wallpaper"):
            self.file_button_night.set_label(_("Choose Night Wallpaper"))
        else:
            night_wallpaper = self.settings.get_string("path-to-night-wallpaper")
            self.file_button_night.set_label(night_wallpaper.split("/")[-1])
        self.file_button_night.connect("clicked", self.on_night_wallpaper_choose)
        self.upper_grid.attach_next_to(self.file_button_night, label_night, Gtk.PositionType.BOTTOM, 1, 1)
        
    def on_day_value_changed(self, scale):
        self.settings.set_int("daytime", scale.get_value())
        
    def on_night_value_changed(self, scale):
        self.settings.set_int("nighttime", scale.get_value())
        
    def init_bottom_grid(self):
        self.bottom_grid = Gtk.Grid()
        self.bottom_grid.set_column_homogeneous(True)
        self.bottom_grid.set_row_homogeneous(True)
        
        time_label = Gtk.Label(label=_("Time Manage:"))
        self.bottom_grid.add(time_label)
        
        daytime_box = Gtk.Box()
        daytime_box.set_homogeneous(True)
        daytime_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        day_label = Gtk.Label(label=_("Daytime: "))
        day_label.set_halign(Gtk.Align.START)
        daytime_box.add(day_label)
        
        self.day_scale = Gtk.Scale()
        self.day_scale.set_range(0, 23)
        self.day_scale.set_digits(0)
        self.day_scale.set_draw_value(True)
        self.day_scale.set_value_pos(Gtk.PositionType.LEFT)
        self.day_scale.set_value(self.settings.get_int("daytime"))
        self.day_scale.connect("value_changed", self.on_day_value_changed)
        daytime_box.add(self.day_scale)
        
        nighttime_box = Gtk.Box()
        nighttime_box.set_homogeneous(True)
        nighttime_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        night_label = Gtk.Label(label=_("Night: "))
        night_label.set_halign(Gtk.Align.START)
        nighttime_box.add(night_label)
        
        self.night_scale = Gtk.Scale()
        self.night_scale.set_range(0, 23)
        self.night_scale.set_digits(0)
        self.night_scale.set_draw_value(True)
        self.night_scale.set_value_pos(Gtk.PositionType.LEFT)
        self.night_scale.set_value(self.settings.get_int("nighttime"))
        self.night_scale.connect("value_changed", self.on_night_value_changed)
        nighttime_box.add(self.night_scale)
        
        self.bottom_grid.attach_next_to(daytime_box, time_label, Gtk.PositionType.BOTTOM, 1, 1)
        self.bottom_grid.attach_next_to(nighttime_box, daytime_box, Gtk.PositionType.BOTTOM, 1, 1)
        
        
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
