import os
import re
from pathlib import Path
from datetime import datetime

# Configuration
BLOG_DIR = r"c:\Users\OlgaKorniichuk\Documents\antiGravity Projects\Facebok AI.corelogic\blog"
POSTS_DIR = os.path.join(BLOG_DIR, "posts")
ASSETS_DIR = os.path.join(BLOG_DIR, "assets")

CATEGORIES = {
    "Automation": ["automation", "agent", "bot", "workflow", "efficiency", "robot", "process", "audit", "scale", "autonomous"],
    "Logistics": ["logistics", "supply chain", "dispatch", "route", "fleet", "transport", "shipping", "delivery", "warehouse", "freight", "cargo"],
    "Intelligence": ["intelligence", "analysis", "insight", "strategy", "decision", "logic", "reasoning", "future", "trend", "market", "finance", "stock", "investment"],
    "Tech Stack": ["python", "api", "database", "code", "dev", "sql", "javascript", "framework", "library", "github", "server", "backend", "frontend", "software", "platform", "tool", "tech", "tutorial", "guide", "build"]
}

def get_posts():
    """Reads all HTML posts and extracts metadata"""
    posts = []
    for filepath in sorted(Path(POSTS_DIR).glob("*.html"), reverse=True):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Extract metadata...
        # Use DOTALL to match titles traversing multiple lines
        title_match = re.search(r'<title>(.*?) \|', content, re.DOTALL)
        if title_match:
            title = title_match.group(1).strip().replace('\n', ' ')
            # Collapse multiple spaces
            title = re.sub(r'\s+', ' ', title)
        else:
            title = filepath.stem
        
        # Image Extraction Strategy (Fallback Logic)
        image_url = ""
        
        # 1. Try Open Graph Image (Most Reliable)
        og_match = re.search(r'<meta property="og:image" content="(.*?)"', content)
        if og_match:
            image_url = og_match.group(1)
        
        # 2. Try CSS Background (Standard Generator)
        if not image_url:
            css_match = re.search(r"background(?:-image)?: url\(['\"]?(.*?)['\"]?\)", content)
            if css_match:
                image_url = css_match.group(1)
                
        # 3. Try First Image Tag (Legacy/Migrated Posts) - Ignore logo/assets
        if not image_url:
            img_matches = re.finditer(r'<img [^>]*src=["\'](.*?)["\']', content)
            for m in img_matches:
                src = m.group(1)
                # Skip assets, logos, icons
                if "assets/" not in src and "logo" not in src.lower() and "icon" not in src.lower():
                    image_url = src
                    break
        
        date_match = re.search(r'<span class="date">(.*?)</span>', content)
        date = date_match.group(1) if date_match else ""
        
        snippet_match = re.search(r'<p class="article-snippet">(.*?)</p>', content)
        snippet = snippet_match.group(1) if snippet_match else ""
        
        # Determine Category Score using Regex (Whole Words)
        cat_scores = {cat: 0 for cat in CATEGORIES}
        lower_content = content.lower()
        
        for cat, keywords in CATEGORIES.items():
            for kw in keywords:
                # Use regex to find whole words only
                matches = re.findall(r'\b' + re.escape(kw) + r'\b', lower_content)
                cat_scores[cat] += len(matches)
        
        # Priority Logic with Thresholds
        best_cat = "Intelligence"
        
        # 1. Logistics (Nichest)
        if cat_scores["Logistics"] >= 2:
            best_cat = "Logistics"
        # 2. Tech Stack (Specific) - Promoted above Automation
        elif cat_scores["Tech Stack"] >= 2:
            best_cat = "Tech Stack"
        # 3. Automation (Core Theme)
        elif cat_scores["Automation"] >= 2:
            best_cat = "Automation"
        # 4. Intelligence (Broadest/Default)
        else:
            best_cat = "Intelligence"
            
        posts.append({
            "filename": filepath.name,
            "title": title,
            "image_url": image_url,
            "date": date,
            "snippet": snippet,
            "category": best_cat,
            "path": f"posts/{filepath.name}"
        })
    return posts

