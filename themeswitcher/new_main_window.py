import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GdkPixbuf
from Themeswitcher.helper_functions import init_de, convert_to_values
from Themeswitcher.theme_switcher_constants import theme_switcher_constants as constants
from locale import gettext as _
import os
import datetime
import subprocess

desktop = init_de()
themes = sorted(desktop._get_valid_themes())

@Gtk.Template(resource_path = constants["UI_PATH"] + 'ui/new_window.ui')
class AppWindow(Gtk.ApplicationWindow):

    __gtype_name__ = "AppWindow"
    
    _left_switch = Gtk.Template.Child()
    _day_button = Gtk.Template.Child()
    _night_button = Gtk.Template.Child()
    _light_combo_box = Gtk.Template.Child()
    _dark_combo_box = Gtk.Template.Child()
    _day_hour_spin_button = Gtk.Template.Child()
    _day_minutes_spin_button = Gtk.Template.Child()
    _night_hour_spin_button = Gtk.Template.Child()
    _night_minutes_spin_button = Gtk.Template.Child()
    _change_theme_button = Gtk.Template.Child()
    _reset_all_button = Gtk.Template.Child()
    _reset_time_button = Gtk.Template.Child()
    _reset_themes = Gtk.Template.Child()
    _reset_wallpapers = Gtk.Template.Child()
    _about_button = Gtk.Template.Child()
    day_time_main_frame = Gtk.Template.Child() #
    night_time_main_frame = Gtk.Template.Child() #
    night_wallpaper_image_box = Gtk.Template.Child()
    day_wallpaper_image_box = Gtk.Template.Child()
    _light_tree_model = Gtk.Template.Child()
    _dark_tree_model = Gtk.Template.Child()
    
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, title=_("Theme Switcher"), application=app)

        self.set_wmclass("Theme Switcher", _("Theme Switcher"))
        
        self.current_theme = desktop.get_current_theme()
        self.cur_light_theme, self.cur_dark_theme = desktop.get_current_themes()
        self._light_combo_box.set_name("light_box")
        self._dark_combo_box.set_name("dark_box")
        
        self._day_button.set_name("day_button")
        self._night_button.set_name("night_button")
        self._day_button.connect("clicked", self.wallpaper_button_clicked)
        self._night_button.connect("clicked", self.wallpaper_button_clicked)
        
        self.night_time_main_frame.set_visible(desktop.get_value("auto-switch"))
        self.day_time_main_frame.set_visible(desktop.get_value("auto-switch"))
        
        self.current_day_wallpaper = desktop.get_value("path-to-day-wallpaper")
        self.current_night_wallpaper = desktop.get_value("path-to-night-wallpaper")
        
        if self.current_day_wallpaper != "":
            image = Gtk.Image()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.current_day_wallpaper, 114, 64, True)
            image.set_from_pixbuf(pixbuf)
            self.day_wallpaper_image_box.pack_start(image, True, True, 2)
            image.show()
            
        if self.current_night_wallpaper != "":
            image = Gtk.Image()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.current_night_wallpaper, 114, 64, True)
            image.set_from_pixbuf(pixbuf)
            self.night_wallpaper_image_box.pack_start(image, True, True, 2)
            image.show()
        
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
        
        self.set_values_from_settings()
        self.on_combo_box_changed()

    @Gtk.Template.Callback()
    def on__left_switch_state_set(self, widget, state):
        desktop.set_value("auto-switch", state)
        
        if state:
            self.night_time_main_frame.set_visible(True)
            self.day_time_main_frame.set_visible(True)
            desktop.start_systemd_timers()
        else:
            self.night_time_main_frame.set_visible(False)
            self.day_time_main_frame.set_visible(False)
            desktop.stop_systemd_timers()
        
    @Gtk.Template.Callback()
    def on__day_hour_adjustment_value_changed(self, scale):
        desktop.set_value("daytime-hour", scale.get_value())
        self.on_combo_box_changed()
        
    @Gtk.Template.Callback()
    def on__day_minutes_adjustment_value_changed(self, scale):
        desktop.set_value("daytime-minutes", scale.get_value())
        self.on_combo_box_changed()
        
    @Gtk.Template.Callback()
    def on__night_minutes_adjustment_value_changed(self, scale):
        desktop.set_value("nighttime-minutes", scale.get_value())
        self.on_combo_box_changed()
    
    @Gtk.Template.Callback()
    def on__night_hour_adjustment_value_changed(self, scale):
        desktop.set_value("nighttime-hour", scale.get_value())
        self.on_combo_box_changed()
        
    #callback for change theme now
    @Gtk.Template.Callback()
    def on__change_theme_button_clicked(self, button):
        try:
            subprocess.call(['theme-switcher-manual.py'])
        except:
            pass

    #other callbacks in our popover menu

    @Gtk.Template.Callback()
    def on__reset_time_button_clicked(self, button):
        desktop.reset_value("nighttime")
        desktop.reset_value("daytime")

    @Gtk.Template.Callback()
    def on__reset_themes_clicked(self, button):
        desktop.reset_value("light-theme")
        desktop.reset_value("dark-theme")

    @Gtk.Template.Callback()
    def on__reset_wallpapers_clicked(self, button):
        desktop.reset_value("path-to-night-wallpaper")
        desktop.reset_value("path-to-day-wallpaper")

    @Gtk.Template.Callback()
    def on__reset_all_button_clicked(self, button):
        self.on__reset_time_button_clicked(button)
        self.on__reset_wallpapers_clicked(button)
        self.on__reset_themes_clicked(button)
        desktop.reset_value("auto-switch")

    @Gtk.Template.Callback()
    def on__about_button_clicked(self, button):
        about = Gtk.AboutDialog()
        about.set_program_name(_("Theme Switcher"))
        about.set_version("1.9.0")
        about.set_authors(["Letalis", "Artem Polishchuk", "@DarthL1ne (Telegram)", "@dead_mozay"])
        about.set_artists(["Raxi Petrov"])
        about.set_logo_icon_name(constants["APP_ID"])
        about.set_copyright("GPLv3+")
        about.set_comments(_("A global automated switcher for dark/light GTK theme during day/night and more."))
        about.set_website("https://github.com/Latesil/theme-switcher")
        about.set_website_label(_("Website"))
        about.set_wrap_license(True)
        about.set_license_type(Gtk.License.GPL_3_0)
        about.run()
        about.destroy()
        
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
                    desktop.set_current_theme(theme)

            if name == 'dark_box':
                desktop.set_value('dark-theme', theme)
                current_time = datetime.datetime.now()
                if (current_time.hour >= desktop.get_value("nighttime")):
                    desktop.set_current_theme(theme)
    
    def wallpaper_button_clicked(self, button):
        dialog = Gtk.FileChooserDialog(_("Choose a file"), None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            wallpaper = dialog.get_filename()
            image = Gtk.Image()
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(wallpaper, 114, 64, True)
                image.set_from_pixbuf(pixbuf)
            except Exception:
                print('Error occured')
                image.set_from_icon_name('dialog-error-symbolic', Gtk.IconSize.DIALOG)
            image.show()
            name = button.get_name()
            if name == "night_button":
                desktop.set_value("path-to-night-wallpaper", wallpaper)
                #add thumbnail
                
                self.night_wallpaper_image_box.pack_start(image, True, True, 2)
                
                current_time = datetime.datetime.now()
                if (current_time.hour >= desktop.get_value("nighttime")):
                    desktop.set_wallpapers(wallpaper)
            elif name == "day_button":
                desktop.set_value("path-to-day-wallpaper", wallpaper)
                #add thumbnail
                
                self.day_wallpaper_image_box.pack_start(image, True, True, 2)
                
                current_time = datetime.datetime.now()
                if (current_time.hour <= desktop.get_value("daytime")):
                    desktop.set_wallpapers(wallpaper)
        dialog.destroy()
        
    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Pictures")
        filter_text.add_mime_type("image/jpeg")
        filter_text.add_mime_type("image/png")
        dialog.add_filter(filter_text)
        
    def set_values_from_settings(self):
        self._day_minutes_spin_button.set_value(desktop.get_value("daytime-minutes"))
        self._night_hour_spin_button.set_value(desktop.get_value("nighttime-hour"))
        self._night_minutes_spin_button.set_value(desktop.get_value("nighttime-minutes"))
        self._day_hour_spin_button.set_value(desktop.get_value("daytime-hour"))
        
    def on_combo_box_changed(self):
        current_time = datetime.datetime.now()
        values = self.get_values()
        
        #find better solution
        current_values = convert_to_values(current_time.hour, int(str(current_time.minute)[:-1]+'0'))
        
        day_values = convert_to_values(values[0], values[1])
        night_values = convert_to_values(values[2], values[3])
        
        if ((current_values <= day_values or current_values >= night_values)):
            desktop.set_current_theme(self.cur_dark_theme)
        else:
            desktop.set_current_theme(self.cur_light_theme)
    
    def get_values(self):
        day_hour_values = desktop.get_value("daytime-hour")
        day_minutes_values = desktop.get_value("daytime-minutes")
        night_hour_values = desktop.get_value("nighttime-hour")
        night_minutes_values = desktop.get_value("nighttime-minutes")
        return day_hour_values, day_minutes_values, night_hour_values, night_minutes_values

