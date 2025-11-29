import google.generativeai as genai
from utils.logger import get_logger

logger = get_logger(__name__)

class AIInterface:
    def __init__(self, settings):
        self.settings = settings
        self.model = None
        
        # Initialize Google Gemini Client
        try:
            # We specifically look for GEMINI_API_KEY now
            if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
                logger.info("Connected to Google Gemini Cloud.")
            else:
                logger.warning("No Google API Key found in settings.")
        except Exception as e:
            logger.error(f"Failed to connect to Google AI: {e}")

    def get_response(self, user_text, visual_context=None):
        """
        Sends text + visual context to Google Gemini.
        """
        if not self.model:
            return "I am unable to access the cloud brain. Please check your API key."

        try:
            # 1. Construct the Prompt with Context
            full_prompt = f"{self.settings.SYSTEM_PROMPT}\n\n"
            
            if visual_context and visual_context != "Nothing specific.":
                full_prompt += f"[SYSTEM DATA: Camera detects: {visual_context}]\n"
            
            full_prompt += f"User: {user_text}"

            # 2. Call Gemini
            response = self.model.generate_content(full_prompt)
            
            # 3. Extract Answer safely
            if response and response.text:
                return response.text.strip().replace("\n", " ")
            return "I received an empty response from the network."

        except Exception as e:
            logger.error(f"Gemini Error: {e}")
            return "I am having trouble connecting to the neural network."