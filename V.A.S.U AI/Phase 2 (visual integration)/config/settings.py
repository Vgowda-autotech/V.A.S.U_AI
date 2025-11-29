import os
from pathlib import Path

class Settings:
    def __init__(self):
        # ==========================================
        # 📂 BASE DIRECTORIES
        # ==========================================
        # Calculate the root folder of the project
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        
        # Define sub-directories
        self.DATA_DIR = self.BASE_DIR / "data"
        self.MODELS_DIR = self.BASE_DIR / "models"
        self.LOGS_DIR = self.BASE_DIR / "logs"
        self.FACES_DIR = self.DATA_DIR / "faces"
        self.IMAGES_DIR = self.DATA_DIR / "images"

        # Create directories if they don't exist
        for directory in [self.DATA_DIR, self.MODELS_DIR, self.LOGS_DIR, self.FACES_DIR, self.IMAGES_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

        # ==========================================
        # 📷 CAMERA SETTINGS
        # ==========================================
        self.CAMERA_INDEX = 0      # 0 is usually the default webcam
        self.FRAME_WIDTH = 640     # Lower resolution = faster processing
        self.FRAME_HEIGHT = 480
        self.FPS = 30

        # ==========================================
        # 👁️ VISION SYSTEM (YOLOv4-Tiny)
        # ==========================================
        self.YOLO_CONFIG = self.MODELS_DIR / "yolov4-tiny.cfg"
        self.YOLO_WEIGHTS = self.MODELS_DIR / "yolov4-tiny.weights"
        self.YOLO_CLASSES = self.MODELS_DIR / "coco.names"
        
        # Detection Thresholds
        self.CONFIDENCE_THRESHOLD = 0.5  # Minimum probability (50%) to show a box
        self.NMS_THRESHOLD = 0.4         # Lower value = less overlapping boxes

        # Face Recognition Data Path
        self.FACE_ENCODINGS_FILE = self.FACES_DIR / "encodings.pickle"

        # ==========================================
        # 🎤 VOICE & AUDIO SETTINGS
        # ==========================================
        # Text-to-Speech (TTS)
        self.SPEECH_RATE = 170     # Speed of talking (default is ~200)
        self.SPEECH_VOLUME = 1.0   # Volume (0.0 to 1.0)
        
        # Speech Recognition
        self.ENERGY_THRESHOLD = 300  # Adjust for background noise (higher = less sensitive)
        self.PAUSE_THRESHOLD = 0.8   # Seconds of silence before processing

        # ==========================================
        # 🧠 ARTIFICIAL INTELLIGENCE (Google Gemini)
        # ==========================================
        # Paste your Google API Key inside the quotes below
        self.GEMINI_API_KEY = "Write_your_API_Key_here" 
        
        # Model Selection ('gemini-1.5-flash' is fast and ideal for assistants)
        self.GEMINI_MODEL = "gemini-2.5-pro"
        
        # System Persona (Instructions for how VASU should act)
        self.SYSTEM_PROMPT = (
            "You are V.A.S.U, a futuristic AI assistant inspired by JARVIS. "
            "Your responses should be concise, professional, and slightly witty. "
            "Do not give long lectures; keep answers short for voice output."
        )

        # ==========================================
        # 🎨 GUI APPEARANCE
        # ==========================================
        self.THEME_COLOR = "#00ffcc"  # Cyan/Teal (Iron Man HUD style)
        self.BG_COLOR = "#0d0d0d"     # Almost Black
        self.TEXT_COLOR = "#ffffff"   # White

        self.ERROR_COLOR = "#ff3333"  # Red
