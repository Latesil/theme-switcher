import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GdkPixbuf
from Themeswitcher.helper_functions import init_de, convert_to_values
from Themeswitcher.theme_switcher_constants import theme_switcher_constants as constants
from locale import gettext as _
import os
import datetime
import subprocess

current_desktop = init_de()
themes = sorted(current_desktop._get_valid_themes())
terminal_profiles = current_desktop.get_terminal_profiles()

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
    day_terminal_combo = Gtk.Template.Child()
    night_terminal_combo = Gtk.Template.Child()
    terminal_checkbox = Gtk.Template.Child()
    day_terminal_main_frame = Gtk.Template.Child()
    night_terminal_main_frame = Gtk.Template.Child()
    
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, title=_("Theme Switcher"), application=app)

        self.set_wmclass("Theme Switcher", _("Theme Switcher"))
        
        self.current_theme = current_desktop.get_current_theme()
        self.cur_light_theme, self.cur_dark_theme = current_desktop.get_current_themes()
        self._light_combo_box.set_name("light_box")
        self._dark_combo_box.set_name("dark_box")
        
        self._day_button.set_name("day_button")
        self._night_button.set_name("night_button")
        self._day_button.connect("clicked", self.wallpaper_button_clicked)
        self._night_button.connect("clicked", self.wallpaper_button_clicked)
        
        self.night_time_main_frame.set_visible(current_desktop.get_value("auto-switch"))
        self.day_time_main_frame.set_visible(current_desktop.get_value("auto-switch"))
        
        self.current_day_wallpaper = current_desktop.get_value("path-to-day-wallpaper")
        self.current_night_wallpaper = current_desktop.get_value("path-to-night-wallpaper")
        
        self.terminal_checkbox.set_active(current_desktop.get_value("terminal"))
        self.populate_terminal_profiles()
        
        self.day_terminal_combo.set_active_id(current_desktop.get_value("active-day-profile-terminal"))
        self.night_terminal_combo.set_active_id(current_desktop.get_value("active-night-profile-terminal"))
        
        #retrieve current light\dark theme and set it as a default option in combo box
        self.retrieve_day_profile(self.day_terminal_combo)
        self.retrieve_night_profile(self.night_terminal_combo)
        
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
        current_desktop.set_value("auto-switch", state)
        
        if state:
            self.night_time_main_frame.set_visible(True)
            self.day_time_main_frame.set_visible(True)
            current_desktop.start_systemd_timers()
        else:
            self.night_time_main_frame.set_visible(False)
            self.day_time_main_frame.set_visible(False)
            current_desktop.stop_systemd_timers()
            self.resize_window()
            
    @Gtk.Template.Callback()
    def on_terminal_checkbox_toggled(self, checkbox):
        if checkbox.get_active():
            self.day_terminal_main_frame.set_visible(True)
            self.night_terminal_main_frame.set_visible(True)
            current_desktop.set_value("terminal", True)
            self.day_terminal_combo.set_active_id(current_desktop.get_value("active-day-profile-terminal"))
            self.night_terminal_combo.set_active_id(current_desktop.get_value("active-night-profile-terminal"))
        else:
            self.day_terminal_main_frame.set_visible(False)
            self.night_terminal_main_frame.set_visible(False)
            current_desktop.set_value("terminal", False)
            self.resize_window()
        
    @Gtk.Template.Callback()
    def on__day_hour_adjustment_value_changed(self, scale):
        current_desktop.set_value("daytime-hour", scale.get_value())
        self.on_combo_box_changed()
        
    @Gtk.Template.Callback()
    def on__day_minutes_adjustment_value_changed(self, scale):
        current_desktop.set_value("daytime-minutes", scale.get_value())
        self.on_combo_box_changed()
        
    @Gtk.Template.Callback()
    def on__night_minutes_adjustment_value_changed(self, scale):
        current_desktop.set_value("nighttime-minutes", scale.get_value())
        self.on_combo_box_changed()
    
    @Gtk.Template.Callback()
    def on__night_hour_adjustment_value_changed(self, scale):
        current_desktop.set_value("nighttime-hour", scale.get_value())
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
        current_desktop.reset_value("nighttime-minutes")
        current_desktop.reset_value("daytime-minutes")
        current_desktop.reset_value("nighttime-hour")
        current_desktop.reset_value("daytime-hour")
        self.set_value_from_settings(self._night_minutes_spin_button, "nighttime-minutes")
        self.set_value_from_settings(self._day_minutes_spin_button, "daytime-minutes")
        self.set_value_from_settings(self._night_hour_spin_button, "nighttime-hour")
        self.set_value_from_settings(self._day_hour_spin_button, "daytime-hour")

    @Gtk.Template.Callback()
    def on__reset_themes_clicked(self, button):
        current_desktop.reset_value("light-theme")
        current_desktop.reset_value("dark-theme")
        self.retrieve_light_default_theme(self._light_combo_box)
        self.retrieve_dark_default_theme(self._dark_combo_box)

    @Gtk.Template.Callback()
    def on__reset_wallpapers_clicked(self, button):
        current_desktop.reset_value("path-to-night-wallpaper")
        current_desktop.reset_value("path-to-day-wallpaper")
        
        if len(self.night_wallpaper_image_box) > 0:
            element = self.night_wallpaper_image_box.get_children()[0]
            self.night_wallpaper_image_box.remove(element)
            
        if len(self.day_wallpaper_image_box) > 0:
            element = self.day_wallpaper_image_box.get_children()[0]
            self.day_wallpaper_image_box.remove(element)

    @Gtk.Template.Callback()
    def on__reset_all_button_clicked(self, button):
        self.on__reset_time_button_clicked(button)
        self.on__reset_wallpapers_clicked(button)
        self.on__reset_themes_clicked(button)
        current_desktop.reset_value("auto-switch")
        current_desktop.reset_value("terminal")
        current_desktop.reset_value("active-day-profile-terminal")
        current_desktop.reset_value("active-night-profile-terminal")
        self.day_terminal_combo.set_active_id(None)
        self.night_terminal_combo.set_active_id(None)
        self.terminal_checkbox.set_active(False)

    @Gtk.Template.Callback()
    def on__about_button_clicked(self, button):
        about = Gtk.AboutDialog()
        about.set_program_name(_("Theme Switcher"))
        about.set_version("1.9.1")
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
        
    @Gtk.Template.Callback()
    def on_terminal_combo_changed(self, combobox):
        if combobox.props.name == "night_terminal_combobox":
            current_desktop.set_value("active-night-profile-terminal", combobox.get_active_text())
            current_time = datetime.datetime.now()
            if (current_time.hour >= current_desktop.get_value("nighttime")):
                current_desktop.set_terminal_profile(current_desktop.get_value("active-night-profile-terminal"))
        elif combobox.props.name == "day_terminal_combobox":
            current_desktop.set_value("active-day-profile-terminal", combobox.get_active_text())
            current_time = datetime.datetime.now()
            if (current_time.hour <= current_desktop.get_value("daytime")):
                current_desktop.set_terminal_profile(current_desktop.get_value("active-day-profile-terminal"))
        
    ######################################################################
        
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
                
    def retrieve_light_default_theme(self, box):
        self._light_model = box.get_model()
        for row in self._light_model:
            if row[0] == "Adwaita":
                box.set_active_iter(row.iter)
                
    def retrieve_dark_default_theme(self, box):
        self._light_model = box.get_model()
        for row in self._light_model:
            if row[0] == "Adwaita-dark":
                box.set_active_iter(row.iter)
                
    def combo_box_changed(self, combo):
        name = combo.get_name()
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            combo.set_active_iter(tree_iter)
            theme = model[tree_iter][0]

            if name == 'light_box':
                current_desktop.set_value('light-theme', theme)
                current_time = datetime.datetime.now()
                if (current_time.hour <= current_desktop.get_value("daytime")):
                    current_desktop.set_current_theme(theme)

            if name == 'dark_box':
                current_desktop.set_value('dark-theme', theme)
                current_time = datetime.datetime.now()
                if (current_time.hour >= current_desktop.get_value("nighttime")):
                    current_desktop.set_current_theme(theme)
    
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
                current_desktop.set_value("path-to-night-wallpaper", wallpaper)
                #add thumbnail
                
                self.night_wallpaper_image_box.pack_start(image, True, True, 2)
                
                current_time = datetime.datetime.now()
                if (current_time.hour >= current_desktop.get_value("nighttime")):
                    current_desktop.set_wallpapers(wallpaper)
            elif name == "day_button":
                current_desktop.set_value("path-to-day-wallpaper", wallpaper)
                #add thumbnail
                
                self.day_wallpaper_image_box.pack_start(image, True, True, 2)
                
                current_time = datetime.datetime.now()
                if (current_time.hour <= current_desktop.get_value("daytime")):
                    current_desktop.set_wallpapers(wallpaper)
        dialog.destroy()
        
    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Pictures")
        filter_text.add_mime_type("image/jpeg")
        filter_text.add_mime_type("image/png")
        dialog.add_filter(filter_text)
        
    def set_values_from_settings(self):
        self._day_minutes_spin_button.set_value(current_desktop.get_value("daytime-minutes"))
        self._night_hour_spin_button.set_value(current_desktop.get_value("nighttime-hour"))
        self._night_minutes_spin_button.set_value(current_desktop.get_value("nighttime-minutes"))
        self._day_hour_spin_button.set_value(current_desktop.get_value("daytime-hour"))
        
        #state
        self._left_switch.set_state(current_desktop.get_value("auto-switch"))
        
    def set_value_from_settings(self, widget, key):
        widget.set_value(current_desktop.get_value(key))
        
    def on_combo_box_changed(self):
        current_time = datetime.datetime.now()
        values = self.get_values()
        
        #find better solution
        current_values = convert_to_values(current_time.hour, int(str(current_time.minute)[:-1]+'0'))
        
        day_values = convert_to_values(values[0], values[1])
        night_values = convert_to_values(values[2], values[3])
        
        if ((current_values <= day_values or current_values >= night_values)):
            current_desktop.set_current_theme(self.cur_dark_theme)
        else:
            current_desktop.set_current_theme(self.cur_light_theme)
    
    def get_values(self):
        day_hour_values = current_desktop.get_value("daytime-hour")
        day_minutes_values = current_desktop.get_value("daytime-minutes")
        night_hour_values = current_desktop.get_value("nighttime-hour")
        night_minutes_values = current_desktop.get_value("nighttime-minutes")
        return day_hour_values, day_minutes_values, night_hour_values, night_minutes_values
        
    def resize_window(self):
        self.resize(600, 100)
        
    def populate_terminal_profiles(self):
        for profile in terminal_profiles:
            self.day_terminal_combo.append_text(profile)
            self.night_terminal_combo.append_text(profile)
            
    def retrieve_day_profile(self, box):
        self.day_profile = box.get_model()
        for row in self.day_profile:
            if row[0] == current_desktop.get_value("active-day-profile-terminal"):
                box.set_active_iter(row.iter)
        
    def retrieve_night_profile(self, box):
        self.night_profile = box.get_model()
        for row in self.night_profile:
            if row[0] == current_desktop.get_value("active-night-profile-terminal"):
                box.set_active_iter(row.iter)


