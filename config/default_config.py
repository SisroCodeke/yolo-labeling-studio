"""
Default configuration for YOLO Labeling Studio
"""

DEFAULT_CONFIG = {
    "app": {
        "window_title": "YOLO Labeling Studio Pro - RealTime FIXED",
        "window_geometry": "1280x900",
        "theme": "dark",
        "status_bar": True,
        "confirm_on_exit": True,
        "autosave_on_navigation": True,
        "load_previous_session": True,
        "initial_zoom": 1.0,
        "min_zoom": 0.2,
        "max_zoom": 4.0,
        "zoom_factor_in": 1.25,
        "zoom_factor_out": 1.25,
        "mouse_wheel_zoom": True,
        "mouse_wheel_zoom_step": 1.15,
        "session_history_file": "session_history.pkl"
    },
    "paths": {
        "image_dir": "",
        "label_dir": "",
        "processed_dir": "processed",
        "log_dir": "logs",
        "font_search_paths": [
            "arial.ttf",
            "Vazirmatn-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ],
        "default_config_save": "yolo_gui_config.json"
    },
    "classes": {
        "class_names": ["vehicle", "plate"],
        "show_class_index": False,
        "rtl_naive_reverse": True,
        "min_box_draw_pixels": 3,
        "restrict_drawing_inside_image": True
    },
    "drawing": {
        "color_mode": "golden_angle",
        "golden_angle_offset": 137,
        "fixed_colors": {},
        "random_seed": 1234,
        "hsv_saturation": 0.7,
        "hsv_value": 1.0,
        "box_line_width": 2,
        "ed_box_line_width": 3,
        "selected_box_line_width": 3,
        "handle_size": 5,
        "handle_color": "#0000ff",
        "handle_fill_selected": "#0000ff",
        "draw_handles": True,
        "draw_label_background": True,
        "label_text_color": "#000000",
        "selected_outline_contrast_color": "#000000",
        "font_size": 12,
        "label_padding": 4,
        "inside_fallback_when_no_space": True,
        "resize_interpolation": "nearest",
        "show_fps_overlay": False,
        "translucent_selected": False,
        "selected_alpha": 128,
        "enable_canvas_cache": True,
        "cache_zoom_levels": True,
        "real_time_drawing": True,
        "min_redraw_interval": 16,
        "edge_hit_margin": 8
    },
    "font": {
        "preferred_font": "arial.ttf",
        "fallback_to_default": True
    },
    "history": {
        "undo_history_size": 100,
        "auto_save_state_on_load": True
    },
    "label_format": {
        "type": "yolo",
        "float_precision": 6,
        "sort_boxes_on_save": False,
        "include_trailing_newline": True
    },
    "behavior": {
        "allow_move": True,
        "allow_resize": True,
        "new_box_starts_on_click": True,
        "use_drag_for_box": True,
        "select_on_right_click": True,
        "deselect_class_on_right_click_list": True,
        "deselect_box_on_second_click": True,
        "auto_move_processed_images": True,
        "select_first_box_on_class_click": False,
        "enable_batch_operations": True,
        "smart_rendering": True,
        "lazy_image_loading": True,
        "keep_class_selected_after_drawing": True,
        "update_image_paths_after_move": True,
        "real_time_box_preview": True
    },
    "keybindings": {
        "save": "Control-s",
        "undo": "Control-z",
        "delete_box": "Delete",
        "prev_image": ["Left", "a"],
        "next_image": ["Right", "d"],
        "zoom_in": "plus",
        "zoom_out": "minus",
        "reset_zoom": "r",
        "toggle_dark_mode": "Control-d",
        "select_all_boxes": "Control-a",
        "duplicate_box": "Control-d",
        "quick_save_next": "Control-Shift-s",
        "reload_image": "i"
    },
    "logging": {
        "level": "INFO",
        "log_to_console": True,
        "filename_timestamp_format": "%Y%m%d_%H%M%S",
        "max_bytes": 0,
        "backup_count": 0
    },
    "constraints": {
        "clamp_boxes_inside_image": True,
        "prevent_negative_coords": True,
        "min_box_side_pixels": 1
    },
    "autosave": {
        "enabled": True,
        "on_interval_seconds": 0,
        "on_class_change": False
    },
    "plugins": {
        "enabled": [],
        "config": {}
    },
    "performance": {
        "image_cache_size": 5,
        "enable_selective_rendering": True,
        "render_throttle_ms": 16,
        "optimize_memory_usage": True,
        "enable_gpu_acceleration": False,
        "enable_double_buffering": True,
        "use_canvas_items": True,
        "max_fps": 60
    }
}
