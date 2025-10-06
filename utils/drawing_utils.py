"""
Drawing utilities for canvas operations and coordinate transformations
"""

from typing import Tuple, Optional, Dict, Any
import tkinter as tk


class DrawingUtils:
    """Utilities for drawing operations and coordinate handling"""
    
    @staticmethod
    def image_to_canvas_coords(x_img: float, y_img: float, 
                             zoom_scale: float, 
                             offset_x: float, offset_y: float) -> Tuple[float, float]:
        """Convert image coordinates to canvas coordinates"""
        x_canvas = x_img * zoom_scale + offset_x
        y_canvas = y_img * zoom_scale + offset_y
        return x_canvas, y_canvas
    
    @staticmethod
    def canvas_to_image_coords(x_canvas: float, y_canvas: float,
                             zoom_scale: float,
                             offset_x: float, offset_y: float) -> Tuple[float, float]:
        """Convert canvas coordinates to image coordinates"""
        x_img = (x_canvas - offset_x) / zoom_scale
        y_img = (y_canvas - offset_y) / zoom_scale
        return x_img, y_img
    
    @staticmethod
    def create_box_on_canvas(canvas: tk.Canvas, 
                           x1: float, y1: float, x2: float, y2: float,
                           color: str, width: int = 2, 
                           tags: str = "box") -> int:
        """Create a box on canvas with given parameters"""
        return canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=color,
            width=width,
            tags=tags
        )
    
    @staticmethod
    def create_resize_handle(canvas: tk.Canvas, 
                           x: float, y: float, 
                           size: int,
                           fill_color: str, 
                           outline_color: str,
                           tags: str = "handle") -> int:
        """Create a resize handle on canvas"""
        return canvas.create_rectangle(
            x - size, y - size,
            x + size, y + size,
            fill=fill_color,
            outline=outline_color,
            tags=tags
        )
    
    @staticmethod
    def create_label_background(canvas: tk.Canvas,
                              x: float, y: float,
                              text: str,
                              color: str,
                              padding: int = 4) -> int:
        """Create background for class label"""
        text_width = len(text) * 8  # Approximate width
        return canvas.create_rectangle(
            x, y - 20,
            x + text_width + padding * 2, y,
            fill=color,
            outline=color,
            tags="label_bg"
        )
    
    @staticmethod
    def create_label_text(canvas: tk.Canvas,
                        x: float, y: float,
                        text: str,
                        color: str,
                        font_size: int = 12) -> int:
        """Create class label text"""
        return canvas.create_text(
            x + 5, y - 10,
            text=text,
            anchor=tk.W,
            fill=color,
            font=("Arial", font_size),
            tags="label"
        )