def generate_page(filename, posts, active_filter, page_title):
    """Generates an HTML page based on the index.html template"""
    
    # Read template (index.html)
    with open(os.path.join(BLOG_DIR, "index.html"), "r", encoding="utf-8") as f:
        template = f.read()
        
    # 1. Update Navigation (Remove Join Community, Add About Us)
    nav_replacement = """
        <div class="header-right">
            <a href="about.html" class="nav-link" style="color: #94A3B8; text-decoration: none; font-weight: 500; transition: color 0.2s;">About Us</a>
        </div>
    """
    # Replace existing header-right div
    template = re.sub(r'<div class="header-right">.*?</div>', nav_replacement, template, flags=re.DOTALL)
    
    # 2. Update Filter Bar Links & Active State
    
    # First, strip any existing "active" classes
    template = re.sub(r'class="active"', '', template)
    
    # Ensure "All" link points to index.html (handle various spacing)
    template = re.sub(r'<a href="#"\s*>All</a>', '<a href="index.html">All</a>', template)
    
    # Ensure other category links are correct (if they were reset to #)
    template = template.replace('<a href="#">Automation</a>', '<a href="automation.html">Automation</a>')
    template = template.replace('<a href="#">Logistics</a>', '<a href="logistics.html">Logistics</a>')
    template = template.replace('<a href="#">Intelligence</a>', '<a href="intelligence.html">Intelligence</a>')
    template = template.replace('<a href="#">Tech Stack</a>', '<a href="tech-stack.html">Tech Stack</a>')

    # Now set the new active class
    if active_filter == "All":
        template = template.replace('<a href="index.html">All</a>', '<a href="index.html" class="active">All</a>')
    else:
        # Use regex to safely find the link and add class
        # (simpler string replace might fail if attributes are reordered, but for now exact match is likely fine if we just generated it)
        template = template.replace(f'<a href="{filename}">{active_filter}</a>', f'<a href="{filename}" class="active">{active_filter}</a>')
    
    # 3. Generate Post Grid
    
    # Available Local Assets (Generic Tech/AI visuals)
    LOCAL_ASSETS = [
        "assets/photo_2026-02-06_16-51-45.jpg",
        "assets/photo_2026-02-06_16-51-47.jpg",
        "assets/photo_2026-02-06_16-51-50.jpg",
        "assets/photo_2026-02-06_16-51-52.jpg",
        "assets/photo_2026-02-06_16-51-54.jpg",
        "assets/photo_2026-02-06_16-51-57.jpg",
        "assets/photo_2026-02-06_16-51-59.jpg",
        "assets/photo_2026-02-06_16-52-02.jpg",
        "assets/photo_2026-02-06_16-52-04.jpg",
        "assets/photo_2026-02-06_16-52-07.jpg",
        "assets/photo_2026-02-06_16-52-09.jpg",
        "assets/photo_2026-02-06_16-52-17.jpg"
    ]
    
    # Manual Overrides (Filename -> Specific Asset)
    IMAGE_OVERRIDES = {
        # Musk - Swapping from 54 (Our Team) to 17 (Generic Dark/Market)
        "2026-02-10-why-has-elon-musk-merged-his-rocket-company-with-h.html": "assets/photo_2026-02-06_16-52-17.jpg",
        # US Software Stocks - Using 47
        "2026-02-10-us-software-stocks-tumble-sparks-concerns-that-ai-.html": "assets/photo_2026-02-06_16-51-47.jpg",
    }

    posts_html = ""
    for post in posts:
        bg_image = ""
        
        # 1. Check Manual Overrides First
        if post['filename'] in IMAGE_OVERRIDES:
            bg_image = IMAGE_OVERRIDES[post['filename']]
        else:
            # 2. Use Extracted Image if valid
            bg_image = post['image_url']
        
        # 3. Validation: Check for broken providers
        if bg_image and ("via.placeholder.com" in bg_image or "pollinations.ai" in bg_image):
            bg_image = "" 

        # 4. Resolve relative paths
        if bg_image and bg_image.startswith("../assets/"):
            bg_image = bg_image.replace("../assets/", "assets/")
            
        # 5. Fallback: If still empty, deterministically assign a local asset
        if not bg_image:
             # Use hash of title to pick a consistent random image from LOCAL_ASSETS
             # This ensures the same post always gets the same image, but different posts get different images
             asset_index = hash(post['title']) % len(LOCAL_ASSETS)
             bg_image = LOCAL_ASSETS[asset_index]
             
        print(f"Post: {post['filename']} | Image: {bg_image}") # DEBUG

        posts_html += f"""
        <article class="article-card">
            <div class="card-image-placeholder" style="background-image: url('{bg_image}');">
                <span class="category-pill">{post['category']}</span>
            </div>
            <div class="card-content">
                <h2><a href="{post['path']}">{post['title']}</a></h2>
                <p class="article-snippet">{post['snippet']}</p>
                <div class="card-meta">
                    <span class="date">{post['date']}</span>
                    <a href="{post['path']}" class="read-more-btn"></a>
                </div>
            </div>
        </article>
        """
        
    # Replace Main Content
    template = re.sub(r'<main id="news-feed">.*?</main>', f'<main id="news-feed">{posts_html}</main>', template, flags=re.DOTALL)
    
    # Write File
    with open(os.path.join(BLOG_DIR, filename), "w", encoding="utf-8") as f:
        f.write(template)
    print(f"Generated {filename} with {len(posts)} posts")

