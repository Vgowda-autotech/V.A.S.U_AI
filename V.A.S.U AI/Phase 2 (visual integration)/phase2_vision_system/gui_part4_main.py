import sys
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QTextEdit
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap, QFont
from config.settings import Settings
from phase2_vision_system.vision_manager import VisionManager

class ModernHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.vision_manager = VisionManager(self.settings)
        
        self.setWindowTitle("V.A.S.U - VISION SYSTEMS")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #0d0d0d; color: #00ffcc;")

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Header
        self.header = QLabel("👁️ V.A.S.U INTEGRATED VISION SYSTEM")
        self.header.setFont(QFont("Consolas", 20, QFont.Weight.Bold))
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.header)

        # Video Feed Label
        self.video_label = QLabel("Initializing Camera...")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("border: 2px solid #00ffcc; background: #000;")
        self.video_label.setMinimumSize(640, 480)
        layout.addWidget(self.video_label)

        # Logs
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMaximumHeight(150)
        self.log_box.setStyleSheet("border: 1px solid #005544; font-family: Consolas;")
        layout.addWidget(self.log_box)

        # Start System
        self.log("Initializing core systems...")
        if self.vision_manager.start_vision_system():
            self.log("Vision System: ONLINE")
            self.log("Camera Feed: ACQUIRED")
        else:
            self.log("CRITICAL ERROR: Camera initialization failed!")

        # Timer for updating UI
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def log(self, message):
        self.log_box.append(f">> {message}")

    def update_frame(self):
        frame = self.vision_manager.get_frame()
        detections = self.vision_manager.get_detections()
        
        if frame is not None:
            # Draw detections (Mock HUD overlay)
            for (label, conf, (x, y, w, h)) in detections:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 204), 2)
                cv2.putText(frame, f"{label} {int(conf*100)}%", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 204), 2)

            # Convert to Qt Format
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
                self.video_label.width(), self.video_label.height(), 
                Qt.AspectRatioMode.KeepAspectRatio))

    def closeEvent(self, event):
        self.vision_manager.stop_vision_system()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = ModernHUD()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()