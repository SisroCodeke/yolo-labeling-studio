# core/ai_predictor.py
"""
YOLOv8-based AI pre-labeling predictor
"""
import logging
from typing import List, Dict, Optional
import numpy as np
import cv2

# Lazy import to avoid hard dependency unless enabled
try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False

from models.bounding_box import BoundingBox
from config.config_manager import load_config


logger = logging.getLogger("AIPredictor")

class AIPredictor:
    def __init__(self):
        self.config = load_config()
        self.model = None
        self.class_names = self.config["ai_assistant"]["class_names_coco"]
        self.enabled_classes = set(self.config["ai_assistant"]["enabled_classes"])
        self._initialized = False

    def initialize(self):
        """Initialize YOLOv8 model (lazy loading)"""
        if not ULTRALYTICS_AVAILABLE:
            logger.error("ultralytics not installed. Install with: pip install ultralytics")
            return False

        if self._initialized:
            return True

        try:
            model_path = self.config["ai_assistant"]["model_path"]
            logger.info(f"Loading YOLOv8 model from: {model_path}")
            self.model = YOLO(model_path)  # Auto-downloads if missing
            self._initialized = True
            logger.info("YOLOv8 model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to load YOLOv8 model: {e}")
            return False

    def predict(self, image: np.ndarray) -> List[Dict]:
        """
        Run inference and return list of box dicts compatible with app
        Returns: [{'class_id': int, 'x_min': int, ...}, ...]
        """
        if not self._initialized and not self.initialize():
            return []

        if self.model is None:
            return []

        try:
            conf = self.config["ai_assistant"]["confidence_threshold"]
            iou = self.config["ai_assistant"]["iou_threshold"]

            results = self.model(
                image,
                conf=conf,
                iou=iou,
                classes=list(self.enabled_classes) if self.enabled_classes else None,
                verbose=False
            )

            boxes = []
            for r in results:
                if r.boxes is None:
                    continue
                for box in r.boxes:
                    cls_id = int(box.cls.item())
                    if cls_id not in self.enabled_classes:
                        continue

                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    # Clamp to image bounds
                    h, w = image.shape[:2]
                    x1 = max(0, min(x1, w))
                    y1 = max(0, min(y1, h))
                    x2 = max(0, min(x2, w))
                    y2 = max(0, min(y2, h))

                    if x2 <= x1 or y2 <= y1:
                        continue

                    boxes.append({
                        'class_id': cls_id,
                        'x_min': x1,
                        'y_min': y1,
                        'x_max': x2,
                        'y_max': y2
                    })
            logger.info(f"AI predicted {len(boxes)} boxes")
            return boxes
        except Exception as e:
            logger.error(f"Error during AI prediction: {e}", exc_info=True)
            return []
