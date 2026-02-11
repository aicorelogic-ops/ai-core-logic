import google.generativeai as genai
from news_bot.settings import GOOGLE_API_KEY
import os

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

genai.configure(api_key=GOOGLE_API_KEY)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Name: {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
