import os
import re
from pathlib import Path

BLOG_DIR = r"c:\Users\OlgaKorniichuk\Documents\antiGravity Projects\Facebok AI.corelogic\blog"
POSTS_DIR = os.path.join(BLOG_DIR, "posts")

# NEW THEMATIC ASSETS
THEME_ASSETS = {
    "Logistics": "assets/theme_logistics.png",
    "Automation": "assets/theme_automation.png",
    "Intelligence": "assets/theme_intelligence.png",
    "Tech Stack": "assets/theme_techstack.png",
    "Finance": "assets/theme_finance.png",
    "Office": "assets/theme_office.png"
}

def get_theme_image(title, category):
    title_lower = title.lower()
    
    # Priority Keyword Matching
    if "stock" in title_lower or "market" in title_lower or "finance" in title_lower or "money" in title_lower or "investment" in title_lower:
        return THEME_ASSETS["Finance"]
    
    if "manager" in title_lower or "corporate" in title_lower or "business" in title_lower or "office" in title_lower or "job" in title_lower:
        return THEME_ASSETS["Office"]
        
    if "code" in title_lower or "python" in title_lower or "api" in title_lower or "tech" in title_lower or "software" in title_lower:
        return THEME_ASSETS["Tech Stack"]

    if "robot" in title_lower or "agent" in title_lower or "musk" in title_lower or "rocket" in title_lower:
        return THEME_ASSETS["Automation"]

    if "logistics" in title_lower or "supply chain" in title_lower or "shipping" in title_lower:
        return THEME_ASSETS["Logistics"]
        
    # Category Fallback
    if category in THEME_ASSETS:
        return THEME_ASSETS[category]
        
    return THEME_ASSETS["Intelligence"]

def update_posts():
    print("Updating individual blog posts...")
    files = sorted(Path(POSTS_DIR).glob("*.html"))
    
    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract Title for context
        title_match = re.search(r'<title>(.*?) \|', content, re.DOTALL)
        title = title_match.group(1).strip() if title_match else filepath.stem

        # Extract Category (Simple approximation)
        category = "Intelligence"
        if "Logistics" in content: category = "Logistics"
        elif "Automation" in content: category = "Automation"
        elif "Tech" in content: category = "Tech Stack"
        
        # Determine New Image
        new_image = get_theme_image(title, category)
        # Fix path for inside /posts/ directory (needs ../)
        relative_image_path = "../" + new_image

        # Regex to replace background-image
        # Pattern: background-image: url('...');
        # We want to be careful not to break other styles
        
        # Look for the hero header style
        # <header class="article-hero" style="background-image: url('...');">
        
        pattern = r'(class="article-hero"[^>]*style="[^"]*background-image:\s*url\([\'"]?)(.*?)([\'"]?\))'
        
        def replacer(match):
            prefix = match.group(1)
            old_url = match.group(2)
            suffix = match.group(3)
            return f"{prefix}{relative_image_path}{suffix}"

        new_content = re.sub(pattern, replacer, content)
        
        # Also fix Og:Image if present
        og_pattern = r'(<meta property="og:image" content=")(.*?)(")'
        new_content = re.sub(og_pattern, lambda m: f'{m.group(1)}{relative_image_path}{m.group(3)}', new_content)

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {filepath.name} -> {new_image}")
        else:
            print(f"No changes matched for {filepath.name}")

if __name__ == "__main__":
    update_posts()
