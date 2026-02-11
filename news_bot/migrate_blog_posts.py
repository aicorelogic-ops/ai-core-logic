import os
import re
import urllib.parse
from datetime import datetime

BLOG_DIR = r"c:\Users\OlgaKorniichuk\Documents\antiGravity Projects\Facebok AI.corelogic\blog"
POSTS_DIR = os.path.join(BLOG_DIR, "posts")

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | AI Core Logic</title>
    
    <!-- Open Graph for Facebook -->
    <meta property="og:title" content="{title} | AI Core Logic" />
    <meta property="og:type" content="article" />
    <meta property="og:image" content="{image_url}" />
    <meta property="og:description" content="Read the latest analysis on AI and Logic-based business automation." />

    <link rel="stylesheet" href="../css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
<div id="scroll-progress"></div>

<header>
    <div class="nav-left">
        <a href="../index.html" class="logo-link" style="display: flex; align-items: center; gap: 10px; text-decoration: none;">
            <img src="../assets/brand-logo.png" alt="AI Core Logic" style="height: 40px; border-radius: 4px;">
            <span style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.5rem; color: #F8FAFC;">AI.CORE <span style="color: #00F0FF;">LOGIC</span></span>
        </a>
    </div>
    <nav class="nav-center">
        <a href="../index.html">Home</a>
    </nav>
</header>

<main style="max-width: 900px; margin: 0 auto; padding: 4rem 2rem;">
    <article class="article-details">
        <div class="article-meta" style="font-family: 'Space Mono', monospace; font-size: 0.85rem; color: #94A3B8; margin-bottom: 1rem;">
            {date} &bull; ⏱️ {reading_time} min read
        </div>
        
        <h1 style="font-family: 'Outfit', sans-serif; font-size: 4rem; line-height: 1.1; margin-bottom: 2rem; font-weight: 700; color: #F8FAFC;">{clean_title}</h1>
        
        <!-- Hero Image -->
        <img src="{image_url}" alt="Hero Image" style="width: 100%; border-radius: 12px; margin-bottom: 3rem; box-shadow: 0 10px 40px rgba(0,0,0,0.5);">

        <!-- Quick Summary Box (High Readability Spec) -->
        <div class="quick-summary">
            <strong>TL;DR:</strong> 
            <p>Our deep analysis of this development reveals critical shifts in the AI landscape. We've distilled the noise into the absolute essentials you need to know to stay ahead.</p>
        </div>

        <div class="article-body" style="font-family: 'Verdana', sans-serif; font-size: 20px; line-height: 1.8; color: #CBD5E1;">
            {body_content}
        </div>
        
        <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 4rem 0;">
        
        <!-- Author Bio Section -->
        <div class="author-bio" style="display: flex; gap: 1.5rem; align-items: center; background: #141B24; padding: 2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
            <div style="width: 80px; height: 80px; background: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; overflow: hidden; border: 2px solid #00F0FF; box-shadow: 0 4px 12px rgba(0, 240, 255, 0.2);">
                <img src="../assets/brand-logo.png" alt="AI Core Logic Logo" style="width: 100%; height: 100%; object-fit: contain;">
            </div>
            <div>
                <h4 style="margin: 0 0 0.5rem 0; font-family: 'Outfit', sans-serif; color: #F8FAFC;">AI Core Logic Editorial</h4>
                <p style="margin: 0; font-size: 0.9rem; color: #94A3B8;">Mastering the intersection of logistics, automation, and generative AI. We cut through the hype to find real-world business value.</p>
            </div>
        </div>

        <div style="margin-top: 4rem;">
            <a href="../index.html" class="cta-button primary">← Back to News Feed</a>
        </div>
    </article>
</main>

<script>
    // Reading Progress Bar
    window.onscroll = function() {{
        let winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        let height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        let scrolled = (winScroll / height) * 100;
        document.getElementById("scroll-progress").style.width = scrolled + "%";
    }};
</script>

<footer>
    <p>&copy; 2026 AI Core Logic. Scanned for excellence.</p>
</footer>
</body>
</html>
"""

def migrate():
    print("🚀 Starting Migration of Blog Posts...")
    files = [f for f in os.listdir(POSTS_DIR) if f.endswith(".html")]
    count = 0
    
    for filename in files:
        filepath = os.path.join(POSTS_DIR, filename)
        
        # Skip the one we just generated or already migrated
        # with open(filepath, "r", encoding="utf-8") as f:
        #     html = f.read()
            
        # if 'id="scroll-progress"' in html:
        #     print(f"  ⏭️ Skipping {filename} (Already has progress bar)")
        #     continue
        
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
            
        # Extraction logic
        try:
            # 1. Title
            title_match = re.search(r"<title>(.*?) \| AI Core Logic</title>", html)
            title = title_match.group(1) if title_match else "AI Market Update"
            clean_title = title # In case we want to strip anything extra
            
            # 2. Image
            img_match = re.search(r'property="og:image" content="(.*?)"', html)
            image_url = img_match.group(1) if img_match else "https://via.placeholder.com/1200x630"
            
            # 3. Body Content
            body_match = re.search(r'<div class="article-body"[^>]*>(.*?)</div>\s*<hr', html, re.DOTALL)
            if not body_match:
                # Fallback search if hr is missing
                body_match = re.search(r'<div class="article-body"[^>]*>(.*?)</div>', html, re.DOTALL)
            
            body_content = body_match.group(1).strip() if body_match else "Content missing."
            
            # 4. Date
            date_match = re.search(r'<div class="article-date"[^>]*>(.*?)</div>', html)
            date = date_match.group(1) if date_match else "February 10, 2026"
            
            # 5. Reading Time Calculation
            word_count = len(re.sub('<[^<]+?>', '', body_content).split())
            reading_time = max(1, round(word_count / 200))
            
            # Construct new HTML
            new_html = TEMPLATE.format(
                title=title,
                clean_title=clean_title,
                image_url=image_url,
                date=date,
                reading_time=reading_time,
                body_content=body_content
            )
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_html)
                
            print(f"  ✅ Migrated: {filename}")
            count += 1
            
        except Exception as e:
            print(f"  ❌ Error migrating {filename}: {e}")
            
    print(f"\n✨ Done! Migrated {count} posts to High-Readability design.")

if __name__ == "__main__":
    migrate()
