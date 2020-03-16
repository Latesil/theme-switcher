from abc import ABC, abstractmethod

class Desktop(ABC):
    
    def __init__(self):
        print('init')
        
    @abstractmethod
    def init_settings(self):
        print('init settings')
        
    @abstractmethod
    def get_init_settings(self):
        print('get_init settings')
        
    @abstractmethod
    def connect_wallpapers(self):
        print('connect wallpapers')
        
    @abstractmethod
    def connect_daytime(self):
        print('connect_daytime')
        
    @abstractmethod
    def connect_nighttime(self):
        print('connect_nighttime')
        
    @abstractmethod
    def connect_time_visible(self):
        print('connect_time_visible')
        
    @abstractmethod
    def connect_autoswitch(self):
        print('connect_autoswitch')
        
    @abstractmethod
    def set_wallpapers(self):
        print('set wallpapers')
        
    @abstractmethod
    def start_systemd_timers(self):
        print('start_systemd_timers')
        
    @abstractmethod
    def stop_systemd_timers(self):
        print('stop_systemd_timers')
        
    @abstractmethod
    def get_current_theme(self):
        print('get current theme')
        
    @abstractmethod
    def set_current_theme(self):
        print('set current theme')
