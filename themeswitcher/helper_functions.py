import itertools
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

#helper functions
    
def init_de():
    if os.environ['XDG_CURRENT_DESKTOP'] == 'GNOME':
        from .gnome import Gnome
        desktop = Gnome()
    
    return desktop
    
def convert_to_values(i, j):
    first_value = i * 60
    return first_value + j
    
    
