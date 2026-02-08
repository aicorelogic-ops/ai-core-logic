import google.generativeai as genai
import os
from news_bot.settings import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

print("Listing available models...")
try:
    with open("models.txt", "w") as f:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"{m.name}\n")
except Exception as e:
    with open("models.txt", "w") as f:
        f.write(f"Error: {e}")
