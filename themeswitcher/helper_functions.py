import itertools
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

#helper functions
#taken from GNOME Tweaks
#by John Stowers.

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
    
def init_de():
    from .gnome import Gnome

    desktop = Gnome()
    desktop.init_settings()
    
    return desktop
    
def convert_to_values(i, j):
    first_value = i * 60
    return first_value + j
    