def generate_about_page():
    """Generates the About Us page"""
    
    content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Us | AI Core Logic</title>
    <link rel="stylesheet" href="css/style.css?v=6">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        .about-container { max-width: 800px; margin: 0 auto; padding: 4rem 2rem; }
        .about-hero { text-align: center; margin-bottom: 4rem; }
        .about-hero h1 { font-size: 3.5rem; background: linear-gradient(to right, #fff, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; }
        .mission-box { background: rgba(0, 240, 255, 0.05); border-left: 4px solid #00F0FF; padding: 2rem; border-radius: 8px; margin: 3rem 0; }
        .contact-form { background: #0F1419; padding: 2.5rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-top: 4rem; }
        .form-group { margin-bottom: 1.5rem; }
        .form-group label { display: block; color: #94A3B8; margin-bottom: 0.5rem; font-size: 0.9rem; }
        .form-control { width: 100%; padding: 1rem; background: #050507; border: 1px solid rgba(255,255,255,0.1); color: #fff; border-radius: 6px; font-family: 'Outfit'; transition: border-color 0.2s; }
        .form-control:focus { outline: none; border-color: #00F0FF; }
        textarea.form-control { min-height: 150px; resize: vertical; }
        .submit-btn { width: 100%; background: #00F0FF; color: #000; font-weight: 700; padding: 1rem; border: none; border-radius: 6px; cursor: pointer; transition: transform 0.2s; font-size: 1.1rem; }
        .submit-btn:hover { transform: scale(1.02); }
    </style>
</head>
<body>

    <header>
        <div class="nav-left">
            <a href="index.html" class="logo-link" style="display: flex; align-items: center; gap: 10px; text-decoration: none;">
                <img src="assets/brand-logo.png" alt="AI Core Logic" style="height: 40px; border-radius: 4px;">
                <span style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.5rem; color: #F8FAFC;">AI.CORE <span style="color: #00F0FF;">LOGIC</span></span>
            </a>
        </div>
        <div class="header-right">
             <a href="index.html" class="nav-link" style="color: #94A3B8; text-decoration: none; font-weight: 500;">Home</a>
        </div>
    </header>

    <main class="about-container">
        <div class="about-hero">
            <h1>Logic Over Hype.</h1>
            <p style="font-size: 1.25rem; color: #94A3B8;">We build the systems that build the future.</p>
        </div>

        <div class="article-body" style="font-size: 1.15rem; line-height: 1.8; color: #CBD5E1;">
            <p>At <strong>AI Core Logic</strong>, we believe that Artificial Intelligence isn't magic—it's engineering. While the world chases the latest shiny chatbot, we are focused on the infrastructure of autonomy.</p>
            
            <p>Our roots are in <strong>Logistics</strong> and <strong>High-Scale Automation</strong>. We know what happens when systems break, and we know exactly how to build them so they don't.</p>

            <div class="mission-box">
                <h3 style="color: #00F0FF; margin-top: 0;">Our Mission</h3>
                <p style="margin-bottom: 0;">To demystify AI for modern businesses and provide the architectural logic needed to scale without chaos. We don't just write about code; we deploy it.</p>
            </div>

            <h2>Why Us?</h2>
            <p>We combine deep technical expertise in <strong>Python, Cloud Architecture, and LLM Orchestration</strong> with real-world business strategy. We translate "AI buzzwords" into "Bottom-line results".</p>
        </div>

        <!-- Contact Section -->
        <div class="contact-form" id="contact">
            <h2 style="color: #fff; margin-top: 0; margin-bottom: 0.5rem;">Partner With Us</h2>
            <p style="color: #94A3B8; margin-bottom: 2rem;">Ready to optimize your logic? Tell us what you're building.</p>
            
            <!-- Formspree Integration -->
            <form action="https://formspree.io/f/xbdadegq" method="POST">
                
                <!-- Anti-spam honeypot (hidden) -->
                <input type="text" name="_gotcha" style="display:none">
                
                <!-- Success redirect (optional, or rely on Formspree default) -->
                <!-- <input type="hidden" name="_next" value="https://aicorelogic-ops.github.io/ai-core-logic/thanks.html"> -->

                <div class="form-group">
                    <label>Name</label>
                    <input type="text" name="name" class="form-control" placeholder="Jane Doe" required>
                </div>
                
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" name="email" class="form-control" placeholder="jane@company.com" required>
                </div>
                
                <div class="form-group">
                    <label>Computed Needs (How can we help?)</label>
                    <textarea name="message" class="form-control" placeholder="I need to automate my dispatch workflow..." required></textarea>
                </div>
                
                <button type="submit" class="submit-btn" style="background: #00F0FF; color: #000; font-weight: 700; border: none; padding: 1rem; border-radius: 6px; cursor: pointer; width: 100%;">Schedule Consulting Appointment</button>
            </form>
        </div>
    </main>

    <footer>
        <div class="footer-big-text">AI.Core Logic</div>
        <p>&copy; 2026 AI Core Logic. Integrating Intelligence.</p>
    </footer>

    <script src="js/search.js"></script>
</body>
</html>"""
    
    with open(os.path.join(BLOG_DIR, "about.html"), "w", encoding="utf-8") as f:
        f.write(content)
    print("Generated about.html")

def main():
    print("Starting Logic Core Expansion...")
    
    # 1. Parse all posts
    all_posts = get_posts()
    print(f"Parsed {len(all_posts)} posts")
    
    # 2. Filter posts by category
    cat_posts = {cat: [] for cat in CATEGORIES}
    for post in all_posts:
        cat_posts[post['category']].append(post)
        
    print(f"   - Automation: {len(cat_posts['Automation'])}")
    print(f"   - Logistics: {len(cat_posts['Logistics'])}")
    print(f"   - Intelligence: {len(cat_posts['Intelligence'])}")
    print(f"   - Tech Stack: {len(cat_posts['Tech Stack'])}")
    
    # 3. Generate Category Pages
    generate_page("automation.html", cat_posts['Automation'], "Automation", "Automation & Efficiency")
    generate_page("logistics.html", cat_posts['Logistics'], "Logistics", "Logistics & Supply Chain")
    generate_page("intelligence.html", cat_posts['Intelligence'], "Intelligence", "Business Intelligence")
    generate_page("tech-stack.html", cat_posts['Tech Stack'], "Tech Stack", "Engineering & Code")
    
    # 4. Update Index (All Posts)
    generate_page("index.html", all_posts, "All", "Business Intelligence")
    
    # 5. Generate About Page
    generate_about_page()

if __name__ == "__main__":
    main()
