import sys
import cv2
import threading
import time
import random
import numpy as np
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QTextEdit, QHBoxLayout, QGraphicsDropShadowEffect, QFrame)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QThread, QRectF
from PyQt6.QtGui import QImage, QPixmap, QFont, QColor, QPainter, QBrush, QPen

# Import Project Settings
from config.settings import Settings
from phase2_vision_system.vision_manager import VisionManager

# ==========================================
# 🎨 CUSTOM WIDGET: AUDIO VISUALIZER
# ==========================================
class TechVisualizer(QWidget):
    """A sci-fi style audio visualizer bar graph."""
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(40)
        self.bars = 20
        self.values = [10] * self.bars
        self.state = "IDLE" # IDLE, LISTENING, SPEAKING
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(50) # Fast update

    def set_state(self, state):
        self.state = state

    def animate(self):
        # Generate random heights based on state
        for i in range(self.bars):
            if self.state == "IDLE":
                target = random.randint(5, 15)
            elif self.state == "LISTENING":
                target = random.randint(10, 80) # High activity
            elif self.state == "SPEAKING":
                target = random.randint(20, 60) # Medium activity
            else:
                target = 5
            
            # Smooth interpolation
            self.values[i] = self.values[i] * 0.7 + target * 0.3
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        bar_w = w / self.bars
        
        # Draw bars
        for i in range(self.bars):
            bar_h = (self.values[i] / 100) * h
            
            # Color based on state
            if self.state == "LISTENING":
                color = QColor(0, 255, 0) # Green
            elif self.state == "SPEAKING":
                color = QColor(0, 255, 255) # Cyan
            else:
                color = QColor(0, 100, 100) # Dim Cyan
                
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            
            rect = QRectF(i * bar_w + 2, h - bar_h, bar_w - 4, bar_h)
            painter.drawRoundedRect(rect, 2, 2)


# ==========================================
# 🎤 VOICE WORKER (With Welcome Protocol)
# ==========================================
class VoiceWorker(QThread):
    text_received = pyqtSignal(str, str) 
    status_update = pyqtSignal(str)      
    
    def __init__(self, settings, vision_manager):
        super().__init__()
        self.settings = settings
        self.vision_manager = vision_manager 
        self.is_running = True

    def run(self):
        self.status_update.emit("Initializing...")
        try:
            from phase1_voice_interface.voice_manager import VoiceManager
            from phase1_voice_interface.command_processor import CommandProcessor
            
            self.voice_manager = VoiceManager(self.settings)
            self.command_processor = CommandProcessor(self.settings, self.vision_manager)
            
            if hasattr(self.voice_manager, 'initialize'):
                self.voice_manager.initialize()

            self.text_received.emit("System", "Voice Systems Online.")
            
            # 🔔 WELCOME PROTOCOL
            # ========================================================
            welcome_msg = "Welcome back, Boss. Visual and Audio systems are online."
            self.text_received.emit("VASU", welcome_msg)
            self.status_update.emit("Speaking")
            if hasattr(self.voice_manager, 'speak'):
                self.voice_manager.speak(welcome_msg)
            # ========================================================
            
            while self.is_running:
                self.status_update.emit("Listening")
                
                if hasattr(self.voice_manager, 'listen'):
                    command = self.voice_manager.listen() 
                else:
                    time.sleep(1)
                    command = None
                
                if command:
                    self.status_update.emit("Processing")
                    self.text_received.emit("User", command)
                    
                    response = self.command_processor.process_command(command)
                    if response:
                        self.text_received.emit("VASU", response)
                        self.status_update.emit("Speaking")
                        if hasattr(self.voice_manager, 'speak'):
                            self.voice_manager.speak(response)
                else:
                     self.status_update.emit("Idle")
                
                time.sleep(0.1)

        except Exception as e:
            self.text_received.emit("Error", str(e))

    def stop(self):
        self.is_running = False
        self.wait()


