import gi
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class MyWindow(Gtk.ApplicationWindow):

    BASE_KEY = "org.theme-switcher"

    def __init__(self):
    
        Gtk.Window.__init__(self, title="Theme Switcher")
        
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
        
    def state_off(self):
        self.settings.set_boolean("auto-switch", self.auto_button.get_active())
        subprocess.call(['systemctl','stop','--user','theme-switcher-auto.timer'])
        subprocess.call(['systemctl','disable','--user','theme-switcher-auto.timer'])
        
    def state_on(self):
        self.settings.set_boolean("auto-switch", self.auto_button.get_active())
        subprocess.call(['systemctl','start','--user','theme-switcher-auto.timer'])
        subprocess.call(['systemctl','enable','--user','theme-switcher-auto.timer'])
        
    def on_day_wallpaper_choose(self, widget):
        dialog = Gtk.FileChooserDialog("Choose a file", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        self.add_filters(dialog)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            day_wallpaper = dialog.get_filename()
            self.settings.set_string("path-to-day-wallpaper", day_wallpaper)
            self.file_button_day.set_label(day_wallpaper.split("/")[-1])
        dialog.destroy()
        
    def on_night_wallpaper_choose(self, widget):
        dialog = Gtk.FileChooserDialog("Choose a file", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        self.add_filters(dialog)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            night_wallpaper = dialog.get_filename()
            self.settings.set_string("path-to-night-wallpaper", night_wallpaper)
            self.file_button_night.set_label(night_wallpaper.split("/")[-1])
            
        dialog.destroy()
            
    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("image/jpeg")
        filter_text.add_mime_type("image/png")
        dialog.add_filter(filter_text)
                
    def on_auto_toggled(self, auto_button, gparam):
        if self.auto_button.get_active():
            state = "on"
            self.state_on()
        else:
            state = "off"
            self.state_off()
            
    def on_auto_switch_change(self, settings, key, auto_button):
        self.auto_button.set_active(settings.get_boolean("auto-switch"))
        
    def on_main_button_clicked(self, button):
        self.popover.set_relative_to(button)
        self.popover.show_all()
        self.popover.popup()
        
    def on_reset_wallpapers(self, button):
        self.settings.set_string("path-to-night-wallpaper", "")
        self.settings.set_string("path-to-day-wallpaper", "")
        self.file_button_night.set_label("Choose Night Wallpaper")
        self.file_button_day.set_label("Choose Day Wallpaper")
        
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
        self.file_button_night.set_label("Choose Night Wallpaper")
        self.file_button_day.set_label("Choose Day Wallpaper")
        
    def init_headerbar(self):
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = "Theme Switcher"
        
        header_box = Gtk.Box(spacing=6)
        header_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        
        header_label = Gtk.Label("Auto:")
        header_box.add(header_label)
        
        self.auto_button = Gtk.Switch()
        
        self.settings = Gio.Settings.new(self.BASE_KEY)
        self.settings.connect("changed::auto-switch", self.on_auto_switch_change, self.auto_button)
        
        self.auto_button.set_active(self.settings.get_boolean("auto-switch"))
        self.auto_button.connect("notify::active", self.on_auto_toggled)
        header_box.add(self.auto_button)
        
        self.header_bar.pack_start(header_box)
        
        reset_button = Gtk.ModelButton(label="Reset all")
        reset_button.centered = False
        reset_button.connect("clicked", self.reset)
        
        reset_wallpapers_button = Gtk.ModelButton(label="Reset Wallpapers")
        reset_wallpapers_button.connect("clicked", self.on_reset_wallpapers)
        
        reset_time_button = Gtk.ModelButton(label="Reset Time")
        reset_time_button.connect("clicked", self.reset_time)
        
        main_button = Gtk.Button.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.BUTTON)
        self.popover = Gtk.Popover()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.set_margin_left(10)
        vbox.set_margin_right(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_top(10)
        vbox.pack_start(reset_button, False, False, 0)
        vbox.pack_start(reset_time_button, False, False, 0)
        vbox.pack_start(reset_wallpapers_button, False, False, 0)
        self.popover.add(vbox)
        self.popover.set_position(Gtk.PositionType.BOTTOM)
        main_button.connect("clicked", self.on_main_button_clicked)
        self.header_bar.pack_end(main_button)
        
    def init_upper_grid(self):
        self.upper_grid = Gtk.Grid()
        self.upper_grid.set_column_homogeneous(True)
        self.upper_grid.set_row_homogeneous(True)
        
        label_day = Gtk.Label("File for day:")
        label_day.set_halign(Gtk.Align.START)
        self.upper_grid.add(label_day)
        
        self.file_button_day = Gtk.Button()
        if not self.settings.get_string("path-to-day-wallpaper"):
            self.file_button_day.set_label("Choose Day Wallpaper")
        else:
            day_wallpaper = self.settings.get_string("path-to-day-wallpaper")
            self.file_button_day.set_label(day_wallpaper.split("/")[-1])
        self.file_button_day.set_margin_right(10)
        self.file_button_day.connect("clicked", self.on_day_wallpaper_choose)
        self.upper_grid.attach_next_to(self.file_button_day, label_day, Gtk.PositionType.BOTTOM, 1, 1)
        
        label_night = Gtk.Label("File for night:")
        label_night.set_halign(Gtk.Align.START)
        self.upper_grid.attach_next_to(label_night, label_day, Gtk.PositionType.RIGHT, 1, 1)
        
        self.file_button_night = Gtk.Button()
        if not self.settings.get_string("path-to-night-wallpaper"):
            self.file_button_night.set_label("Choose Night Wallpaper")
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
        
        time_label = Gtk.Label("Time Manage:")
        self.bottom_grid.add(time_label)
        
        daytime_box = Gtk.Box()
        daytime_box.set_homogeneous(True)
        daytime_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        day_label = Gtk.Label("Daytime: ")
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
        night_label = Gtk.Label("Night: ")
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
