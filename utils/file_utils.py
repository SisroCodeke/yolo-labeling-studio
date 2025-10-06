"""
File utilities for image and label file operations
"""

import os
import glob
import shutil
from typing import List, Optional, Tuple
import cv2


class FileUtils:
    """Utilities for file operations"""
    
    @staticmethod
    def find_image_files(directory: str) -> List[str]:
        """Find all image files in directory"""
        if not os.path.exists(directory):
            return []
            
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif']
        image_files = []
        
        for ext in extensions:
            pattern = os.path.join(directory, ext)
            image_files.extend(glob.glob(pattern))
            # Also check uppercase extensions
            pattern = os.path.join(directory, ext.upper())
            image_files.extend(glob.glob(pattern))
        
        return sorted(image_files)
    
    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Ensure directory exists, create if not"""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_label_path(image_path: str, label_dir: str) -> str:
        """Get corresponding label file path for image"""
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        return os.path.join(label_dir, image_name + ".txt")
    
    @staticmethod
    def load_image_with_caching(path: str, cache: Optional[dict] = None) -> Optional[any]:
        """Load image with optional caching"""
        if cache is not None and path in cache:
            return cache[path]
        
        if not os.path.exists(path):
            return None
            
        image = cv2.imread(path)
        if image is not None and cache is not None:
            cache[path] = image
            
        return image
    
    @staticmethod
    def move_to_processed_dir(source_path: str, 
                            processed_dir: str, 
                            create_subdirs: bool = True) -> Tuple[Optional[str], Optional[str]]:
        """
        Move file to processed directory
        
        Returns:
            Tuple of (new_image_path, new_label_path) or (None, None) on error
        """
        try:
            if create_subdirs:
                images_dir = os.path.join(processed_dir, 'images')
                labels_dir = os.path.join(processed_dir, 'labels')
                FileUtils.ensure_directory(images_dir)
                FileUtils.ensure_directory(labels_dir)
            else:
                images_dir = processed_dir
                labels_dir = processed_dir
            
            filename = os.path.basename(source_path)
            new_image_path = os.path.join(images_dir, filename)
            
            # Move image file
            if os.path.exists(source_path):
                shutil.move(source_path, new_image_path)
            
            # Determine label path
            label_name = os.path.splitext(filename)[0] + ".txt"
            source_dir = os.path.dirname(source_path)
            source_label_path = os.path.join(source_dir, label_name)
            new_label_path = os.path.join(labels_dir, label_name)
            
            # Move label file if exists
            if os.path.exists(source_label_path):
                shutil.move(source_label_path, new_label_path)
            
            return new_image_path, new_label_path
            
        except Exception as e:
            print(f"Error moving file to processed directory: {e}")
            return None, None
    
    @staticmethod
    def is_valid_image_file(path: str) -> bool:
        """Check if file is a valid image file"""
        if not os.path.isfile(path):
            return False
            
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        ext = os.path.splitext(path)[1].lower()
        return ext in valid_extensions
