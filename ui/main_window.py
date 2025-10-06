"""
Main window setup and UI layout
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any

from .components import ButtonPanel, ClassList, BoxList, StatusBar
from .themes import ThemeManager
from config.config_manager import load_config

CONFIG = load_config()


class MainWindow:
    """Main application window layout"""
    
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.theme_manager = ThemeManager()
        
        self.setup_window()
        self.create_widgets()
        self.setup_bindings()
    
    def setup_window(self):
        """Setup main window properties"""
        self.root.title(CONFIG["app"]["window_title"])
        self.root.geometry(CONFIG["app"]["window_geometry"])
        self.root.config(bg=self.theme_manager.get_color('bg'))
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Left panel
        self.left_frame = tk.Frame(
            self.root, 
            bg=self.theme_manager.get_color('panel')
        )
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.left_frame, 
            variable=self.progress_var, 
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # Class list
        self.class_list = ClassList(
            self.left_frame,
            self.theme_manager,
            self.app.class_names,
            self.app.get_class_color
        )
        
        # Buttons
        button_configs = [
            ("Open Image Dir", self.app.open_image_dir),
            ("Open Label Dir", self.app.open_label_dir),
            ("Save Labels", self.app.save_labels),
            ("Prev (A/←)", self.app.prev_image),
            ("Next (D/→)", self.app.next_image),
            ("Zoom In (+)", self.app.zoom_in),
            ("Zoom Out (-)", self.app.zoom_out),
            ("Reset Zoom (R)", self.app.reset_zoom),
            ("Delete Box (Del)", self.app.delete_selected_box),
            ("Select All Boxes (Ctrl+A)", self.app.select_all_boxes),
            ("Duplicate Box (Ctrl+D)", self.app.duplicate_selected_box),
            ("Toggle Dark Mode (Ctrl+D)", self.app.toggle_dark_mode),
            ("Quick Save & Next (Ctrl+Shift+S)", self.app.quick_save_next),
            ("Reload Image (I)", self.app.reload_image)
        ]
        
        self.button_panel = ButtonPanel(
            self.left_frame,
            self.theme_manager,
            button_configs
        )
        
        # Box list panel
        self.box_list = BoxList(self.root, self.theme_manager)
        self.box_list.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Canvas
        self.canvas = tk.Canvas(
            self.root, 
            bg=self.theme_manager.get_color('canvas')
        )
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = StatusBar(self.root, self.theme_manager)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_bindings(self):
        """Setup event bindings"""
        # Class list bindings
        self.class_list.listbox.bind("<Button-3>", self.app.deselect_class)
        
        # Box list bindings
        self.box_list.listbox.bind("<<ListboxSelect>>", self.app.on_box_list_select)
        
        # Canvas bindings
        self.canvas.bind("<Button-1>", self.app.on_left_click_start)
        self.canvas.bind("<ButtonRelease-1>", self.app.on_left_click_end)
        self.canvas.bind("<B1-Motion>", self.app.on_mouse_drag)
        self.canvas.bind("<Button-3>", self.app.select_box)
        self.canvas.bind("<Control-MouseWheel>", self.app.on_mouse_wheel_zoom)
        self.canvas.bind("<Button-4>", self.app.on_mouse_wheel_zoom)
        self.canvas.bind("<Button-5>", self.app.on_mouse_wheel_zoom)
        self.canvas.bind("<Button-2>", self.app.on_middle_click_start)
        self.canvas.bind("<B2-Motion>", self.app.on_pan_drag)
        self.canvas.bind("<ButtonRelease-2>", self.app.on_middle_click_end)
        self.canvas.bind("<Motion>", self.app.on_mouse_move)
        
        # Key bindings
        self.root.bind("<Control-s>", lambda e: self.app.save_labels())
        self.root.bind("<Control-z>", self.app.undo)
        self.root.bind("<Delete>", self.app.delete_selected_box)
        self.root.bind("<Control-a>", self.app.select_all_boxes)
        self.root.bind("<Control-d>", self.app.duplicate_selected_box)
        self.root.bind("<Control-Shift-s>", self.app.quick_save_next)
        self.root.bind("<i>", self.app.reload_image)
        
        for key in CONFIG["keybindings"]["prev_image"]:
            self.root.bind(f"<{key}>", lambda e: self.app.prev_image())
        for key in CONFIG["keybindings"]["next_image"]:
            self.root.bind(f"<{key}>", lambda e: self.app.next_image())
        self.root.bind("<Control-d>", lambda e: self.app.toggle_dark_mode())
        self.root.protocol("WM_DELETE_WINDOW", self.app.on_close)
    
    def update_theme(self):
        """Update all UI colors for current theme"""
        self.root.config(bg=self.theme_manager.get_color('bg'))
        self.left_frame.config(bg=self.theme_manager.get_color('panel'))
        self.canvas.config(bg=self.theme_manager.get_color('canvas'))
        
        self.class_list.update_colors()
        self.button_panel.update_colors()
        self.box_list.update_colors()
        self.status_bar.update_colors()
    
    def set_status(self, text: str):
        """Set status bar text"""
        self.status_bar.set_text(text)
    
    def set_progress(self, value: float):
        """Set progress bar value"""
        self.progress_var.set(value)
    
    def update_box_list(self, boxes: List[Dict], class_names: List[str]):
        """Update box list display"""
        self.box_list.update_boxes(boxes, class_names, self.app.get_class_color)
