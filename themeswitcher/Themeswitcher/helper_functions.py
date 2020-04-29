import itertools
import os

#helper functions
    
def init_de():
    if os.environ['XDG_CURRENT_DESKTOP'] == 'GNOME':
        from .gnome import Gnome
        desktop = Gnome()
    
    return desktop
    
def convert_to_values(i, j):
    # values is an amount of minutes rounded by 10
    # first value is an amount of hours and we multiply it to the 60 (minutes)
    # for calculate amount of minutes. And second parameter
    # is an amount of minutes divided by 10 (for example 10, 20, 30, 40 and not 34, 56, 22)
    # (33 became 30, 56 became 50 etc)
    # returns amount of abstract values (equals to minutes divided by 10)
    first_value = i * 60
    return first_value + j
    
    
