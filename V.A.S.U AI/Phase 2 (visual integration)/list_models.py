import google.generativeai as genai
from config.settings import Settings

try:
    settings = Settings()
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    print(f"🔑 Checking available models for key ending in ...{settings.GEMINI_API_KEY[-5:]}")
    
    print("\n--- AVAILABLE MODELS ---")
    count = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ {m.name}")
            count += 1
            
    if count == 0:
        print("❌ No text-generation models found. Check your API Key permissions.")
    else:
        print(f"\n✨ Found {count} models available for use.")

except Exception as e:
    print(f"❌ Error: {e}")