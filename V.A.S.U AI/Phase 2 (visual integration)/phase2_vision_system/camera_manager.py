import cv2
from utils.logger import get_logger

logger = get_logger(__name__)

class CameraManager:
    def __init__(self):
        self.cap = None
        self.is_initialized = False

    def initialize(self):
        try:
            self.cap = cv2.VideoCapture(0) # Index 0 is usually default webcam
            if not self.cap.isOpened():
                logger.error("Could not open video device")
                return False
            
            # Set resolution
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.is_initialized = True
            return True
        except Exception as e:
            logger.error(f"Camera init failed: {e}")
            return False

    def get_frame(self):
        if self.is_initialized and self.cap:
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def release(self):
        if self.cap:
            self.cap.release()
        self.is_initialized = False

    def get_status(self):
        return {"is_initialized": self.is_initialized}