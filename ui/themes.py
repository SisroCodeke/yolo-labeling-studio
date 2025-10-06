"""
Theme management for the application
"""

from typing import Dict, Any


class ThemeManager:
    """Manages application themes and colors"""
    
    DARK_THEME = {
        'bg': "#2d2d2d",
        'fg': "#ffffff", 
        'panel': "#3d3d3d",
        'canvas': "#1d1d1d",
        'button': "#4d4d4d",
        'listbox': "#3d3d3d",
        'status': "#3d3d3d",
        'accent': "#007acc",
        'success': "#4caf50",
        'warning': "#ff9800",
        'error': "#f44336"
    }
    
    LIGHT_THEME = {
        'bg': "#f4f4f4",
        'fg': "#000000",
        'panel': "#fafafa", 
        'canvas': "gray",
        'button': "#e0e0e0",
        'listbox': "#ffffff",
        'status': "#e0e0e0",
        'accent': "#2196f3",
        'success': "#4caf50",
        'warning': "#ff9800",
        'error': "#f44336"
    }
    
    def __init__(self, dark_mode: bool = True):
        self.dark_mode = dark_mode
        self.colors = self.DARK_THEME if dark_mode else self.LIGHT_THEME
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.dark_mode = not self.dark_mode
        self.colors = self.DARK_THEME if self.dark_mode else self.LIGHT_THEME
        return self.dark_mode
    
    def get_colors(self) -> Dict[str, str]:
        """Get current theme colors"""
        return self.colors.copy()
    
    def get_color(self, key: str, default: str = "#000000") -> str:
        """Get specific color from theme"""
        return self.colors.get(key, default)
