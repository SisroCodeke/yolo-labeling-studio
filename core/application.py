"""
Main application class for YOLO Labeling Studio
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import os
import pickle
import time, json
from collections import deque
from typing import List, Dict, Tuple, Optional, Any
import cv2

from config.config_manager import load_config
from .renderer import HighPerformanceRenderer
from .image_cache import ImageCache
from ui.main_window import MainWindow
from utils.file_utils import FileUtils
from utils.text_utils import contains_persian
from models.bounding_box import BoxUtils

CONFIG = load_config()


class YOLOLabelStudio:
    """Main application class for YOLO Labeling Studio"""
    def __init__(self, root):
            self.root = root
            self.setup_logging()
            self.logger = logging.getLogger("YOLOLabelStudio")
            
            # Initialize core components
            self.image_cache = ImageCache(CONFIG["performance"]["image_cache_size"])
            
            # Application state
            self._initialize_state()
            
            # Setup UI first
            self.ui = MainWindow(self.root, self)
            
            # Initialize renderer AFTER UI is created
            self.renderer = HighPerformanceRenderer(self)
            
            # Load previous session if enabled
            if CONFIG["app"]["load_previous_session"]:
                self.load_session_history()
                
            self.logger.info("YOLO Labeling Studio initialized")

    def _initialize_state(self):
        """Initialize application state variables"""
        # Directories and files
        self.image_dir = CONFIG["paths"]["image_dir"]
        self.label_dir = CONFIG["paths"]["label_dir"]
        self.image_files = []
        self.current_index = -1
        self.image_name = ""
        
        # Image data
        self.original_image = None
        self.display_image = None
        self.tk_image = None
        
        # Zoom and pan
        self.zoom_scale = CONFIG["app"]["initial_zoom"]
        self.min_zoom = CONFIG["app"]["min_zoom"]
        self.max_zoom = CONFIG["app"]["max_zoom"]
        self.image_offset_x = 0
        self.image_offset_y = 0
        self.zoom_cache = {}
        
        # Box management
        self.boxes = []
        self.selected_box_idx = -1
        self.drawing_class_id = None
        self.box_list_to_box_index = []
        
        # Drawing state
        self.start_draw_point = None
        self.is_drawing = False
        self.drag_type = None
        self.drag_corner = None
        self.drag_edge = None
        self.pan_start = None
        
        # Configuration
        self.class_names = CONFIG["classes"]["class_names"]
        self.handle_size = CONFIG["drawing"]["handle_size"]
        self.box_line_width = CONFIG["drawing"]["box_line_width"]
        self.selected_box_line_width = CONFIG["drawing"]["selected_box_line_width"]
        self.label_font_size = CONFIG["drawing"]["font_size"]
        self.edge_hit_margin = CONFIG["drawing"]["edge_hit_margin"]
        
        # History and caching
        self.history = deque(maxlen=CONFIG["history"]["undo_history_size"])
        self._cached_class_colors = {}
        self.processed_images = set()

    # Add properties to access UI components
    @property
    def canvas(self):
        """Get canvas from UI"""
        return self.ui.canvas

    def setup_logging(self):
        """Setup application logging"""
        log_dir = CONFIG["paths"]["log_dir"]
        os.makedirs(log_dir, exist_ok=True)
        
        log_filename = os.path.join(
            log_dir,
            f"labeling_tool_{time.strftime(CONFIG['logging']['filename_timestamp_format'])}.log"
        )
        
        handlers = [logging.FileHandler(log_filename)]
        if CONFIG["logging"]["log_to_console"]:
            handlers.append(logging.StreamHandler())
            
        logging.basicConfig(
            level=getattr(logging, CONFIG["logging"]["level"]),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=handlers
        )


    def setup_logging(self):
        """Setup application logging"""
        log_dir = CONFIG["paths"]["log_dir"]
        os.makedirs(log_dir, exist_ok=True)
        
        log_filename = os.path.join(
            log_dir,
            f"labeling_tool_{time.strftime(CONFIG['logging']['filename_timestamp_format'])}.log"
        )
        
        handlers = [logging.FileHandler(log_filename)]
        if CONFIG["logging"]["log_to_console"]:
            handlers.append(logging.StreamHandler())
            
        logging.basicConfig(
            level=getattr(logging, CONFIG["logging"]["level"]),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=handlers
        )

    # ======================
    # Theme Management
    # ======================

    def toggle_dark_mode(self):
        """Toggle between dark and light themes"""
        self.ui.theme_manager.toggle_theme()
        self.ui.update_theme()
        self.renderer.mark_dirty()
        self.logger.info(f"Switched to {'dark' if self.ui.theme_manager.dark_mode else 'light'} mode")

    # ======================
    # Class and Color Management
    # ======================

    def get_class_color(self, class_id):
        """Get color for class ID with caching"""
        return BoxUtils.get_class_color(class_id, self._cached_class_colors)

    def contains_persian(self, text: str) -> bool:
        """Check if text contains Persian/Arabic characters"""
        return contains_persian(text)

    # ======================
    # Image and File Operations
    # ======================

    def open_image_dir(self):
        """Open image directory dialog"""
        directory = filedialog.askdirectory()
        if directory:
            self.image_dir = directory
            self.image_files = FileUtils.find_image_files(directory)
            self.current_index = 0 if self.image_files else -1
            if self.image_files:
                self.load_image()
            self.update_status_label()

    def open_label_dir(self):
        """Open label directory dialog"""
        directory = filedialog.askdirectory()
        if directory:
            self.label_dir = directory
            if self.image_files:
                self.load_image()

    def reload_image(self, event=None):
        """Reload current image and labels"""
        if self.image_files and self.current_index >= 0:
            self.logger.info(f"Reloading image: {self.image_files[self.current_index]}")
            self.load_image()
            self.ui.set_status("Image reloaded")
        else:
            self.ui.set_status("No image to reload")

    def load_image(self):
        """Load current image with caching"""
        if not self.image_files or self.current_index < 0:
            return
            
        path = self.image_files[self.current_index]
        
        # Check if file exists and handle processed images
        path = self._handle_missing_image(path)
        if not path:
            return
            
        # Load image with caching
        self.original_image = FileUtils.load_image_with_caching(path, self.image_cache.cache)
        if self.original_image is None:
            messagebox.showerror("Image Error", f"Failed to load: {os.path.basename(path)}")
            return
            
        self._setup_image_state(path)
        self.load_labels()
        self.save_state()
        self.renderer.mark_dirty()

    def _handle_missing_image(self, path: str) -> Optional[str]:
        """Handle missing image file by checking processed directory"""
        if not os.path.exists(path):
            self.logger.warning(f"Image not found at original path: {path}")
            
            processed_dir = self.get_processed_dir()
            images_dir = os.path.join(processed_dir, 'images')
            filename = os.path.basename(path)
            processed_path = os.path.join(images_dir, filename)
            
            if os.path.exists(processed_path):
                self.logger.info(f"Found image in processed directory: {processed_path}")
                path = processed_path
                self.image_files[self.current_index] = processed_path
            else:
                self.logger.error(f"Image not found in processed directory either: {filename}")
                messagebox.showerror("Image Error", f"Image not found: {filename}")
                return None
                
        return path

    def _setup_image_state(self, path: str):
        """Setup image-related state variables"""
        self.image_name = os.path.splitext(os.path.basename(path))[0]
        self.boxes.clear()
        self.selected_box_idx = -1
        self.image_offset_x = 0
        self.image_offset_y = 0
        self.history.clear()
        self.zoom_cache.clear()
        self.is_drawing = False

    def get_processed_dir(self):
        """Get processed directory path"""
        processed_dir = CONFIG["paths"]["processed_dir"]
        if not os.path.isabs(processed_dir):
            processed_dir = os.path.join(self.image_dir, processed_dir)
        FileUtils.ensure_directory(processed_dir)
        return processed_dir

    def move_to_processed(self, image_path: str):
        """Move image to processed directory"""
        if not CONFIG["behavior"]["auto_move_processed_images"]:
            return
            
        try:
            processed_dir = self.get_processed_dir()
            new_image_path, _ = FileUtils.move_to_processed_dir(
                image_path, processed_dir, create_subdirs=True
            )
            
            if (CONFIG["behavior"]["update_image_paths_after_move"] and 
                new_image_path and self.current_index < len(self.image_files)):
                self.image_files[self.current_index] = new_image_path
                self.processed_images.add(new_image_path)
                self.logger.info(f"Updated image path to: {new_image_path}")
                
        except Exception as e:
            self.log_error(f"Error moving processed image: {image_path}", exc_info=True)

    # ======================
    # Label File Operations
    # ======================

    def load_labels(self):
        """Load labels from YOLO format file"""
        if not self.label_dir or self.original_image is None:
            return
            
        label_path = FileUtils.get_label_path(
            self.image_files[self.current_index], self.label_dir
        )
        
        if not os.path.exists(label_path):
            self.logger.info(f"No label file found: {label_path}")
            return
            
        try:
            with open(label_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    self._parse_label_line(line.strip(), label_path, line_num)
                    
            self.logger.info(f"Loaded {len(self.boxes)} boxes from {label_path}")
            
        except Exception as e:
            self.log_error(f"Error loading labels from {label_path}", exc_info=True)

    def _parse_label_line(self, line: str, label_path: str, line_num: int):
        """Parse a single line from label file"""
        parts = line.strip().split()
        if len(parts) != 5:
            self.logger.warning(f"Invalid line format in {label_path} line {line_num}: {line}")
            return
            
        try:
            cls, cx, cy, w, h = map(float, parts)
            cls = int(cls)
            
            if not (0 <= cls < len(self.class_names)):
                self.logger.warning(f"Invalid class ID {cls} in {label_path} line {line_num}")
                return
                
            # Convert YOLO to pixel coordinates
            h_img, w_img = self.original_image.shape[:2]
            box = BoxUtils.yolo_to_pixel([cls, cx, cy, w, h], w_img, h_img)
            
            # Ensure coordinates are within bounds
            if self._validate_and_clamp_box(box, w_img, h_img):
                self.boxes.append(box.to_dict())
                self.logger.debug(f"Loaded box: class={cls}, coords=({box.x_min},{box.y_min},{box.x_max},{box.y_max})")
            else:
                self.logger.warning(f"Invalid box dimensions in {label_path} line {line_num}")
                
        except ValueError as e:
            self.logger.warning(f"Invalid data in {label_path} line {line_num}: {line} - {e}")

    def _validate_and_clamp_box(self, box, img_width: int, img_height: int) -> bool:
        """Validate and clamp box coordinates to image bounds"""
        box.x_min = max(0, min(box.x_min, img_width))
        box.y_min = max(0, min(box.y_min, img_height))
        box.x_max = max(0, min(box.x_max, img_width))
        box.y_max = max(0, min(box.y_max, img_height))
        
        return box.x_max > box.x_min and box.y_max > box.y_min

    def save_labels(self):
        """Save labels to YOLO format file"""
        if not self.label_dir:
            messagebox.showerror("Save Error", "No label directory selected")
            return
            
        if self.original_image is None:
            messagebox.showerror("Save Error", "No image loaded")
            return
            
        label_path = FileUtils.get_label_path(
            self.image_files[self.current_index], self.label_dir
        )
        
        try:
            with open(label_path, 'w') as f:
                for box_dict in self.boxes:
                    box = BoxUtils.from_dict(box_dict)
                    h_img, w_img = self.original_image.shape[:2]
                    
                    # Convert to YOLO format
                    yolo_coords = BoxUtils.pixel_to_yolo(box, w_img, h_img)
                    
                    # Validate coordinates
                    if self._validate_yolo_coordinates(yolo_coords):
                        line = " ".join(f"{coord:.6f}" for coord in yolo_coords)
                        f.write(line + "\n")
                    else:
                        self.logger.warning(f"Invalid box coordinates: {box_dict}")
                        
            self.save_state()
            self.ui.set_status(f"Labels saved: {len(self.boxes)} boxes")
            self.logger.info(f"Saved {len(self.boxes)} boxes to {label_path}")
            
        except Exception as e:
            self.log_error(f"Error saving labels to {label_path}", exc_info=True)
            messagebox.showerror("Save Error", f"Failed to save labels: {e}")

    def _validate_yolo_coordinates(self, coords: List[float]) -> bool:
        """Validate YOLO format coordinates"""
        _, x_center, y_center, width, height = coords
        return (0 <= x_center <= 1 and 0 <= y_center <= 1 and 
                0 <= width <= 1 and 0 <= height <= 1)

    # ======================
    # Navigation
    # ======================

    def prev_image(self):
        """Navigate to previous image"""
        if self.current_index > 0:
            if CONFIG["app"]["autosave_on_navigation"]:
                self.save_labels()
            self.current_index -= 1
            self.load_image()

    def next_image(self):
        """Navigate to next image"""
        if self.current_index + 1 < len(self.image_files):
            if CONFIG["app"]["autosave_on_navigation"]:
                self.save_labels()
            current_path = self.image_files[self.current_index]
            self.move_to_processed(current_path)
            self.current_index += 1
            self.load_image()

    def update_status_label(self):
        """Update status label with current image info"""
        if self.original_image is not None:
            h, w = self.original_image.shape[:2]
            path = self.image_files[self.current_index] if self.image_files else "-"
            box_count = len(self.boxes)
            status_text = f"{self.image_name} — {w}×{h} — Boxes: {box_count} — {path}"
            self.ui.set_status(status_text)
            
            if self.image_files:
                progress = (self.current_index + 1) / len(self.image_files) * 100
                self.ui.set_progress(progress)
        else:
            self.ui.set_status("Ready")

    # ======================
    # Box List Management
    # ======================

    def update_box_list(self):
        """Update the box list display"""
        self.ui.update_box_list(self.boxes, self.class_names)

    def on_box_list_select(self, event):
        """Handle box selection from list"""
        box_index = self.ui.box_list.get_selected_box_index()
        if box_index is not None:
            self.selected_box_idx = box_index
            self.renderer.mark_dirty()
            box = self.boxes[box_index]
            class_name = self.class_names[box['class_id']]
            self.ui.set_status(f"Selected box: {class_name} #{box_index}")


    def select_all_boxes(self, event=None):
        """Select all boxes in the image"""
        if not self.boxes:
            self.ui.set_status("No boxes to select")
            return
            
        if self.boxes:
            self.selected_box_idx = 0
            self.renderer.mark_dirty()
            self.ui.set_status(f"Selected first of {len(self.boxes)} boxes")
            
            if self.box_list_to_box_index:
                self.ui.box_list.select_box(self.selected_box_idx)

    def duplicate_selected_box(self, event=None):
        """Duplicate the selected box"""
        if self.selected_box_idx == -1:
            self.ui.set_status("No box selected to duplicate")
            return
            
        self.save_state()
        original_box = self.boxes[self.selected_box_idx].copy()
        
        # Offset the duplicated box
        offset = 10
        original_box['x_min'] += offset
        original_box['x_max'] += offset
        original_box['y_min'] += offset
        original_box['y_max'] += offset
        
        self.boxes.append(original_box)
        self.selected_box_idx = len(self.boxes) - 1
        self.renderer.mark_dirty()
        self.ui.set_status("Box duplicated")

    def delete_selected_box(self, event=None):
        """Delete the selected box"""
        if self.selected_box_idx == -1:
            self.ui.set_status("No box selected to delete")
            return
            
        self.save_state()
        del self.boxes[self.selected_box_idx]
        self.selected_box_idx = -1
        self.renderer.mark_dirty()
        self.ui.set_status("Box deleted")

    def quick_save_next(self, event=None):
        """Quick save and move to next image"""
        if self.image_files and self.current_index >= 0:
            self.save_labels()
            self.next_image()

    def deselect_class(self, event):
        """Deselect current class"""
        self.ui.class_list.clear_selection()
        self.drawing_class_id = None
        self.selected_box_idx = -1
        self.renderer.mark_dirty()
        self.ui.set_status("Class and box deselected")

    # ======================
    # History Management
    # ======================

    def save_state(self):
        """Save current state for undo functionality"""
        self.history.append([box.copy() for box in self.boxes])

    def undo(self, event=None):
        """Undo last operation"""
        if self.history:
            self.boxes = self.history.pop()
            if self.selected_box_idx >= len(self.boxes):
                self.selected_box_idx = -1
            self.renderer.mark_dirty()
            self.ui.set_status("Undo successful")
        else:
            self.ui.set_status("Nothing to undo")

    # ======================
    # Zoom and Pan Operations
    # ======================

    def on_mouse_wheel_zoom(self, event):
        """Handle mouse wheel zoom"""
        if event.delta > 0 or event.num == 4:
            self.zoom_in(event)
        else:
            self.zoom_out(event)

    def zoom_in(self, event=None):
        """Zoom in"""
        if self.zoom_scale >= self.max_zoom:
            return
        self._apply_zoom(1 / CONFIG["app"]["zoom_factor_in"], event)

    def zoom_out(self, event=None):
        """Zoom out"""
        if self.zoom_scale <= self.min_zoom:
            return
        self._apply_zoom(CONFIG["app"]["zoom_factor_out"], event)

    def reset_zoom(self):
        """Reset zoom to 100%"""
        self.zoom_scale = 1.0
        self.image_offset_x = 0
        self.image_offset_y = 0
        self.renderer.mark_dirty()

    def _apply_zoom(self, factor, event=None):
        """Apply zoom transformation"""
        if self.original_image is None:
            return

        old_scale = self.zoom_scale
        new_scale = old_scale / factor
        new_scale = max(self.min_zoom, min(self.max_zoom, new_scale))
        
        if new_scale == old_scale:
            return

        if event is None:
            self.zoom_scale = new_scale
            self.image_offset_x = 0
            self.image_offset_y = 0
            self.renderer.mark_dirty()
            return

        # Zoom relative to mouse position
        mouse_x = event.x
        mouse_y = event.y
        img_x = (mouse_x - self.image_offset_x) / old_scale
        img_y = (mouse_y - self.image_offset_y) / old_scale

        self.zoom_scale = new_scale
        self.image_offset_x = mouse_x - img_x * new_scale
        self.image_offset_y = mouse_y - img_y * new_scale
        self.renderer.mark_dirty()

    # ======================
    # Pan Support
    # ======================

    def on_middle_click_start(self, event):
        """Start pan operation"""
        self.pan_start = (event.x, event.y)
        self.ui.canvas.config(cursor="fleur")

    def on_pan_drag(self, event):
        """Handle pan dragging"""
        if self.pan_start is None:
            return
            
        dx = event.x - self.pan_start[0]
        dy = event.y - self.pan_start[1]
        self.image_offset_x += dx
        self.image_offset_y += dy
        self.pan_start = (event.x, event.y)
        self.renderer.mark_dirty()

    def on_middle_click_end(self, event):
        """End pan operation"""
        self.pan_start = None
        self.ui.canvas.config(cursor="")

    # ======================
    # Drag Detection for Corners and Edges
    # ======================

    def detect_drag_target(self, event_x, event_y, box):
        """Detect if cursor is over a corner or edge of the selected box"""
        # Convert box coordinates to canvas coordinates
        x1_canvas = box['x_min'] * self.zoom_scale + self.image_offset_x
        y1_canvas = box['y_min'] * self.zoom_scale + self.image_offset_y
        x2_canvas = box['x_max'] * self.zoom_scale + self.image_offset_x
        y2_canvas = box['y_max'] * self.zoom_scale + self.image_offset_y
        
        margin = self.edge_hit_margin
        
        # Check corners first (higher priority)
        corners = [
            (x1_canvas, y1_canvas, 'tl'), 
            (x2_canvas, y1_canvas, 'tr'),
            (x1_canvas, y2_canvas, 'bl'), 
            (x2_canvas, y2_canvas, 'br')
        ]
        
        for cx, cy, corner in corners:
            if abs(event_x - cx) < margin and abs(event_y - cy) < margin:
                return 'corner', corner
        
        # Check edges if no corner was hit
        # Top edge
        if (x1_canvas <= event_x <= x2_canvas and 
            abs(event_y - y1_canvas) < margin):
            return 'edge', 'top'
        
        # Bottom edge
        if (x1_canvas <= event_x <= x2_canvas and 
            abs(event_y - y2_canvas) < margin):
            return 'edge', 'bottom'
        
        # Left edge
        if (y1_canvas <= event_y <= y2_canvas and 
            abs(event_x - x1_canvas) < margin):
            return 'edge', 'left'
        
        # Right edge
        if (y1_canvas <= event_y <= y2_canvas and 
            abs(event_x - x2_canvas) < margin):
            return 'edge', 'right'
        
        # Check if inside box for moving
        if (x1_canvas <= event_x <= x2_canvas and y1_canvas <= event_y <= y2_canvas):
            return 'move', None
        
        return None, None

    def get_cursor_for_drag_target(self, drag_type, target):
        """Get appropriate cursor for drag target"""
        if drag_type == 'corner':
            if target in ['tl', 'br']:
                return "crosshair"
            elif target in ['tr', 'bl']:
                return "crosshair"
        elif drag_type == 'edge':
            if target in ['top', 'bottom']:
                return "sb_v_double_arrow"
            elif target in ['left', 'right']:
                return "sb_h_double_arrow"
        elif drag_type == 'move':
            return "fleur"
        return ""


    
    # ======================
    # Mouse Event Handlers
    # ======================

    def on_mouse_move(self, event):
        """Handle mouse movement for real-time cursor changes"""
        # Don't change cursor while drawing or dragging
        if self.is_drawing or self.drag_type:
            return
            
        # Update cursor based on position near selected box corners/edges
        if self.selected_box_idx != -1:
            box = self.boxes[self.selected_box_idx]
            drag_type, drag_target = self.detect_drag_target(event.x, event.y, box)
            
            if drag_type:
                cursor = self.get_cursor_for_drag_target(drag_type, drag_target)
                self.ui.canvas.config(cursor=cursor)
                return
        
        # Default cursor
        self.ui.canvas.config(cursor="")

# Add this method to your YOLOLabelStudio class in core/application.py
    def debug_class_selection(self):
        """Debug method to check class selection state"""
        selection = self.ui.class_list.get_selection()
        print(f"DEBUG - Class selection: {selection}")
        print(f"DEBUG - Drawing class ID: {self.drawing_class_id}")
        print(f"DEBUG - Class names: {self.class_names}")
        if selection is not None and selection < len(self.class_names):
            print(f"DEBUG - Selected class name: {self.class_names[selection]}")
        print(f"DEBUG - Is drawing: {self.is_drawing}")
        print(f"DEBUG - Start draw point: {self.start_draw_point}")

    # In core/application.py - Update on_left_click_start method


    def on_left_click_start(self, event):
        """Handle left mouse button press with better debugging"""
        current_time = time.time()

        # Debug info
        print(f"=== LEFT CLICK START ===")
        self.debug_class_selection()

        # Reset selection if out of bounds
        if self.selected_box_idx != -1 and not (0 <= self.selected_box_idx < len(self.boxes)):
            self.selected_box_idx = -1

        mouse_x_img = (event.x - self.image_offset_x) / self.zoom_scale
        mouse_y_img = (event.y - self.image_offset_y) / self.zoom_scale

        self.last_click_time = current_time

        # FIRST: Check if clicking on corners/edges of SELECTED box for resize/move
        if self.selected_box_idx != -1:
            box = self.boxes[self.selected_box_idx]
            drag_type, drag_target = self.detect_drag_target(event.x, event.y, box)
            
            if drag_type in ('corner', 'edge', 'move'):
                self.drag_type = 'resize' if drag_type in ('corner', 'edge') else 'move'
                self.drag_corner = drag_target if drag_type == 'corner' else None
                self.drag_edge = drag_target if drag_type == 'edge' else None
                self.start_draw_point = (mouse_x_img, mouse_y_img)
                self.is_drawing = False
                
                action = f"Resizing {drag_target} {'corner' if drag_type == 'corner' else 'edge'}" if drag_type != 'move' else "Moving box"
                self.ui.set_status(action)
                print(f"Drag operation: {action}")
                return

        # Check if class is selected
        selected_class = self.ui.class_list.get_selection()
        print(f"Selected class index: {selected_class}")
        
        if selected_class is None:
            self.ui.set_status("Select a class before drawing")
            print("ERROR: No class selected!")
            return

        # Start drawing new box
        self.drawing_class_id = selected_class
        self.start_draw_point = (mouse_x_img, mouse_y_img)
        self.is_drawing = True
        self.selected_box_idx = -1  # Deselect any selected box when starting new drawing
        self.drag_type = None
        self.drag_corner = None
        self.drag_edge = None
        
        class_name = self.class_names[self.drawing_class_id]
        self.ui.set_status(f"Drawing new {class_name} box")
        print(f"Started drawing: {class_name} (class_id: {self.drawing_class_id})")

    def on_mouse_drag(self, event):
        """Handle mouse dragging for real-time operations"""
        current_x_img = (event.x - self.image_offset_x) / self.zoom_scale
        current_y_img = (event.y - self.image_offset_y) / self.zoom_scale

        # Handle box resizing/moving (HIGHEST PRIORITY)
        if self.drag_type in ('resize', 'move') and self.selected_box_idx != -1:
            if not hasattr(self, 'saved_state_for_drag'):
                self.save_state()
                self.saved_state_for_drag = True

            dx = current_x_img - self.start_draw_point[0]
            dy = current_y_img - self.start_draw_point[1]

            box = self.boxes[self.selected_box_idx]
            self._handle_box_drag(box, dx, dy)

            self.start_draw_point = (current_x_img, current_y_img)
            self.renderer.mark_dirty()

        # Handle new box drawing with real-time preview
        elif self.start_draw_point and self.is_drawing and self.drawing_class_id is not None:
            x1, y1 = self.start_draw_point
            x2, y2 = current_x_img, current_y_img
            
            # Create temporary box for real-time preview
            temp_box = (
                min(x1, x2), min(y1, y2),
                max(x1, x2), max(y1, y2)
            )
            self.renderer.set_temp_box(temp_box)  # This should work now

    # And in on_left_click_end method:
    def on_left_click_end(self, event):
        """Handle left mouse button release"""
        # Handle drag operations (resize/move)
        if self.drag_type:
            self.drag_type = None
            self.drag_corner = None
            self.drag_edge = None
            if hasattr(self, 'saved_state_for_drag'):
                del self.saved_state_for_drag
            self.renderer.mark_dirty()
            self.ui.set_status("Box modified")
            return

        # Handle new box creation
        if self.start_draw_point and self.is_drawing:
            self._create_new_box(event)
            self.start_draw_point = None
            self.is_drawing = False
            self.renderer.clear_temp_box()  # This should work now
            self.renderer.mark_dirty()

    def _handle_box_drag(self, box, dx, dy):
        """Handle box dragging for resize and move operations"""
        if self.drag_type == 'resize':
            # Corner resizing
            if self.drag_corner:
                if self.drag_corner == 'tl':
                    box['x_min'] = max(0, box['x_min'] + dx)
                    box['y_min'] = max(0, box['y_min'] + dy)
                elif self.drag_corner == 'tr':
                    box['x_max'] = max(0, box['x_max'] + dx)
                    box['y_min'] = max(0, box['y_min'] + dy)
                elif self.drag_corner == 'bl':
                    box['x_min'] = max(0, box['x_min'] + dx)
                    box['y_max'] = max(0, box['y_max'] + dy)
                elif self.drag_corner == 'br':
                    box['x_max'] = max(0, box['x_max'] + dx)
                    box['y_max'] = max(0, box['y_max'] + dy)
            
            # Edge resizing
            elif self.drag_edge:
                if self.drag_edge == 'top':
                    box['y_min'] = max(0, box['y_min'] + dy)
                elif self.drag_edge == 'bottom':
                    box['y_max'] = max(0, box['y_max'] + dy)
                elif self.drag_edge == 'left':
                    box['x_min'] = max(0, box['x_min'] + dx)
                elif self.drag_edge == 'right':
                    box['x_max'] = max(0, box['x_max'] + dx)
                    
        elif self.drag_type == 'move':
            box['x_min'] = max(0, box['x_min'] + dx)
            box['y_min'] = max(0, box['y_min'] + dy)
            box['x_max'] = max(0, box['x_max'] + dx)
            box['y_max'] = max(0, box['y_max'] + dy)

        # Ensure box maintains minimum size
        self._enforce_minimum_box_size(box)

    def _enforce_minimum_box_size(self, box):
        """Ensure box maintains minimum size"""
        min_size = 5
        if box['x_max'] - box['x_min'] < min_size:
            if self.drag_corner in ['tr', 'br'] or self.drag_edge == 'right':
                box['x_max'] = box['x_min'] + min_size
            else:
                box['x_min'] = box['x_max'] - min_size
                
        if box['y_max'] - box['y_min'] < min_size:
            if self.drag_corner in ['bl', 'br'] or self.drag_edge == 'bottom':
                box['y_max'] = box['y_min'] + min_size
            else:
                box['y_min'] = box['y_max'] - min_size

    def _create_new_box(self, event):
        """Create a new box from drawing coordinates"""
        x1, y1 = self.start_draw_point
        x2 = (event.x - self.image_offset_x) / self.zoom_scale
        y2 = (event.y - self.image_offset_y) / self.zoom_scale
        
        # Only create box if significant size and class is selected
        if (abs(x2 - x1) > 10 and abs(y2 - y1) > 10 and
            self.drawing_class_id is not None and
            self.original_image is not None):
            
            self.save_state()
            
            # Ensure coordinates are within image bounds
            h, w = self.original_image.shape[:2]
            x1 = max(0, min(x1, w))
            y1 = max(0, min(y1, h))
            x2 = max(0, min(x2, w))
            y2 = max(0, min(y2, h))
            
            new_box = {
                'class_id': self.drawing_class_id,
                'x_min': min(x1, x2),
                'y_min': min(y1, y2),
                'x_max': max(x1, x2),
                'y_max': max(y1, y2)
            }
            self.boxes.append(new_box)
            self.selected_box_idx = len(self.boxes) - 1
            self.ui.set_status("Box added")

    def select_box(self, event):
        """Select box with right click"""
        if self.is_drawing:
            return  # Don't select boxes while drawing
            
        x_img = (event.x - self.image_offset_x) / self.zoom_scale
        y_img = (event.y - self.image_offset_y) / self.zoom_scale
        
        # Check boxes in reverse order (top-most boxes first)
        for i in range(len(self.boxes) - 1, -1, -1):
            box = self.boxes[i]
            if (box['x_min'] <= x_img <= box['x_max'] and 
                box['y_min'] <= y_img <= box['y_max']):
                
                if i == self.selected_box_idx and CONFIG["behavior"]["deselect_box_on_second_click"]:
                    self.selected_box_idx = -1
                    self.ui.set_status("Box deselected")
                else:
                    self.selected_box_idx = i
                    class_name = self.class_names[box['class_id']]
                    self.ui.set_status(f"Selected box {i} - Class {class_name}")
                
                self.renderer.mark_dirty()
                
                # Update box list selection
                if self.selected_box_idx != -1:
                    self.ui.box_list.select_box(self.selected_box_idx)
                else:
                    self.ui.box_list.clear_selection()
                    
                return
                
        # If no box was clicked, deselect
        self.selected_box_idx = -1
        self.ui.box_list.clear_selection()
        self.ui.set_status("No box selected")
        self.renderer.mark_dirty()

    # ======================
    # Session Management
    # ======================

    def save_session_history(self):
        """Save session history to file"""
        try:
            session_data = {
                'image_dir': self.image_dir,
                'label_dir': self.label_dir,
                'current_index': self.current_index,
                'image_files': self.image_files,
                'boxes': self.boxes,
                'selected_box_idx': self.selected_box_idx,
                'zoom_scale': self.zoom_scale,
                'class_names': self.class_names,
                'drawing_class_id': self.drawing_class_id
            }
            
            with open(CONFIG["app"]["session_history_file"], 'wb') as f:
                pickle.dump(session_data, f)
                
        except Exception as e:
            self.log_error("Error saving session history", exc_info=True)

    def load_session_history(self):
        """Load session history from file"""
        history_file = CONFIG["app"]["session_history_file"]
        if not os.path.exists(history_file):
            return False
            
        try:
            with open(history_file, 'rb') as f:
                data = pickle.load(f)
                
            self.image_dir = data.get('image_dir', '')
            self.label_dir = data.get('label_dir', '')
            self.image_files = data.get('image_files', [])
            self.current_index = data.get('current_index', -1)
            
            if 0 <= self.current_index < len(self.image_files):
                path = self.image_files[self.current_index]
                if os.path.exists(path):
                    img = cv2.imread(path)
                    if img is not None:
                        self.original_image = img
                        self.image_name = os.path.splitext(os.path.basename(path))[0]
                        self.boxes = data.get('boxes', [])
                        self.selected_box_idx = data.get('selected_box_idx', -1)
                        if self.selected_box_idx >= len(self.boxes):
                            self.selected_box_idx = -1
                        self.zoom_scale = data.get('zoom_scale', 1.0)
                        self.drawing_class_id = data.get('drawing_class_id')
                        if self.drawing_class_id is not None:
                            self.ui.class_list.listbox.selection_clear(0, tk.END)
                            self.ui.class_list.listbox.selection_set(self.drawing_class_id)
                        self.renderer.mark_dirty()
                        self.update_status_label()
                        self.ui.set_status(f"Restored session - {self.image_name}")
                        return True
                else:
                    self.logger.warning(f"Cached image not found: {path}")
                    
        except Exception as e:
            self.log_error("Error loading session", exc_info=True)
        return False

    def on_close(self):
        """Handle application close"""
        try:
            # Save configuration
            with open("yolo_gui_config.json", 'w') as f:
                json.dump({"image_dir": self.image_dir, "label_dir": self.label_dir}, f)
                
            self.save_session_history()
            
            # Clear caches
            self.image_cache.clear()
            self.zoom_cache.clear()
            
        except Exception as e:
            self.log_error("Error during shutdown", exc_info=True)
        finally:
            self.root.destroy()

    def log_error(self, msg, exc_info=False):
        """Log error with context"""
        self.logger.error(msg, exc_info=exc_info)
        self.ui.set_status(f"Error: {msg}")
