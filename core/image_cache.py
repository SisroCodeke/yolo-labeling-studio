# core/image_cache.py
"""
Image caching system for performance optimization
"""

from collections import deque
from typing import Optional, Any, Deque, Dict


class ImageCache:
    """Optimized image caching system using LRU (Least Recently Used) strategy"""
    
    def __init__(self, max_size: int = 5):
        """
        Initialize the image cache
        
        Args:
            max_size: Maximum number of images to keep in cache
        """
        self.max_size = max_size
        self.cache: Dict[str, Any] = {}  # Stores key -> image data
        self.access_order: Deque[str] = deque()  # Tracks usage order
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get an image from cache
        
        Args:
            key: Cache key (usually file path)
            
        Returns:
            Cached image data or None if not found
        """
        if key in self.cache:
            # Move to end (most recently used)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def put(self, key: str, value: Any):
        """
        Store an image in cache
        
        Args:
            key: Cache key (usually file path)
            value: Image data to cache
        """
        if key in self.cache:
            # Update existing: move to end
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_size:
            # Remove least recently used item
            oldest = self.access_order.popleft()
            del self.cache[oldest]
        
        # Add new item
        self.cache[key] = value
        self.access_order.append(key)
    
    def clear(self):
        """Clear all cached images"""
        self.cache.clear()
        self.access_order.clear()
    
    def __len__(self) -> int:
        """Return number of cached images"""
        return len(self.cache)
    
    def __contains__(self, key: str) -> bool:
        """Check if key is in cache"""
        return key in self.cache
