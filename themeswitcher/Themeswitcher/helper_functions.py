import gi

gi.require_version('Gtk', '3.0')
import itertools
import os

from gi.repository import GdkPixbuf, Gtk


# helper functions
def init_de():
    if os.environ['XDG_CURRENT_DESKTOP'] == 'GNOME':
        from .gnome import Gnome
        desktop = Gnome()
    return desktop


# class for function without any mentions of the current_desktop 
class Helper:

    def convert_to_values(self, i, j):
        # values is an amount of minutes rounded by 10
        # first value is an amount of hours and we multiply it to the 60 (minutes)
        # for calculate amount of minutes. And second parameter
        # is an amount of minutes divided by 10 (for example 10, 20, 30, 40 and not 34, 56, 22)
        # (33 became 30, 56 became 50 etc)
        # returns amount of abstract values (equals to minutes divided by 10)
        j = j - j % 10
        first_value = i * 60
        return first_value + j

    # triggers in reset
    def reset_box(self, box):
        if len(box) > 0:
            element = box.get_children()[0]
            box.remove(element)

    def resize_window(self, win):
        win.resize(400, 100)

    # triggers in init
    def set_wallpaper_to_box(self, box, wallpaper):
        image = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(wallpaper, 114, 64, True)
        image.set_from_pixbuf(pixbuf)
        box.add(image)
        image.show()

    def remove_wallpaper_from_box(self, box):
        # only one child -> Gtk.Image
        child = box.get_children()[0]
        box.remove(child)
