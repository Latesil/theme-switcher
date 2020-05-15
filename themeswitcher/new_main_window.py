import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GdkPixbuf, GLib
from Themeswitcher.helper_functions import Helper, init_de
from Themeswitcher.theme_switcher_constants import theme_switcher_constants as constants
from locale import gettext as _
import os
import datetime
import time
import subprocess

helper = Helper()

#get current DE
current_desktop = init_de()

#get list of installed themes
themes = sorted(current_desktop._get_valid_themes())

#get list of terminal profiles
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
    _light_tree_model = Gtk.Template.Child()
    _dark_tree_model = Gtk.Template.Child()
    day_terminal_combo = Gtk.Template.Child()
    night_terminal_combo = Gtk.Template.Child()
    terminal_checkbox = Gtk.Template.Child()
    day_terminal_main_frame = Gtk.Template.Child()
    night_terminal_main_frame = Gtk.Template.Child()
    day_wallpaper_event_box = Gtk.Template.Child()
    night_wallpaper_event_box = Gtk.Template.Child()
    day_wallpapers_frame = Gtk.Template.Child()
    night_wallpapers_frame = Gtk.Template.Child()
    no_day_wallpapers_label = Gtk.Template.Child()
    no_night_wallpapers_label = Gtk.Template.Child()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        #retrieve current theme and dark\light themes from desktop
        self.current_theme = current_desktop.get_current_theme()
        self.cur_light_theme, self.cur_dark_theme = current_desktop.get_current_themes()
        
        #set one callback for two buttons
        self._day_button.connect("clicked", self.wallpaper_button_clicked)
        self._night_button.connect("clicked", self.wallpaper_button_clicked)
        
        #frames are visible if auto-switch is on
        self.night_time_main_frame.set_visible(current_desktop.get_value("auto-switch"))
        self.day_time_main_frame.set_visible(current_desktop.get_value("auto-switch"))
        
        #retrieve wallpapers from settings if they exist
        self.current_day_wallpaper = current_desktop.get_value("path-to-day-wallpaper")
        self.current_night_wallpaper = current_desktop.get_value("path-to-night-wallpaper")
        
        #set checkbox on true if there is a terminal boolean in settings
        self.terminal_checkbox.set_active(current_desktop.get_value("terminal"))
        
        #populate terminal profiles 
        self.populate_terminal_profiles()
        
        #show current terminal profile as a default in combobox
        self.day_terminal_combo.set_active_id(current_desktop.get_value("active-day-profile-terminal"))
        self.night_terminal_combo.set_active_id(current_desktop.get_value("active-night-profile-terminal"))
        
        #retrieve current light\dark theme and set it as a default option in combo box
        self.retrieve_profile(self.day_terminal_combo, "active-day-profile-terminal")
        self.retrieve_profile(self.night_terminal_combo, "active-night-profile-terminal")
        
        #if there is some path in wallpapers set it to the box
        if self.current_day_wallpaper != "":
            self.day_wallpapers_frame.props.visible = True
            self.no_day_wallpapers_label.props.visible = False
            helper.set_wallpaper_to_box(self.day_wallpaper_event_box, self.current_day_wallpaper)
            
        if self.current_night_wallpaper != "":
            self.night_wallpapers_frame.props.visible = True
            self.no_night_wallpapers_label.props.visible = False
            helper.set_wallpaper_to_box(self.night_wallpaper_event_box, self.current_night_wallpaper)
        
        #populate theme list
        for i in themes:
            self._light_tree_model.append([i])
            self._dark_tree_model.append([i])

        #retrieve current light\dark theme and set it as a default option in combo box
        self.retrieve_theme(self._light_combo_box, self._light_tree_model, self.cur_light_theme)
        self.retrieve_theme(self._dark_combo_box, self._dark_tree_model, self.cur_dark_theme)
        
        #init light box
        self.init_box(self._light_combo_box)

        #init dark box
        self.init_box(self._dark_combo_box)
        
        #set values from settings when program is started
        self.set_values_from_settings()
        
        #this is probably not a best solution but for now it check time on start according to time section
        #and change what is needed (and only if auto is on)
        is_auto = current_desktop.get_value("auto-switch")
        if is_auto:
            self.on_combo_box_changed()

    #left switch in header bar. 
    #triggers when switch is clicked
    @Gtk.Template.Callback()
    def on__left_switch_state_set(self, widget, state):
        #set value to the settings
        current_desktop.set_value("auto-switch", state)
        
        #set visibillity of time section, is switch is set to true
        if state:
            self.night_time_main_frame.set_visible(True)
            self.day_time_main_frame.set_visible(True)
            
            #set systemd timers. maybe it shouldn't stick with systemd but for now it is
            current_desktop.start_systemd_timers()
            
            #check if niw is the right time for change:
            if self.time_for_night():
                self.trigger_all("night")
            else:
                self.trigger_all("day")
        else:
            self.night_time_main_frame.set_visible(False)
            self.day_time_main_frame.set_visible(False)
            current_desktop.stop_systemd_timers()
            
            #resize the main window to prevent empty space on the bottom
            helper.resize_window(self)
            
    #same as upper switch but it works for the terminal section
    @Gtk.Template.Callback()
    def on_terminal_checkbox_toggled(self, checkbox):
        if checkbox.get_active():
            self.day_terminal_main_frame.set_visible(True)
            self.night_terminal_main_frame.set_visible(True)
            current_desktop.set_value("terminal", True)
        else:
            self.day_terminal_main_frame.set_visible(False)
            self.night_terminal_main_frame.set_visible(False)
            current_desktop.set_value("terminal", False)
            
            #resize the main window to prevent empty space on the bottom
            helper.resize_window(self)
            
    ###################################################################################
        
    # 4 functions tracking changes in time section in night\day hours\minutes
    # and triggers theme changes if needed calling self.on_combo_box_changed() function 
    
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
        
    #####################################################################################
        
    #callback for change theme now
    @Gtk.Template.Callback()
    def on__change_theme_button_clicked(self, button):
        try:
            current_desktop.execute_script('/usr/bin/theme-switcher-manual.py')
        except:
            pass
            
    #####################################################################################

    # reset functions for reset parts of values in the program or all parameters 

    @Gtk.Template.Callback()
    def on__reset_time_button_clicked(self, button):
        current_desktop.reset_value("nighttime-minutes")
        current_desktop.reset_value("daytime-minutes")
        current_desktop.reset_value("nighttime-hour")
        current_desktop.reset_value("daytime-hour")
        current_desktop.reset_value("auto-switch")
        self._left_switch.set_state(False)
        self.set_value_from_settings(self._night_minutes_spin_button, "nighttime-minutes")
        self.set_value_from_settings(self._day_minutes_spin_button, "daytime-minutes")
        self.set_value_from_settings(self._night_hour_spin_button, "nighttime-hour")
        self.set_value_from_settings(self._day_hour_spin_button, "daytime-hour")

    @Gtk.Template.Callback()
    def on__reset_themes_clicked(self, button):
        current_desktop.reset_value("light-theme")
        current_desktop.reset_value("dark-theme")
        self.retrieve_theme(self._light_combo_box, self._light_tree_model, self.cur_light_theme, True, "light")
        self.retrieve_theme(self._dark_combo_box, self._dark_tree_model, self.cur_dark_theme, True, "dark")

    @Gtk.Template.Callback()
    def on__reset_wallpapers_clicked(self, button):
        current_desktop.reset_value("path-to-night-wallpaper")
        current_desktop.reset_value("path-to-day-wallpaper")
        self.day_wallpapers_frame.props.visible = False
        self.no_day_wallpapers_label.props.visible = True
        helper.reset_box(self.night_wallpaper_event_box)
        helper.reset_box(self.day_wallpaper_event_box)
        helper.resize_window(self)

    @Gtk.Template.Callback()
    def on__reset_all_button_clicked(self, button):
        self.on__reset_time_button_clicked(button)
        self.on__reset_wallpapers_clicked(button)
        self.on__reset_themes_clicked(button)
        current_desktop.reset_value("terminal")
        current_desktop.reset_value("active-day-profile-terminal")
        current_desktop.reset_value("active-night-profile-terminal")
        self.day_terminal_combo.set_active_id(None)
        self.night_terminal_combo.set_active_id(None)
        self.terminal_checkbox.set_active(False)
        
    #######################################################################################

    # about dialog
    @Gtk.Template.Callback()
    def on__about_button_clicked(self, button):
        about = Gtk.AboutDialog()
        about.set_program_name(_("Theme Switcher"))
        about.set_version("2.0.2")
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
    
    #######################################################################################
        
    # first it checks what widget triggered by user. It looks at the name of the widget
    # and behave accordingly. If auto-switch is on and time is fit to change it try to set a new
    # terminal profile. BTW it cannot do it instantly. Instead you should reopen any existing terminals.
    
    @Gtk.Template.Callback()
    def on_terminal_combo_changed(self, combobox):
        if combobox.props.name == "night_terminal_combobox":
            current_desktop.set_value("active-night-profile-terminal", combobox.get_active_text())
            is_auto = current_desktop.get_value("auto-switch")
            if is_auto:
                if self.time_for_night():
                    current_desktop.set_terminal_profile(current_desktop.get_value("active-night-profile-terminal"))
        elif combobox.props.name == "day_terminal_combobox":
            current_desktop.set_value("active-day-profile-terminal", combobox.get_active_text())
            is_auto = current_desktop.get_value("auto-switch")
            if is_auto:
                if self.time_for_day():
                    current_desktop.set_terminal_profile(current_desktop.get_value("active-day-profile-terminal"))
        
    ######################################################################
    
    # list of helpers functions that can be triggered by callbacks
    
    # set model in comboboxes according to settings
    # it can retrieve default value from settings or value that is set by user
    
    def retrieve_theme(self, box, model, current_theme, default=False, theme=None):
        # get model from the box (we populate them in init function, after a populate theme list from the system)
        model = box.get_model()
        for row in model:
            #if we want to set default value
            if default:
                #if we want to set a default dark theme
                if theme == "dark":
                    #check all themes until we find default adwaita-dark theme, set it in the combobox and return
                    if row[0] == "Adwaita-dark":
                        box.set_active_iter(row.iter)
                        return
                        
                #if we want to set a default light theme
                elif theme == "light":
                    #check all themes until we find default adwaita theme, set it in the combobox and return
                    if row[0] == "Adwaita":
                        box.set_active_iter(row.iter)
                        return
                        
            #we want to set non-default theme (save current theme to the combobox)
            else:
                #check all themes until we find current theme, set it to the combobox and return
                # theme variable here is equal to None (default value), so we dont have to add it to the function calling
                # if we need to set current theme.
                if row[0] == current_theme:
                    box.set_active_iter(row.iter)
                    
    #-----------------------------------------------------------------------------------------------------------
    
    # init light or dark box (from init function)
    def init_box(self, box):
        #connect it to the changed event
        box.connect("changed", self.combo_box_changed)
        renderer_text = Gtk.CellRendererText()
        
        #add model with text
        box.pack_start(renderer_text, True)
        box.add_attribute(renderer_text, "text", 0)
    
    # triggers when combobox receive changed event
                
    def combo_box_changed(self, combo):
        #get active item in triggered combobox 
        tree_iter = combo.get_active_iter()
        
        #if this is not none
        if tree_iter is not None:
            model = combo.get_model()
            combo.set_active_iter(tree_iter)
            
            #retrieve theme from the model
            theme = model[tree_iter][0]

            #if we touch light box
            if combo.props.name == 'light_box':
                #set values to the settings
                current_desktop.set_value('light-theme', theme)
                is_auto = current_desktop.get_value("auto-switch")
                #check if auto is on
                if is_auto:
                    if self.time_for_day():
                        #set selected theme in the combobox as a day theme
                        current_desktop.set_current_theme(theme)

            #same as light before
            if combo.props.name == 'dark_box':
                current_desktop.set_value('dark-theme', theme)
                is_auto = current_desktop.get_value("auto-switch")
                if is_auto:
                    if self.time_for_night():
                        current_desktop.set_current_theme(theme)
                        
    #-----------------------------------------------------------------------------------------
    
    # triggers when user click on wallpaper button. Behaviour depends on the widget name
    
    def wallpaper_button_clicked(self, button):
        #create gtk.dialog window
        dialog = Gtk.FileChooserDialog(_("Choose a file"), None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        # ...with filters, for only pictures to show
        self.add_filters(dialog)
        response = dialog.run()
        
        #if user click ok
        if response == Gtk.ResponseType.OK:
            #get file path and create image with it
            wallpaper = dialog.get_filename()
            image = Gtk.Image()
            try:
                #fixed size for now
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(wallpaper, 114, 64, True)
                image.set_from_pixbuf(pixbuf)
                
            except Exception:
                print('Error occured')
                image.set_from_icon_name('dialog-error-symbolic', Gtk.IconSize.DIALOG)
            image.show()
            
            if button.props.name == "night_button":
                #set value in settings
                current_desktop.set_value("path-to-night-wallpaper", wallpaper)
                if self.night_wallpaper_event_box.get_children():
                    helper.remove_wallpaper_from_box(self.night_wallpaper_event_box)
                
                #add image in our box
                self.night_wallpaper_event_box.add(image)
                self.night_wallpapers_frame.props.visible = True
                self.no_night_wallpapers_label.props.visible = False
                is_auto = current_desktop.get_value("auto-switch")
                #check if auto is on
                if is_auto:
                    if self.time_for_night():
                        current_desktop.set_wallpapers(wallpaper)
                        
            elif button.props.name == "day_button":
                current_desktop.set_value("path-to-day-wallpaper", wallpaper)
                if self.day_wallpaper_event_box.get_children():
                    helper.remove_wallpaper_from_box(self.day_wallpaper_event_box)
                    
                self.day_wallpaper_event_box.add(image)
                self.day_wallpapers_frame.props.visible = True
                self.no_day_wallpapers_label.props.visible = False
                is_auto = current_desktop.get_value("auto-switch")
                if is_auto:
                    if self.time_for_day():
                        current_desktop.set_wallpapers(wallpaper)
        dialog.destroy()
    
    #--------------------------------------------------------------------------------------
    
    #add filters, for pictures only       
    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Pictures")
        filter_text.add_mime_type("image/jpeg")
        filter_text.add_mime_type("image/png")
        dialog.add_filter(filter_text)
        
    #triggers when program starts. Get all values from settings and set it in the app
    def set_values_from_settings(self):
        self._day_minutes_spin_button.set_value(current_desktop.get_value("daytime-minutes"))
        self._night_hour_spin_button.set_value(current_desktop.get_value("nighttime-hour"))
        self._night_minutes_spin_button.set_value(current_desktop.get_value("nighttime-minutes"))
        self._day_hour_spin_button.set_value(current_desktop.get_value("daytime-hour"))
        
        #state
        self._left_switch.set_state(current_desktop.get_value("auto-switch"))
        
    #one function for setting abstract value from settings
    def set_value_from_settings(self, widget, key):
        widget.set_value(current_desktop.get_value(key))
        
    # triggers when program starts or value in time section is changed
    def on_combo_box_changed(self):
        is_auto = current_desktop.get_value("auto-switch")
        if is_auto:
            if self.time_for_night():
                self.trigger_all("night")
            else:
                self.trigger_all("day")
    
    #get time values from settings
    def get_time(self):
        day_hour = current_desktop.get_value("daytime-hour")
        day_minutes = current_desktop.get_value("daytime-minutes")
        night_hour = current_desktop.get_value("nighttime-hour")
        night_minutes = current_desktop.get_value("nighttime-minutes")
        return day_hour, day_minutes, night_hour, night_minutes
        
    def populate_terminal_profiles(self):
        for profile in terminal_profiles:
            self.day_terminal_combo.append_text(profile)
            self.night_terminal_combo.append_text(profile)
                
    def retrieve_profile(self, box, key):
        profile = box.get_model()
        for row in profile:
            if row[0] == current_desktop.get_value(key):
                box.set_active_iter(row.iter)
                
    #change everything according to day\night time
    def trigger_all(self, time):
        is_terminal = current_desktop.get_value("terminal")
        
        #check if wallpapers exists (they may be changed since init so we get it one more time)
        self.current_day_wallpaper = current_desktop.get_value("path-to-day-wallpaper")
        self.current_night_wallpaper = current_desktop.get_value("path-to-night-wallpaper")
        
        if time == "night":
            current_desktop.set_current_theme(self.cur_dark_theme)
            if is_terminal:
                current_desktop.set_terminal_profile(current_desktop.get_value("active-night-profile-terminal"))
            if self.current_day_wallpaper != "":
                current_desktop.set_wallpapers(current_desktop.get_value("path-to-night-wallpaper"))
        else:
            current_desktop.set_current_theme(self.cur_light_theme)
            if is_terminal:
                current_desktop.set_terminal_profile(current_desktop.get_value("active-day-profile-terminal"))
            if self.current_day_wallpaper != "":
                current_desktop.set_wallpapers(current_desktop.get_value("path-to-day-wallpaper"))
    
    #retrieve current values and
    #returns True if current value is fit for a daytime
    def time_for_day(self):
        current, day, night = self.get_values_list()
        return current >= day and current < night
        
    #retrieve current values and
    #returns True if current value is fit for a nighttime
    def time_for_night(self):
        current, day, night = self.get_values_list()
        return current <= day or current >= night
            
    #get values (10th of minutes)
    #returns tuple like this:
    # 0 - Current Values
    # 1 - Day values
    # 2 - Night values
    def get_values_list(self):
        #this is a list of time values [day_hours, day_minutes, night_hours, nught_minutes])
        values = self.get_time()
        current_time = datetime.datetime.now()
        
        # convert hours to internal values (function convert to values in the helpers file)
        # values is an amount of minutes rounded by 10, for example if current time if 00:20 then
        # current values equals to 20. If Night time is set to 20:00 it is equals to 1200 values (because 60 * 20 = 1200)
        # 570 values is equal 09:30 because 6*9 = 540, and + 30 minutes = 570.
        current_values = helper.convert_to_values(current_time.hour, current_time.minute)
        
        day_values = helper.convert_to_values(values[0], values[1])
        night_values = helper.convert_to_values(values[2], values[3])
        return current_values, day_values, night_values
