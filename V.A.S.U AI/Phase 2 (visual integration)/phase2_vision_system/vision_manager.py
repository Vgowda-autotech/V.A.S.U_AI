import threading
import time
import cv2
from .camera_manager import CameraManager
from .object_detector import ObjectDetector
from .scene_analyzer import SceneAnalyzer

class VisionManager:
    def __init__(self, settings):
        self.settings = settings
        self.camera = CameraManager()
        self.detector = ObjectDetector()
        self.analyzer = SceneAnalyzer()
        self.is_active = False
        self.current_frame = None
        self.latest_detections = []
        self.lock = threading.Lock()
        self.thread = None
        self.stop_event = threading.Event()

    def start_vision_system(self):
        if not self.camera.initialize():
            return False
        self.detector.initialize()
        self.is_active = True
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._process_loop, daemon=True)
        self.thread.start()
        return True

    def stop_vision_system(self):
        self.stop_event.set()
        self.is_active = False
        if self.thread:
            self.thread.join()
        self.camera.release()

    def _process_loop(self):
        while not self.stop_event.is_set():
            frame = self.camera.get_frame()
            if frame is not None:
                # Run detection
                detections = self.detector.detect_objects(frame)
                with self.lock:
                    self.current_frame = frame
                    self.latest_detections = detections
            time.sleep(0.03) # ~30 FPS

    def get_frame(self):
        with self.lock:
            if self.current_frame is not None:
                return self.current_frame.copy()
        return None
    
    def get_detections(self):
        with self.lock:
            return self.latest_detections

    def get_status(self):
        return {"active": self.is_active}