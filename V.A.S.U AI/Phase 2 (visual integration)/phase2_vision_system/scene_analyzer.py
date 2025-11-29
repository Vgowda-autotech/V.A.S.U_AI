import numpy as np
import cv2

class SceneAnalyzer:
    def analyze_scene(self, frame):
        if frame is None:
            return {}
            
        # 1. Lighting Analysis
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        lighting_condition = "Dark"
        if brightness > 150: lighting_condition = "Bright"
        elif brightness > 80: lighting_condition = "Normal"
        
        # 2. Blur detection
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        is_blurry = laplacian_var < 100
        
        return {
            "brightness": brightness,
            "condition": lighting_condition,
            "is_blurry": is_blurry
        }