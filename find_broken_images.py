import os
import re

posts_dir = r"c:\Users\OlgaKorniichuk\Documents\antiGravity Projects\Facebok AI.corelogic\blog\posts"
broken_posts = []

# Regex to find background images
bg_regex = re.compile(r"background(?:-image)?: url\(['\"]?(.*?)['\"]?\)")

print("Scanning for broken/risky image URLs...")
for filename in os.listdir(posts_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        match = bg_regex.search(content)
        if match:
            url = match.group(1)
            # Flag placeholders and Pollinations (which are timing out)
            if "via.placeholder.com" in url or "pollinations.ai" in url and "nologo=true" in url:
                broken_posts.append({
                    "file": filename,
                    "url": url,
                    "title": filename.replace(".html", "").replace("-", " ")
                })

print(f"Found {len(broken_posts)} posts with risky images:\n")
for p in broken_posts:
    print(f"File: {p['file']}")
    print(f"URL:  {p['url']}")
    print("-" * 50)
