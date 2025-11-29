import speech_recognition as sr
import pyttsx3
from utils.logger import get_logger

logger = get_logger(__name__)

class VoiceManager:
    def __init__(self, settings):
        self.settings = settings
        self.recognizer = sr.Recognizer()
        self.microphone = None
        # We do NOT init the engine here to avoid threading locks
        self.is_initialized = False

    def initialize(self):
        try:
            # Only init the microphone here
            try:
                self.microphone = sr.Microphone()
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            except Exception as e:
                logger.warning(f"Microphone setup issue: {e}")
                
            self.is_initialized = True
            return True
        except Exception as e:
            logger.error(f"Voice Manager Init Failed: {e}")
            return False

    def listen(self):
        """Listens for a single command."""
        if not self.microphone:
            return None

        try:
            with self.microphone as source:
                # Reduced timeout for snappier GUI
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
            
            try:
                text = self.recognizer.recognize_google(audio)
                return text.lower()
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                return None
        except Exception:
            return None

    def speak(self, text):
        """
        Speak text using a fresh engine instance to prevent 
        PyQt thread lockups on Windows.
        """
        if not text:
            return
            
        try:
            # Re-initialize engine locally for thread safety
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)
            engine.setProperty('volume', 1.0)
            
            # Queue and play
            engine.say(text)
            engine.runAndWait()
            
            # Explicitly cleanup
            engine.stop()
            del engine
        except Exception as e:
            logger.error(f"TTS Error: {e}")