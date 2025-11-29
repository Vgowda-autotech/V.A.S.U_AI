from datetime import datetime
from .ai_interface import AIInterface
from utils.logger import get_logger

logger = get_logger(__name__)

class CommandProcessor:
    def __init__(self, settings, vision_manager=None):
        self.settings = settings
        self.ai = AIInterface(settings)
        self.vision_manager = vision_manager
        self.user_name = "Sir" # Default name for memory feature

    def process_command(self, command):
        """Decide what to do with the text."""
        if not command:
            return None
            
        logger.info(f"Processing: {command}")
        command = command.lower()

        # --- 1. MEMORY & IDENTITY (For Demos) ---
        if "my name is" in command:
            # Extract name (simple split)
            name = command.split("is")[-1].strip()
            self.user_name = name
            return f"Protocol updated. I will address you as {name}."

        elif "who am i" in command:
            return f"You are {self.user_name}, the authorized administrator of this system."
            
        elif "who are you" in command:
            return "I am VASU, your virtual autonomous system utility."

        # --- 2. SYSTEM COMMANDS ---
        elif "time" in command:
            return f"The time is {datetime.now().strftime('%H:%M')}."
            
        elif "date" in command:
            return f"Today is {datetime.now().strftime('%A, %B %d')}."
            
        elif "terminate" in command or "exit" in command:
            return "Shutting down systems."

        # --- 3. VISION & AI CONTEXT PREPARATION ---
        # We prepare the 'visual_context' to send to ChatGPT
        visual_context = "Nothing specific."
        if self.vision_manager:
            detections = self.vision_manager.get_detections()
            if detections:
                # Get unique labels (e.g., ['person', 'bottle'])
                labels = [d[0] for d in detections]
                unique_labels = list(set(labels))
                visual_context = ", ".join(unique_labels)

        # --- 4. VISION SPECIFIC QUERY ---
        # If user explicitly asks what is in front, we answer directly using vision data
        if "what is this" in command or "what do you see" in command:
            if visual_context != "Nothing specific.":
                return f"I see {visual_context}."
            else:
                return "I am looking, but I do not see any specific objects right now."

        # --- 5. ADVANCED AI (ChatGPT) ---
        # Send the command AND the visual context to the AI
        return self.ai.get_response(command, visual_context)