# ==========================================
# 🖥️ MAIN GUI (Futuristic Style)
# ==========================================
class FuturisticHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.vision_manager = VisionManager(self.settings)
        
        # Scanning Animation Variables
        self.scan_y = 0
        self.scan_direction = 1
        
        # Window Setup
        self.setWindowTitle("V.A.S.U - MK.III INTERFACE")
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet("""
            QMainWindow { background-color: #050505; }
            QLabel { color: #00ffcc; font-family: Consolas; }
            QTextEdit { 
                background-color: #0a0a0a; 
                color: #00ffcc; 
                border: 1px solid #004444;
                font-family: Consolas;
            }
        """)

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- LEFT PANEL (VISION) ---
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #000; border: 2px solid #004444; border-radius: 10px;")
        
        # Add Glow Effect
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setColor(QColor(0, 255, 204, 100)) # Cyan glow
        glow.setOffset(0, 0)
        left_panel.setGraphicsEffect(glow)
        
        left_layout = QVBoxLayout(left_panel)
        
        self.header = QLabel("👁️ VISION FEED // LIVE")
        self.header.setFont(QFont("Consolas", 14, QFont.Weight.Bold))
        self.header.setStyleSheet("border: none; color: #00ffcc;")
        left_layout.addWidget(self.header)

        self.video_label = QLabel("INITIALIZING OPTICAL SENSORS...")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("border: 1px dashed #00ffcc; background: #000;")
        self.video_label.setMinimumSize(640, 480)
        left_layout.addWidget(self.video_label)
        
        self.info_label = QLabel("STATUS: SCANNING...")
        self.info_label.setStyleSheet("border: none; color: #008888; font-size: 10pt;")
        left_layout.addWidget(self.info_label)
        
        main_layout.addWidget(left_panel, stretch=2)

        # --- RIGHT PANEL (DATA) ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Audio Visualizer
        self.visualizer = TechVisualizer()
        right_layout.addWidget(self.visualizer)

        # Status Label
        self.status_label = QLabel("SYSTEM ONLINE")
        self.status_label.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            background-color: #001111; 
            color: #00ffcc; 
            padding: 10px; 
            border: 1px solid #00ffcc;
            border-radius: 5px;
        """)
        
        # Status Glow
        status_glow = QGraphicsDropShadowEffect()
        status_glow.setBlurRadius(15)
        status_glow.setColor(QColor(0, 255, 204, 80))
        self.status_label.setGraphicsEffect(status_glow)
        
        right_layout.addWidget(self.status_label)

        # Chat Log
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        right_layout.addWidget(self.log_box)

        main_layout.addWidget(right_panel, stretch=1)

        # Start Threads
        self.vision_manager.start_vision_system()
        
        self.voice_thread = VoiceWorker(self.settings, self.vision_manager)
        self.voice_thread.text_received.connect(self.log)
        self.voice_thread.status_update.connect(self.update_status)
        self.voice_thread.start()

        # Frame Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def log(self, sender, message):
        color = "#00ffcc"
        if sender == "User": color = "#ffffff"
        elif sender == "Error": color = "#ff3333"
        timestamp = datetime.now().strftime("%H:%M:%S")
        html = f'<div style="margin-bottom: 5px;"><span style="color: #444;">[{timestamp}]</span> <b style="color: {color}">{sender}:</b> {message}</div>'
        self.log_box.append(html)
        self.log_box.verticalScrollBar().setValue(self.log_box.verticalScrollBar().maximum())

    def update_status(self, status):
        self.status_label.setText(status.upper())
        state = status.upper()
        
        # Update Visualizer
        if "LISTENING" in state:
            self.visualizer.set_state("LISTENING")
            self.status_label.setStyleSheet("border: 1px solid #00ff00; color: #00ff00; background: #001100;")
        elif "SPEAKING" in state:
            self.visualizer.set_state("SPEAKING")
            self.status_label.setStyleSheet("border: 1px solid #00ffff; color: #00ffff; background: #001111;")
        else:
            self.visualizer.set_state("IDLE")
            self.status_label.setStyleSheet("border: 1px solid #005555; color: #005555; background: #000;")

    def update_frame(self):
        frame = self.vision_manager.get_frame()
        detections = self.vision_manager.get_detections()
        
        if frame is not None:
            # 1. Get correct dimensions
            h, w, ch = frame.shape
            
            # --- DRAW SCANNING LINE (ANIMATION) ---
            self.scan_y += 5 * self.scan_direction
            if self.scan_y >= h: self.scan_y = 0
            cv2.line(frame, (0, self.scan_y), (w, self.scan_y), (255, 255, 0), 2)
            
            # --- DRAW DETECTIONS ---
            label_text = ""
            for (label, conf, (x, y, bw, bh)) in detections:
                color = (255, 255, 0) # Cyan
                d = 20 # Corner length
                
                # Fancy Corners
                # Top-Left
                cv2.line(frame, (x, y), (x+d, y), color, 2)
                cv2.line(frame, (x, y), (x, y+d), color, 2)
                # Top-Right
                cv2.line(frame, (x+bw, y), (x+bw-d, y), color, 2)
                cv2.line(frame, (x+bw, y), (x+bw, y+d), color, 2)
                # Bottom-Left
                cv2.line(frame, (x, y+bh), (x+d, y+bh), color, 2)
                cv2.line(frame, (x, y+bh), (x, y+bh-d), color, 2)
                # Bottom-Right
                cv2.line(frame, (x+bw, y+bh), (x+bw-d, y+bh), color, 2)
                cv2.line(frame, (x+bw, y+bh), (x+bw, y+bh-d), color, 2)

                cv2.putText(frame, f"{label.upper()} {int(conf*100)}%", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                
                label_text += f"[{label}] "

            if label_text: self.info_label.setText(f"DETECTED: {label_text}")
            else: self.info_label.setText("STATUS: SCANNING...")

            # --- CONVERT TO QT IMAGE (FIXED) ---
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w # Fixes the slanted video issue
            
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            
            self.video_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
                self.video_label.width(), self.video_label.height(), Qt.AspectRatioMode.KeepAspectRatio))

    def closeEvent(self, event):
        self.vision_manager.stop_vision_system()
        self.voice_thread.stop()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = FuturisticHUD()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()