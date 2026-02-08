import os
from dotenv import load_dotenv

load_dotenv()

# Facebook Config
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")

# AI Config
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# News Sources (RSS)
# News Sources (RSS)
RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/", # Enterprise & Business AI
    "https://www.wired.com/feed/category/ai/latest/rss",
]

# Filtering keywords
KEYWORDS = ["automation", "productivity", "efficiency", "small business", "AI tool", "software", "generative ai", "startup"]
