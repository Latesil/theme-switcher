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
        
    def on_day_entry_changed(self, button):
        entry_text = self.day_entry.get_text()
        
        if entry_text == '' or entry_text == None:
            entry_text = "0"
            
        if int(entry_text) > 23:
            self.day_entry.set_text("23")
            entry_text = self.day_entry.get_text()
        #TODO add check that night bigger than day
        else:
            self.settings.set_string("daytime", str(entry_text))
        
    def on_night_entry_changed(self, button):
        entry_text = self.night_entry.get_text()
        
        if entry_text == '' or entry_text == None:
            entry_text = "0"
            
        if int(entry_text) > 23:
            self.night_entry.set_text("23")
            entry_text = self.night_entry.get_text()
        #TODO add check that night bigger than day
        else:
            self.settings.set_string("nighttime", str(entry_text))
                
    def on_auto_toggled(self, auto_button, gparam):
        if self.auto_button.get_active():
            state = "on"
            self.state_on()
        else:
            state = "off"
            self.state_off()
            
    def on_auto_switch_change(self, settings, key, auto_button):
        self.auto_button.set_active(settings.get_boolean("auto-switch"))
        
    def reset(self, button):
        
        #maybe there is another way to reset?
        self.settings.set_string("nighttime", "20")
        self.settings.set_string("daytime", "6")
        self.settings.set_string("path-to-night-wallpaper", "")
        self.settings.set_string("path-to-day-wallpaper", "")
        self.settings.set_boolean("auto-switch", True)
        self.day_entry.set_text(self.settings.get_string("daytime"))
        self.night_entry.set_text(self.settings.get_string("nighttime"))
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
        
        reset_button = Gtk.Button(label="Reset")
        reset_button.connect("clicked", self.reset)
        self.header_bar.pack_end(reset_button)
        
    def init_upper_grid(self):
        self.upper_grid = Gtk.Grid()
        self.upper_grid.set_column_homogeneous(True)
        self.upper_grid.set_row_homogeneous(True)
        
        label_day = Gtk.Label("File for day:")
        self.upper_grid.add(label_day)
        
        self.file_button_day = Gtk.Button("Choose Day Wallpaper")
        self.file_button_day.set_margin_right(10)
        self.file_button_day.connect("clicked", self.on_day_wallpaper_choose)
        self.upper_grid.attach_next_to(self.file_button_day, label_day, Gtk.PositionType.BOTTOM, 1, 1)
        
        label_night = Gtk.Label("File for night:")
        self.upper_grid.attach_next_to(label_night, label_day, Gtk.PositionType.RIGHT, 1, 1)
        
        self.file_button_night = Gtk.Button("Choose Night Wallpaper")
        self.file_button_night.connect("clicked", self.on_night_wallpaper_choose)
        self.upper_grid.attach_next_to(self.file_button_night, label_night, Gtk.PositionType.BOTTOM, 1, 1)
        
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
        daytime_box.add(day_label)
        
        self.day_entry = Gtk.Entry()
        self.day_entry.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.day_entry.set_text(self.settings.get_string("daytime"))
        self.day_entry.connect("changed", self.on_day_entry_changed)
        daytime_box.add(self.day_entry)
        
        nighttime_box = Gtk.Box()
        nighttime_box.set_homogeneous(True)
        nighttime_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        night_label = Gtk.Label("Night: ")
        nighttime_box.add(night_label)
        
        self.night_entry = Gtk.Entry()
        self.night_entry.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.night_entry.set_text(self.settings.get_string("nighttime"))
        self.night_entry.connect("changed", self.on_night_entry_changed)
        nighttime_box.add(self.night_entry)
        
        self.bottom_grid.attach_next_to(daytime_box, time_label, Gtk.PositionType.BOTTOM, 1, 1)
        self.bottom_grid.attach_next_to(nighttime_box, daytime_box, Gtk.PositionType.BOTTOM, 1, 1)
