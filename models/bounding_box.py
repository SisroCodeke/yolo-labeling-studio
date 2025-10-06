# models/bounding_box.py
"""
Bounding box data model and utilities
"""

from typing import Dict, Any, List, Tuple
import colorsys


class BoundingBox:
    """Represents a bounding box with class information"""
    
    def __init__(self, class_id: int, x_min: float, y_min: float, x_max: float, y_max: float):
        self.class_id = class_id
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            'class_id': self.class_id,
            'x_min': self.x_min,
            'y_min': self.y_min,
            'x_max': self.x_max,
            'y_max': self.y_max
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BoundingBox':
        """Create from dictionary"""
        return cls(
            class_id=data['class_id'],
            x_min=data['x_min'],
            y_min=data['y_min'],
            x_max=data['x_max'],
            y_max=data['y_max']
        )
    
    @property
    def width(self) -> float:
        return self.x_max - self.x_min
    
    @property
    def height(self) -> float:
        return self.y_max - self.y_min
    
    @property
    def area(self) -> float:
        return self.width * self.height
    
    def is_valid(self, min_size: int = 1) -> bool:
        """Check if box has valid dimensions"""
        return (self.width >= min_size and 
                self.height >= min_size and
                self.x_min >= 0 and self.y_min >= 0)


class BoxUtils:
    """Utility functions for bounding box operations"""
    
    @staticmethod
    def get_class_color(class_id: int, color_cache: Dict = None) -> Tuple[int, int, int]:
        """Get consistent color for class ID"""
        if class_id is None:
            return (255, 0, 0)
        
        if color_cache and class_id in color_cache:
            return color_cache[class_id]
        
        try:
            h = ((class_id - 1) * 137) % 360 / 360.0
            r, g, b = colorsys.hsv_to_rgb(h, 0.7, 1.0)
            color = (int(r*255), int(g*255), int(b*255))
            
            if color_cache is not None:
                color_cache[class_id] = color
                
            return color
        except:
            return (255, 0, 0)
    
    @staticmethod
    def yolo_to_pixel(box: List[float], img_width: int, img_height: int) -> BoundingBox:
        """Convert YOLO format to pixel coordinates"""
        cls, cx, cy, w, h = box
        x_center = cx * img_width
        y_center = cy * img_height
        box_width = w * img_width
        box_height = h * img_height
        
        return BoundingBox(
            class_id=int(cls),
            x_min=int(x_center - box_width / 2),
            y_min=int(y_center - box_height / 2),
            x_max=int(x_center + box_width / 2),
            y_max=int(y_center + box_height / 2)
        )
    
    @staticmethod
    def pixel_to_yolo(box: BoundingBox, img_width: int, img_height: int) -> List[float]:
        """Convert pixel coordinates to YOLO format"""
        x_center = (box.x_min + box.x_max) / 2 / img_width
        y_center = (box.y_min + box.y_max) / 2 / img_height
        width = (box.x_max - box.x_min) / img_width
        height = (box.y_max - box.y_min) / img_height
        
        return [box.class_id, x_center, y_center, width, height]
    
    # ADD THIS MISSING METHOD:
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> BoundingBox:
        """Create BoundingBox from dictionary - wrapper for BoundingBox.from_dict"""
        return BoundingBox.from_dict(data)
