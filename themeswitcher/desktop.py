from abc import ABC, abstractmethod

class Desktop(ABC):
        
    @abstractmethod
    def init_settings(self):
        pass
        
    @abstractmethod
    def get_value(self, key):
        pass
        
    @abstractmethod
    def set_value(self, key, value):
        pass
        
    @abstractmethod
    def reset_value(self, key):
        pass
        
    @abstractmethod
    def set_wallpapers(self, wallpaper):
        pass
        
    @abstractmethod
    def start_systemd_timers(self):
        pass
        
    @abstractmethod
    def stop_systemd_timers(self):
        pass
        
    @abstractmethod
    def get_current_themes(self):
        pass
        
    @abstractmethod
    def get_current_theme(self):
        pass
        
    @abstractmethod
    def set_current_theme(self, theme):
        pass
        
    @abstractmethod
    def get_all_values(self):
        pass
        
    @abstractmethod
    def _get_valid_themes(self):
        pass
