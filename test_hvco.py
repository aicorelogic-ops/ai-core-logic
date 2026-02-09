from generate_hvco import ARTICLES, SYSTEM_PROMPT
import google.generativeai as genai
import os
from dotenv import load_dotenv
from news_bot.publisher import FacebookPublisher
from news_bot.blog_generator import BlogGenerator
import urllib.parse

load_dotenv("news_bot/.env")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('models/gemini-2.0-flash')

def test_single():
    article = ARTICLES[0] # Death of Middle Manager
    print(f"🧪 Testing: {article['title']}")
    
    try:
        print("1. Generating Blog Content...")
        res = model.generate_content(f"{SYSTEM_PROMPT}\n\nTASK:\n{article['prompt']}")
        print(f"✅ Blog Content Length: {len(res.text)}")
        
        print("2. Generating Social Copy...")
        res_s = model.generate_content(f"{SYSTEM_PROMPT}\n\nTASK:\n{article['social_prompt']}")
        print(f"✅ Social Copy Length: {len(res_s.text)}")
        print(f"Social Copy Snippet: {res_s.text[:100]}...")

        print("3. Generating Image URL...")
        screaming_prompt = urllib.parse.quote(f"Bold high-impact editorial illustration: {article['title']}. Vibrant neon colors, high contrast, dramatic shadows, futuristic digital art style, ultra-detailed, 8k, attention-grabbing composition")
        image_url = f"https://image.pollinations.ai/prompt/{screaming_prompt}?width=1200&height=630&nologo=true"
        print(f"✅ Image URL: {image_url}")

        print("4. Posting to Facebook...")
        fb = FacebookPublisher()
        fb.post_photo(photo_url=image_url, message=res_s.text + "\n\nRead more: https://aicorelogic.com")

    except Exception as e:
        print(f"❌ Test Failed: {e}")

if __name__ == "__main__":
    test_single()
