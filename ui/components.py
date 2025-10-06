# ui/components.py
"""
UI components and widgets for the application
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional, Dict, Any


class ButtonPanel:
    """Panel for organizing buttons"""
    
    def __init__(self, parent, theme_manager, button_configs: List[tuple]):
        """
        Args:
            parent: Parent widget
            theme_manager: ThemeManager instance
            button_configs: List of (text, command) tuples
        """
        self.parent = parent
        self.theme_manager = theme_manager
        self.buttons = {}
        self.create_buttons(button_configs)
    
    def create_buttons(self, button_configs: List[tuple]):
        """Create buttons from configuration"""
        for text, command in button_configs:
            btn = tk.Button(
                self.parent,
                text=text,
                command=command,
                bg=self.theme_manager.get_color('button'),
                fg=self.theme_manager.get_color('fg'),
                relief=tk.RAISED,
                bd=1
            )
            btn.pack(fill=tk.X, pady=2)
            self.buttons[text] = btn
    
    def update_colors(self):
        """Update button colors based on current theme"""
        for btn in self.buttons.values():
            btn.config(
                bg=self.theme_manager.get_color('button'),
                fg=self.theme_manager.get_color('fg')
            )


class ClassList:
    """Class list component with color coding"""
    
    def __init__(self, parent, theme_manager, class_names: List[str], 
                 get_class_color: Callable):
        """
        Args:
            parent: Parent widget
            theme_manager: ThemeManager instance
            class_names: List of class names
            get_class_color: Function to get color for class index
        """
        self.parent = parent
        self.theme_manager = theme_manager
        self.class_names = class_names
        self.get_class_color = get_class_color
        
        self.label = tk.Label(
            parent, 
            text="All Classes", 
            bg=self.theme_manager.get_color('panel'),
            fg=self.theme_manager.get_color('fg')
        )
        self.label.pack(anchor='w', padx=5)
        
        self.listbox = tk.Listbox(
            parent, 
            font=("Arial", 11),
            bg=self.theme_manager.get_color('listbox'),
            fg=self.theme_manager.get_color('fg'),
            selectbackground=self.theme_manager.get_color('accent'),
            selectmode=tk.SINGLE  # Ensure single selection
        )
        self.listbox.pack(padx=5, pady=5, fill=tk.X)
        
        self.populate_classes()
        
        # Bind selection event
        self.listbox.bind('<<ListboxSelect>>', self.on_selection_change)
    
    def on_selection_change(self, event):
        """Handle class selection change"""
        selection = self.get_selection()
        print(f"Class selection changed to: {selection}")
    
    def populate_classes(self):
        """Populate listbox with classes and colors"""
        self.listbox.delete(0, tk.END)
        for i, name in enumerate(self.class_names):
            self.listbox.insert(tk.END, name)
            r, g, b = self.get_class_color(i)
            self.listbox.itemconfig(i, bg=f"#{r:02x}{g:02x}{b:02x}", fg="white")
    
    def get_selection(self) -> Optional[int]:
        """Get currently selected class index"""
        selection = self.listbox.curselection()
        return selection[0] if selection else None
    
    def set_selection(self, index: int):
        """Set class selection by index"""
        self.listbox.selection_clear(0, tk.END)
        if 0 <= index < self.listbox.size():
            self.listbox.selection_set(index)
            self.listbox.see(index)
    
    def clear_selection(self):
        """Clear class selection"""
        self.listbox.selection_clear(0, tk.END)
    
    def update_colors(self):
        """Update colors based on current theme"""
        self.label.config(
            bg=self.theme_manager.get_color('panel'),
            fg=self.theme_manager.get_color('fg')
        )
        self.listbox.config(
            bg=self.theme_manager.get_color('listbox'),
            fg=self.theme_manager.get_color('fg')
        )


class BoxList:
    """Box list component for displaying image boxes"""
    
    def __init__(self, parent, theme_manager):
        self.parent = parent
        self.theme_manager = theme_manager
        self.box_list_to_box_index = []
        
        self.frame = tk.Frame(
            parent, 
            bg=self.theme_manager.get_color('panel'),
            bd=1, 
            relief=tk.SUNKEN
        )
        
        self.label = tk.Label(
            self.frame,
            text="Boxes in Image",
            bg=self.theme_manager.get_color('panel'),
            fg=self.theme_manager.get_color('fg')
        )
        self.label.pack(anchor='w', padx=5)
        
        self.listbox = tk.Listbox(
            self.frame,
            font=("Arial", 11),
            bg=self.theme_manager.get_color('listbox'),
            fg=self.theme_manager.get_color('fg'),
            selectbackground=self.theme_manager.get_color('accent')
        )
        self.listbox.pack(padx=5, pady=5, fill=tk.Y, expand=True)
    
    def pack(self, **kwargs):
        """Pack the frame"""
        self.frame.pack(**kwargs)
    
    def update_boxes(self, boxes: List[Dict], class_names: List[str], get_class_color: Callable):
        """Update box list with current boxes"""
        self.listbox.delete(0, tk.END)
        self.box_list_to_box_index = []
        class_counts = {}

        for box_idx, box in enumerate(boxes):
            cls_id = box.get('class_id')
            if cls_id is None or not (0 <= cls_id < len(class_names)):
                continue
                
            class_name = class_names[cls_id]
            count = class_counts.get(class_name, 0)
            display_text = f"{class_name} #{count}"
            class_counts[class_name] = count + 1

            self.listbox.insert(tk.END, display_text)
            r, g, b = get_class_color(cls_id)
            self.listbox.itemconfig(tk.END, bg=f"#{r:02x}{g:02x}{b:02x}", fg="white")
            self.box_list_to_box_index.append(box_idx)
    
    def get_selected_box_index(self) -> Optional[int]:
        """Get selected box index"""
        selection = self.listbox.curselection()
        if not selection:
            return None
            
        list_index = selection[0]
        if list_index >= len(self.box_list_to_box_index):
            return None
            
        return self.box_list_to_box_index[list_index]
    
    def select_box(self, box_index: int):
        """Select box in list by index"""
        self.listbox.selection_clear(0, tk.END)
        for list_idx, stored_idx in enumerate(self.box_list_to_box_index):
            if stored_idx == box_index:
                self.listbox.selection_set(list_idx)
                self.listbox.see(list_idx)
                break
    
    def clear_selection(self):
        """Clear box selection"""
        self.listbox.selection_clear(0, tk.END)
    
    def update_colors(self):
        """Update colors based on current theme"""
        self.frame.config(bg=self.theme_manager.get_color('panel'))
        self.label.config(
            bg=self.theme_manager.get_color('panel'),
            fg=self.theme_manager.get_color('fg')
        )
        self.listbox.config(
            bg=self.theme_manager.get_color('listbox'),
            fg=self.theme_manager.get_color('fg')
        )


class StatusBar:
    """Status bar component"""
    
    def __init__(self, parent, theme_manager):
        self.parent = parent
        self.theme_manager = theme_manager
        
        self.label = tk.Label(
            parent,
            text="Ready",
            anchor='w',
            bg=self.theme_manager.get_color('status'),
            fg=self.theme_manager.get_color('fg'),
            relief=tk.SUNKEN,
            bd=1
        )
    
    def pack(self, **kwargs):
        """Pack the status bar"""
        self.label.pack(**kwargs)
    
    def set_text(self, text: str):
        """Set status text"""
        self.label.config(text=text)
    
    def update_colors(self):
        """Update colors based on current theme"""
        self.label.config(
            bg=self.theme_manager.get_color('status'),
            fg=self.theme_manager.get_color('fg')
        )
