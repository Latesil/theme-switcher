#!/usr/bin/python3

import subprocess
import datetime
import locale
import os
import itertools
from locale import gettext as _

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

#locales
locale.textdomain('com.github.Latesil.theme-switcher')

BASE_KEY = "com.github.Latesil.theme-switcher"
WALLPAPER_KEY = "org.gnome.desktop.background"
UI_PATH = '/com/github/Latesil/theme-switcher/ui/'

resource = Gio.Resource.load("/usr/share/theme-switcher/theme-switcher.gresource")
resource._register()

#helper functions
def get_resource_dirs(resource):
    dirs = [os.path.join(dir, resource)
            for dir in itertools.chain(GLib.get_system_data_dirs())]
    dirs += [os.path.join(os.path.expanduser("~"), ".{}".format(resource))]

    return [dir for dir in dirs if os.path.isdir(dir)]

def _get_valid_themes():
    gtk_ver = Gtk.MINOR_VERSION
    if gtk_ver % 2: # Want even number
        gtk_ver += 1

    valid = ['Adwaita', 'HighContrast', 'HighContrastInverse']
    valid += walk_directories(get_resource_dirs("themes"), lambda d:
                os.path.exists(os.path.join(d, "gtk-3.0", "gtk.css")) or \
                     os.path.exists(os.path.join(d, "gtk-3.{}".format(gtk_ver))))
    return set(valid)
    
def walk_directories(dirs, filter_func):
    valid = []
    try:
        for thdir in dirs:
            if os.path.isdir(thdir):
                for t in os.listdir(thdir):
                    if filter_func(os.path.join(thdir, t)):
                        valid.append(t)
    except:
        pass

    return valid

themes = _get_valid_themes()

@Gtk.Template(resource_path = UI_PATH + 'popover.ui')
class Popover(Gtk.PopoverMenu):

    __gtype_name__ = "Popover"

    _change_theme_button = Gtk.Template.Child()
    _reset_all_button = Gtk.Template.Child()
    _reset_time_button = Gtk.Template.Child()
    _reset_wallpapers = Gtk.Template.Child()
    _about_button = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        #init settings
        self.settings = Gio.Settings.new(BASE_KEY)

    #callback for change theme now
    @Gtk.Template.Callback()
    def on__change_theme_button_clicked(self, button):
        try:
            subprocess.call(['theme-switcher-manual.sh'])
        except:
            pass

    #other callbacks in our popover menu
    @Gtk.Template.Callback()
    def on__reset_all_button_clicked(self, button):
        self.settings.set_int("nighttime", 20)
        self.settings.set_int("daytime", 6)
        self.settings.set_string("path-to-night-wallpaper", "")
        self.settings.set_string("path-to-day-wallpaper", "")
        self.settings.set_boolean("auto-switch", True)

    @Gtk.Template.Callback()
    def on__reset_time_button_clicked(self, button):
        self.settings.set_int("nighttime", 20)
        self.settings.set_int("daytime", 6)

    @Gtk.Template.Callback()
    def on__reset_wallpapers_clicked(self, button):
        self.settings.set_string("path-to-night-wallpaper", "")
        self.settings.set_string("path-to-day-wallpaper", "")

    @Gtk.Template.Callback()
    def on__about_button_clicked(self, button):
        about = Gtk.AboutDialog()
        about.set_program_name("Theme Switcher")
        about.set_version("0.1")
        about.set_authors(["Letalis", 'atim77'])
        # about.set_icon('light-dark-icon.png')
        about.set_copyright("(c) Copylefted")
        about.set_comments("A global automated switcher for dark/light GTK theme during day/night and more.")
        about.set_website("https://github.com/Latesil/theme-switcher")
        about.set_wrap_license(True)
        about.set_license_type(Gtk.License.GPL_3_0)
        about.run()
        about.destroy()


