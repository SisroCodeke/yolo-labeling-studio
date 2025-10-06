# core/renderer.py
# """
# High-performance rendering engine with real-time updates
# """

import time
from typing import Optional, Tuple, Dict, List, Deque
from collections import deque
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import logging

from config.config_manager import load_config

CONFIG = load_config()

class HighPerformanceRenderer:
    """High-performance rendering engine with real-time updates"""
    
    def __init__(self, app):
        self.app = app
        self._last_render_time = 0
        self._render_pending = False
        self._dirty = True
        self._temp_box: Optional[Tuple] = None
        
        # Canvas items for better performance
        self.canvas_items: Dict[str, List] = {
            'image': None,
            'boxes': [],
            'labels': [],
            'handles': [],
            'temp_box': None
        }
        
        self.logger = logging.getLogger("Renderer")
    
    @property
    def canvas(self):
        """Get canvas from UI"""
        return self.app.ui.canvas
    
    @property
    def class_names(self):
        """Get class names from app"""
        return self.app.class_names
    
    def mark_dirty(self):
        """Mark that a full redraw is needed"""
        self._dirty = True
        self.request_render()
    
    def request_render(self):
        """Request a render with throttling"""
        if self._render_pending:
            return
            
        current_time = time.time() * 1000
        min_interval = CONFIG["drawing"]["min_redraw_interval"]
        
        if current_time - self._last_render_time >= min_interval:
            self._perform_render()
        else:
            delay = max(1, int(min_interval - (current_time - self._last_render_time)))
            self.app.root.after(delay, self._perform_render)
            self._render_pending = True

    def set_temp_box(self, box_coords: Tuple):
        """Set temporary box for real-time drawing preview"""
        self._temp_box = box_coords
        self._render_boxes_only()
    
    def clear_temp_box(self):
        """Clear temporary box"""
        self._temp_box = None
        self._render_boxes_only()

    def _perform_render(self):
        """Perform the actual rendering"""
        self._render_pending = False
        self._last_render_time = time.time() * 1000
        
        if self._dirty:
            self._render_full()
        else:
            self._render_boxes_only()
    
    def _render_full(self):
        """Perform full render with image and boxes"""
        if self.app.original_image is None:
            return
            
        try:
            # Clear canvas
            self.canvas.delete("all")
            self.canvas_items = {k: [] for k in self.canvas_items.keys()}
            self.canvas_items['image'] = None
            
            # Render base image
            cache_key = f"{self.app.image_name}_{self.app.zoom_scale:.2f}"
            if cache_key in self.app.zoom_cache:
                self.app.tk_image = self.app.zoom_cache[cache_key]
            else:
                img_rgb = cv2.cvtColor(self.app.original_image, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(img_rgb)
                
                if self.app.zoom_scale != 1.0:
                    new_w = int(pil_img.width * self.app.zoom_scale)
                    new_h = int(pil_img.height * self.app.zoom_scale)
                    pil_img = pil_img.resize((new_w, new_h), Image.NEAREST)
                
                self.app.display_image = pil_img
                self.app.tk_image = ImageTk.PhotoImage(image=pil_img)
                
                if CONFIG["drawing"]["cache_zoom_levels"]:
                    self.app.zoom_cache[cache_key] = self.app.tk_image
                    if len(self.app.zoom_cache) > 10:
                        self.app.zoom_cache.pop(next(iter(self.app.zoom_cache)))
            
            # Create image on canvas
            self.canvas_items['image'] = self.canvas.create_image(
                self.app.image_offset_x, self.app.image_offset_y, 
                anchor=tk.NW, image=self.app.tk_image
            )
            
            # Render all boxes
            self._render_all_boxes()
            
            self._dirty = False
            self.app.update_box_list()
            
        except Exception as e:
            self.logger.error("Error in full render", exc_info=True)
    
    def _render_all_boxes(self):
        """Render all boxes as canvas items for better performance"""
        # Clear existing box items
        for item in self.canvas_items['boxes'] + self.canvas_items['labels'] + self.canvas_items['handles']:
            if item:
                self.canvas.delete(item)
        
        self.canvas_items['boxes'] = []
        self.canvas_items['labels'] = []
        self.canvas_items['handles'] = []
        
        # Render permanent boxes
        for idx, box in enumerate(self.app.boxes):
            self._render_single_box(box, idx == self.app.selected_box_idx)
        
        # Render temporary box if exists
        if self._temp_box:
            self._render_temp_box()
    
    def _render_boxes_only(self):
        """Render only boxes (much faster than full render)"""
        if self.app.original_image is None:
            return
            
        self._render_all_boxes()
    
    def _render_single_box(self, box: Dict, is_selected: bool = False):
        """Render a single box as canvas items"""
        if 'class_id' not in box or box['class_id'] is None:
            return
            
        if not (0 <= box['class_id'] < len(self.class_names)):
            return
        
        # Calculate canvas coordinates
        x1 = int(box['x_min'] * self.app.zoom_scale + self.app.image_offset_x)
        y1 = int(box['y_min'] * self.app.zoom_scale + self.app.image_offset_y)
        x2 = int(box['x_max'] * self.app.zoom_scale + self.app.image_offset_x)
        y2 = int(box['y_max'] * self.app.zoom_scale + self.app.image_offset_y)
        
        color = self.app.get_class_color(box['class_id'])
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        
        # Draw box
        box_item = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=hex_color,
            width=self.app.selected_box_line_width if is_selected else self.app.box_line_width,
            tags="box"
        )
        self.canvas_items['boxes'].append(box_item)
        
        # Draw selection outline
        if is_selected:
            outline_item = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline=CONFIG["drawing"]["selected_outline_contrast_color"],
                width=self.app.selected_box_line_width + 2,
                tags="selection"
            )
            self.canvas_items['boxes'].append(outline_item)
            
            # Draw resize handles
            if CONFIG["drawing"]["draw_handles"]:
                handles = [
                    (x1, y1), (x2, y1), (x1, y2), (x2, y2),
                    ((x1+x2)//2, y1), ((x1+x2)//2, y2), (x1, (y1+y2)//2), (x2, (y1+y2)//2)
                ]
                for hx, hy in handles:
                    handle = self.canvas.create_rectangle(
                        hx - self.app.handle_size, hy - self.app.handle_size,
                        hx + self.app.handle_size, hy + self.app.handle_size,
                        fill=CONFIG["drawing"]["handle_fill_selected"],
                        outline=CONFIG["drawing"]["handle_color"],
                        tags="handle"
                    )
                    self.canvas_items['handles'].append(handle)
        
        # Draw label
        class_name = self.class_names[box['class_id']]
        if CONFIG["classes"]["rtl_naive_reverse"] and self.app.contains_persian(class_name) and len(class_name) > 1:
            class_name = class_name[::-1]
        
        label_bg = self.canvas.create_rectangle(
            x1, y1 - 20, x1 + len(class_name) * 8 + 10, y1,
            fill=hex_color,
            outline=hex_color,
            tags="label_bg"
        )
        self.canvas_items['labels'].append(label_bg)
        
        label_text = self.canvas.create_text(
            x1 + 5, y1 - 10,
            text=class_name,
            anchor=tk.W,
            fill=CONFIG["drawing"]["label_text_color"],
            font=("Arial", self.app.label_font_size),
            tags="label"
        )
        self.canvas_items['labels'].append(label_text)
    
    def _render_temp_box(self):
        """Render temporary box for real-time drawing"""
        if not self._temp_box:
            return
            
        x1, y1, x2, y2 = self._temp_box
        
        # Convert to canvas coordinates
        x1_canvas = int(x1 * self.app.zoom_scale + self.app.image_offset_x)
        y1_canvas = int(y1 * self.app.zoom_scale + self.app.image_offset_y)
        x2_canvas = int(x2 * self.app.zoom_scale + self.app.image_offset_x)
        y2_canvas = int(y2 * self.app.zoom_scale + self.app.image_offset_y)
        
        color = self.app.get_class_color(self.app.drawing_class_id)
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        
        # Clear previous temp box
        if self.canvas_items['temp_box']:
            self.canvas.delete(self.canvas_items['temp_box'])
        
        # Draw temporary box with dashed line
        self.canvas_items['temp_box'] = self.canvas.create_rectangle(
            x1_canvas, y1_canvas, x2_canvas, y2_canvas,
            outline=hex_color,
            width=self.app.box_line_width,
            dash=(4, 2),
            tags="temp_box"
        )
