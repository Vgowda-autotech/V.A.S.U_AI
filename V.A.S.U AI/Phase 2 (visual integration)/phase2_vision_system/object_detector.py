import cv2
import numpy as np
from pathlib import Path
from config.settings import Settings
from utils.logger import get_logger

logger = get_logger(__name__)

class ObjectDetector:
    def __init__(self):
        self.settings = Settings()
        self.net = None
        self.classes = []
        self.output_layers = []
        self.is_initialized = False

    def initialize(self):
        try:
            # check if files exist
            if not Path(self.settings.YOLO_WEIGHTS).exists():
                logger.error(f"Model weights not found: {self.settings.YOLO_WEIGHTS}")
                logger.error("Please run setup_models.py first!")
                return False

            # Load Class Names
            with open(self.settings.YOLO_CLASSES, "r") as f:
                self.classes = [line.strip() for line in f.readlines()]

            # Load YOLO Network
            self.net = cv2.dnn.readNet(
                str(self.settings.YOLO_WEIGHTS), 
                str(self.settings.YOLO_CONFIG)
            )
            
            # Use CPU (change to CUDA if you have an NVIDIA GPU setup)
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            
            # Get Output Layers
            layer_names = self.net.getLayerNames()
            self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
            
            self.is_initialized = True
            logger.info("Object Detector (YOLOv4-Tiny) initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to init Object Detector: {e}")
            return False

    def detect_objects(self, frame):
        if not self.is_initialized or frame is None:
            return []

        height, width, channels = frame.shape
        
        # Create Blob from Image (Preprocessing)
        # 1/255 scales pixels to 0-1 range. (416, 416) is standard YOLO input size.
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        
        # Run Forward Pass
        outs = self.net.forward(self.output_layers)

        class_ids = []
        confidences = []
        boxes = []

        # Process detections
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > self.settings.CONFIDENCE_THRESHOLD:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Apply Non-Maximum Suppression (removes overlapping boxes)
        indexes = cv2.dnn.NMSBoxes(
            boxes, confidences, 
            self.settings.CONFIDENCE_THRESHOLD, 
            self.settings.NMS_THRESHOLD
        )

        results = []
        if len(indexes) > 0:
            for i in indexes.flatten():
                label = str(self.classes[class_ids[i]])
                conf = confidences[i]
                box = boxes[i]
                results.append((label, conf, box))

        return results
        
    def get_detector_status(self):
        return {
            "is_initialized": self.is_initialized, 
            "model": "YOLOv4-Tiny",
            "classes_loaded": len(self.classes)
        }