import sys
import cv2
import threading
import time
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QTextEdit, QHBoxLayout)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QThread
from PyQt6.QtGui import QImage, QPixmap, QFont

# Import Project Settings
from config.settings import Settings
from phase2_vision_system.vision_manager import VisionManager

# --- Voice Worker Thread ---
class VoiceWorker(QThread):
    text_received = pyqtSignal(str, str) # type (User/AI), message
    status_update = pyqtSignal(str)      # Listening/Processing/etc
    
    def __init__(self, settings, vision_manager):
        super().__init__()
        self.settings = settings
        self.vision_manager = vision_manager 
        self.is_running = True
        self.voice_manager = None
        self.command_processor = None

    def run(self):
        self.status_update.emit("Initializing Audio...")
        try:
            from phase1_voice_interface.voice_manager import VoiceManager
            from phase1_voice_interface.command_processor import CommandProcessor
            
            self.voice_manager = VoiceManager(self.settings)
            
            # Pass vision manager to command processor
            self.command_processor = CommandProcessor(self.settings, self.vision_manager)
            
            # Init Mic
            if hasattr(self.voice_manager, 'initialize'):
                self.voice_manager.initialize()

            self.text_received.emit("System", "Voice Systems Online.")
            
            # ========================================================
            # 🔔 WELCOME PROTOCOL (The New Addition)
            # ========================================================
            welcome_message = "Welcome back, Boss. All systems are online and ready."
            self.text_received.emit("VASU", welcome_message)
            self.status_update.emit("Speaking...")
            if hasattr(self.voice_manager, 'speak'):
                self.voice_manager.speak(welcome_message)
            # ========================================================
            
            # Main Loop
            while self.is_running:
                self.status_update.emit("Listening...")
                
                if hasattr(self.voice_manager, 'listen'):
                    command = self.voice_manager.listen() 
                else:
                    time.sleep(1)
                    command = None
                
                if command:
                    self.status_update.emit("Processing...")
                    self.text_received.emit("User", command)
                    
                    response = self.command_processor.process_command(command)
                    if response:
                        self.text_received.emit("VASU", response)
                        self.status_update.emit("Speaking...")
                        if hasattr(self.voice_manager, 'speak'):
                            self.voice_manager.speak(response)
                
                time.sleep(0.1)

        except Exception as e:
            self.text_received.emit("Error", str(e))

    def stop(self):
        self.is_running = False
        self.wait()

# --- Main GUI Class ---
class IntegratedHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        
        # Initialize Core Managers
        self.vision_manager = VisionManager(self.settings)
        
        # UI Setup
        self.setWindowTitle("V.A.S.U - PHASE 3 INTEGRATION")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #0d0d0d; color: #00ffcc;")

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- LEFT PANEL: CAMERA FEED ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.header = QLabel("👁️ V.A.S.U VISION FEED")
        self.header.setFont(QFont("Consolas", 16, QFont.Weight.Bold))
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.header)

        self.video_label = QLabel("Initializing Camera...")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("border: 2px solid #00ffcc; background: #000;")
        self.video_label.setMinimumSize(640, 480)
        left_layout.addWidget(self.video_label)
        
        self.info_label = QLabel("Waiting for analysis...")
        self.info_label.setFont(QFont("Consolas", 10))
        self.info_label.setStyleSheet("color: #aaaaaa;")
        left_layout.addWidget(self.info_label)
        
        main_layout.addWidget(left_panel, stretch=2)

        # --- RIGHT PANEL: AI INTERFACE ---
        right_panel = QWidget()
        right_panel.setStyleSheet("border-left: 1px solid #333; background-color: #111;")
        right_layout = QVBoxLayout(right_panel)

        self.status_label = QLabel("SYSTEM INITIALIZING")
        self.status_label.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("background-color: #003333; padding: 10px; border-radius: 5px;")
        right_layout.addWidget(self.status_label)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("border: none; font-family: Consolas; font-size: 14px; padding: 10px;")
        right_layout.addWidget(self.log_box)

        main_layout.addWidget(right_panel, stretch=1)

        # Start Vision System
        if self.vision_manager.start_vision_system():
            self.log("System", "Vision System: ONLINE")
        else:
            self.log("System", "CRITICAL: Vision System Failed")

        # Start Voice Thread
        self.voice_thread = VoiceWorker(self.settings, self.vision_manager)
        self.voice_thread.text_received.connect(self.log)
        self.voice_thread.status_update.connect(self.update_status)
        self.voice_thread.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def log(self, sender, message):
        color = "#00ffcc"
        if sender == "User": color = "#ffffff"
        elif sender == "Error": color = "#ff3333"
        timestamp = datetime.now().strftime("%H:%M:%S")
        html = f'<div style="margin-bottom: 5px;"><span style="color: #666;">[{timestamp}]</span> <b style="color: {color}">{sender}:</b> {message}</div>'
        self.log_box.append(html)
        self.log_box.verticalScrollBar().setValue(self.log_box.verticalScrollBar().maximum())

    def update_status(self, status):
        self.status_label.setText(status.upper())
        if "Listening" in status:
            self.status_label.setStyleSheet("background-color: #004400; color: #fff; padding: 10px;")
        elif "Speaking" in status:
            self.status_label.setStyleSheet("background-color: #000044; color: #aaf; padding: 10px;")
        else:
            self.status_label.setStyleSheet("background-color: #003333; color: #0fc; padding: 10px;")

    def update_frame(self):
        frame = self.vision_manager.get_frame()
        detections = self.vision_manager.get_detections()
        
        if frame is not None:
            label_text = ""
            for (label, conf, (x, y, w, h)) in detections:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 204), 2)
                label_str = f"{label} {int(conf*100)}%"
                (tw, th), _ = cv2.getTextSize(label_str, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                cv2.rectangle(frame, (x, y-20), (x+tw, y), (0, 255, 204), -1)
                cv2.putText(frame, label_str, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                label_text += f"• {label} ({int(conf*100)}%)  "

            if label_text: self.info_label.setText(label_text)
            else: self.info_label.setText("Scanning area...")

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
                self.video_label.width(), self.video_label.height(), Qt.AspectRatioMode.KeepAspectRatio))

    def closeEvent(self, event):
        self.vision_manager.stop_vision_system()
        self.voice_thread.stop()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = IntegratedHUD()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()