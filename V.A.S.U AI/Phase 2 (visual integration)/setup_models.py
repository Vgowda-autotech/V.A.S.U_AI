import os
import urllib.request
import sys
from pathlib import Path

# Define file paths
BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)

# We will use YOLOv4-Tiny because it is fast enough for CPUs
FILES = {
    "yolov4-tiny.weights": "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights",
    "yolov4-tiny.cfg": "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg",
    "coco.names": "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names"
}

def download_file(url, filename):
    file_path = MODELS_DIR / filename
    if file_path.exists():
        print(f"✅ {filename} already exists.")
        return

    print(f"⬇️ Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, str(file_path))
        print(f"✅ Downloaded {filename}")
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")

def main():
    print(f"Creating models directory at: {MODELS_DIR}")
    for filename, url in FILES.items():
        download_file(url, filename)
    print("\n🎉 All models downloaded successfully!")

if __name__ == "__main__":
    main()