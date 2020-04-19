from abc import ABC, abstractmethod

class Desktop(ABC):
        
    @abstractmethod
    def init_settings(self):
        raise NotImplementedError
        
    @abstractmethod
    def get_value(self, key):
        raise NotImplementedError
        
    @abstractmethod
    def set_value(self, key, value):
        raise NotImplementedError
        
    @abstractmethod
    def reset_value(self, key):
        raise NotImplementedError
        
    @abstractmethod
    def set_wallpapers(self, wallpaper):
        raise NotImplementedError
        
    @abstractmethod
    def start_systemd_timers(self):
        raise NotImplementedError
        
    @abstractmethod
    def stop_systemd_timers(self):
        raise NotImplementedError
        
    @abstractmethod
    def get_current_themes(self):
        raise NotImplementedError
        
    @abstractmethod
    def get_current_theme(self):
        raise NotImplementedError
        
    @abstractmethod
    def set_current_theme(self, theme):
        raise NotImplementedError
        
    @abstractmethod
    def get_all_values(self):
        raise NotImplementedError
        
    @abstractmethod
    def _get_valid_themes(self):
        raise NotImplementedError

    @abstractmethod
    def get_terminal_profiles(self):
        raise NotImplementedError
        
    @abstractmethod
    def execute_script(self, script):
        raise NotImplementedError