@Gtk.Template(resource_path = UI_PATH + 'upper_grid.ui')
class UpperGrid(Gtk.Grid):

    __gtype_name__ = "UpperGrid"

    _day_button = Gtk.Template.Child()
    _night_button = Gtk.Template.Child()
    _day_label = Gtk.Template.Child()
    _night_label = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.settings = Gio.Settings.new(BASE_KEY)

        #monitor changes in gsettings
        self.settings.connect("changed::path-to-day-wallpaper", self.on__day_button_change, self._day_button)
        self.settings.connect("changed::path-to-night-wallpaper", self.on__night_button_change, self._night_button)

        #init button names
        self.set_day_button_label()
        self.set_night_button_label()

        self._day_label.set_halign(Gtk.Align.START)
        self._night_label.set_halign(Gtk.Align.START)
        self._day_button.set_margin_end(10)

    #callbacks for changes in wallpapers
    def on__day_button_change(self, settings, key, button):
        self.set_day_button_label()

    def on__night_button_change(self, settings, key, button):
        self.set_night_button_label()

    #get filename from path and set it to the button label
    def set_day_button_label(self):
        if not self.settings.get_string("path-to-day-wallpaper"):
            self._day_button.set_label(_("Choose Day Wallpaper"))
        else:
            day_wallpaper = self.settings.get_string("path-to-day-wallpaper")
            self._day_button.set_label(day_wallpaper.split("/")[-1])

    def set_night_button_label(self):
        if not self.settings.get_string("path-to-night-wallpaper"):
            self._night_button.set_label(_("Choose Night Wallpaper"))
        else:
            night_wallpaper = self.settings.get_string("path-to-night-wallpaper")
            self._night_button.set_label(night_wallpaper.split("/")[-1])

    #set two callbacks for wallpapers buttons
    @Gtk.Template.Callback()
    def on__night_button_clicked(self, button):
        dialog = Gtk.FileChooserDialog(_("Choose a file for night"), None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            night_wallpaper = dialog.get_filename()
            self.settings.set_string("path-to-night-wallpaper", night_wallpaper)
            self._night_button.set_label(night_wallpaper.split("/")[-1])
            current_time = datetime.datetime.now()
            if (current_time.hour >= self.settings.get_int("nighttime")):
                self.set_wallpaper(night_wallpaper)
        dialog.destroy()

    @Gtk.Template.Callback()
    def on__day_button_clicked(self, button):
        dialog = Gtk.FileChooserDialog(_("Choose a file for day"), None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            day_wallpaper = dialog.get_filename()
            self.settings.set_string("path-to-day-wallpaper", day_wallpaper)
            self._day_button.set_label(day_wallpaper.split("/")[-1])
            current_time = datetime.datetime.now()
            if (current_time.hour >= self.settings.get_int("daytime")):
                self.set_wallpaper(day_wallpaper)
        dialog.destroy()

    #helper function for filter choosing file dialog
    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Pictures")
        filter_text.add_mime_type("image/jpeg")
        filter_text.add_mime_type("image/png")
        dialog.add_filter(filter_text)

    #helper function for setting wallpapers
    def set_wallpaper(self, wallpaper):
        wallpaper_settings = Gio.Settings.new(WALLPAPER_KEY)
        wallpaper_settings.set_string("picture-uri", wallpaper)


@Gtk.Template(resource_path = UI_PATH + 'middle_box.ui')
class MiddleBox(Gtk.Box):

    __gtype_name__ = "MiddleBox"
    
    _middle_box_label = Gtk.Template.Child()
    _dark_theme_label = Gtk.Template.Child()
    _light_theme_label = Gtk.Template.Child()
    _light_combo_box = Gtk.Template.Child()
    _dark_combo_box = Gtk.Template.Child()
    _middle_box_grid = Gtk.Template.Child()
    _light_tree_model = Gtk.Template.Child()
    _dark_tree_model = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.set_margin_top(10)

        self._light_theme_label.set_halign(Gtk.Align.START)
        self._dark_theme_label.set_halign(Gtk.Align.START)
        self._light_combo_box.set_margin_end(10)

        #populate theme list
        for i in themes:
            self._light_tree_model.append([i])
            self._dark_tree_model.append([i])

        #init light box
        self._light_combo_box.connect("changed", self.on__light_combo_box_changed)
        renderer_text = Gtk.CellRendererText()
        self._light_combo_box.pack_start(renderer_text, True)
        self._light_combo_box.add_attribute(renderer_text, "text", 0)

        #init dark box
        self._dark_combo_box.connect("changed", self.on__dark_combo_box_changed)
        renderer_text = Gtk.CellRendererText()
        self._dark_combo_box.pack_start(renderer_text, True)
        self._dark_combo_box.add_attribute(renderer_text, "text", 0)


    def on__light_combo_box_changed(self, combo):
        self.combo_box_changed(combo)

    def on__dark_combo_box_changed(self, combo):
        self.combo_box_changed(combo)

    def combo_box_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            theme = model[tree_iter][0]
            print("Selected: %s" % theme)
        

@Gtk.Template(resource_path = UI_PATH + 'bottom_box.ui')
class BottomBox(Gtk.Box):

    __gtype_name__ = "BottomBox"

    _bottom_label = Gtk.Template.Child()
    _day_scale = Gtk.Template.Child()
    _night_scale = Gtk.Template.Child()
    _bottom_day_label = Gtk.Template.Child()
    _bottom_night_label = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        #init settings
        self.settings = Gio.Settings.new(BASE_KEY)
        self.set_margin_top(20)

        #monitor changes in gsettings
        self.settings.connect("changed::daytime", self.on__day_scale_change, self._day_scale)
        self.settings.connect("changed::nighttime", self.on__night_scale_change, self._night_scale)

        #get values from gsettings after start programm
        self.get_scales_values()

        self._bottom_day_label.set_halign(Gtk.Align.START)
        self._bottom_night_label.set_halign(Gtk.Align.START)

    def on__day_scale_change(self, settings, key, button):
        self._day_scale.set_value(self.settings.get_int("daytime"))

    def on__night_scale_change(self, settings, key, button):
        self._night_scale.set_value(self.settings.get_int("nighttime"))

    def get_scales_values(self):
        self.on__day_scale_change(self.settings, "daytime", self._day_scale)
        self.on__night_scale_change(self.settings, "nighttime", self._night_scale)

    #set two callbacks for scale
    @Gtk.Template.Callback()
    def on__day_adjustment_value_changed(self, scale):
        self.settings.set_int("daytime", scale.get_value())

    @Gtk.Template.Callback()
    def on__night_adjustment_value_changed(self, scale):
        self.settings.set_int("nighttime", scale.get_value())


@Gtk.Template(resource_path = UI_PATH + 'main_window.ui')
class Window(Gtk.Window):

    __gtype_name__ = "Window"

    _main_box = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self._main_box.set_border_width(10)

        #init header_bar
        self.header_bar = HeaderBar()
        self.set_titlebar(self.header_bar)
        self.header_bar.show()

        #init two containers for our widgets
        self.upper_grid = UpperGrid()
        self.middle_box = MiddleBox()
        self.bottom_box = BottomBox()

        #add our containers to the main one
        self._main_box.add(self.upper_grid)
        self._main_box.add(self.middle_box)
        self._main_box.add(self.bottom_box)


@Gtk.Template(resource_path = UI_PATH + 'header_bar.ui')
class HeaderBar(Gtk.HeaderBar):

    __gtype_name__ = "HeaderBar"

    _left_label = Gtk.Template.Child()
    _left_switch = Gtk.Template.Child()
    _main_button = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        #init main settings
        self.settings = Gio.Settings.new(BASE_KEY)

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
        subprocess.call(['systemctl','--user','disable', '--now','theme-switcher-auto.timer'])

    #if switch state is on
    def state_on(self):
        self.settings.set_boolean("auto-switch", self._left_switch.get_active())
        subprocess.call(['systemctl','--user','enable', '--now','theme-switcher-auto.timer'])


#init main window
win = Window()

#connect quit event
win.connect("delete_event", Gtk.main_quit)

#show all inside window
win.show_all()

#main loop
Gtk.main()
