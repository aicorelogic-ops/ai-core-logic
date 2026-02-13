import requests
import os
from dotenv import load_dotenv

# Load params
load_dotenv("news_bot/.env")
PAGE_ID = os.getenv("FB_PAGE_ID")
TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

if not PAGE_ID or not TOKEN:
    print("❌ Missing params")
    exit(1)

# 1. Download Image
image_url = "https://image.pollinations.ai/prompt/test_image_corporate_office?width=800&height=600&nologo=true&model=flux"
print(f"Downloading from: {image_url}")

response = requests.get(image_url)
if response.status_code != 200:
    print(f"❌ Download failed: {response.status_code}")
    exit(1)

content = response.content
print(f"✅ Downloaded {len(content)} bytes")

# 2. Upload to Facebook
url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/photos"

files = {
    'source': ('test_image.jpg', content, 'image/jpeg')
}
data = {
    "caption": "Debug Test Post - Please Ignore 🛠️",
    "published": "true"
}
params = {
    "access_token": TOKEN
}

print("Posting to Facebook...")
try:
    resp = requests.post(url, files=files, data=data, params=params)
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.text}")
except Exception as e:
    print(f"Exception: {e}")
