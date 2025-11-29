# V.A.S.U. - Virtual Autonomous System Utility 🤖👁️

> **"A Multimodal AI Assistant integrating Computer Vision, Voice Interaction, and Generative AI."**

![V.A.S.U. Interface](data/images/demo_screenshot.jpg)
*(Note: Replace this image path with a real screenshot of your futuristic HUD!)*

## 📖 Overview

**V.A.S.U.** is a sophisticated AI assistant inspired by Iron Man's JARVIS. Unlike standard chatbots, V.A.S.U. has "eyes" and "ears." It perceives the real world through a webcam, listens to voice commands, and uses a Large Language Model (Google Gemini) to provide context-aware responses.

It features a custom-built **Futuristic HUD (Heads-Up Display)** that renders real-time telemetry, scanning animations, and audio visualization.

## ✨ Key Features

### 👁️ Computer Vision System
* **Real-Time Detection:** Uses **YOLOv4-Tiny** to identify 80+ distinct objects (people, electronics, vehicles) at 30 FPS.
* **Visual Context:** Can answer questions based on what it sees (e.g., *"What can I do with this object?"*).
* **Scanning UI:** Features a dynamic laser-scan animation and neon-styled bounding boxes.

### 🧠 Advanced AI Brain
* **Google Gemini Integration:** Powered by the `gemini-1.5-flash` model for intelligent, witty, and concise responses.
* **Persona:** programmed with a specific system prompt to act as a professional, loyal assistant.

### 🎤 Voice Interface
* **Asynchronous Listening:** Listens for wake words and commands without freezing the video feed.
* **Text-to-Speech:** Responds verbally using an offline TTS engine for low latency.

### 🖥️ Futuristic GUI
* **PyQt6 Architecture:** A responsive, multithreaded interface.
* **Audio Visualizer:** Dynamic bar graph that reacts to system states (Listening vs. Speaking).
* **Live Telemetry:** Scrolling logs and status indicators.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Vision:** OpenCV, NumPy
* **AI/LLM:** Google Generative AI SDK (Gemini)
* **GUI:** PyQt6 (Qt for Python)
* **Voice:** SpeechRecognition, pyttsx3, PyAudio

---

## 🚀 Installation Guide

### 1. Clone the Repository
```bash
git clone [https://github.com/Vgowda-autotech/VASU.git]

cd VASU



**AUTHOR**
**Vasudev Jinnagara Guruprasad (www.linkedin.com/in/vasudev-jinnagara-guruprasad-29511a398)**
