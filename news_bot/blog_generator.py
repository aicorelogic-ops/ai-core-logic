import os
from datetime import datetime

BLOG_DIR = "blog"
POSTS_DIR = os.path.join(BLOG_DIR, "posts")

# Ensure posts directory exists
os.makedirs(POSTS_DIR, exist_ok=True)

import urllib.parse

class BlogGenerator:
    def create_post(self, title, content_html, original_link, image_url=None):
        """
        Creates a new HTML file for the blog post.
        Uses original image if available, else generates one based on title + content keywords.
        """
        # Create a safe filename
        safe_title = "".join([c if c.isalnum() else "-" for c in title]).lower()
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-{safe_title[:30]}.html"
        filepath = os.path.join(POSTS_DIR, filename)
        
        
        # VIRAL IMAGE GENERATION - Pattern Interrupt Strategy
        # Extract the "Bleeding Neck" problem or shocking detail from title
        image_hook = title[:60] if len(title) <= 60 else title.split(':')[0][:60]
        
        # Apply Direct Response Marketer Framework for Scroll-Stopping Visuals
        import random
        
        # Option A: "Raw Native" / Leaked Evidence (UGC Style)
        raw_native = (
            f"iPhone photo amateur candid shot, first-person POV perspective, "
            f"computer screen showing shocking data about '{image_hook}', "
            f"messy desk with papers and coffee cup, "
            f"RED CIRCLE hand-drawn around key detail, RED ARROW pointing to problem, "
            f"harsh office lighting, grainy quality, user-generated content aesthetic, "
            f"flash photography, NOT professional, NOT stock photo, leaked evidence style"
        )
        
        # Option B: "Breaking News" (Viral News Chyron)
        breaking_news = (
            f"Breaking news TV screenshot style, person looking genuinely SHOCKED or TERRIFIED, "
            f"holding document with '{image_hook}' visible, "
            f"news chyron banner at bottom saying 'BREAKING NEWS' or 'EXPOSED', "
            f"TMZ style viral news aesthetic, candid amateur photo, "
            f"harsh flash lighting, NOT cinematic, NOT studio quality, "
            f"dimly lit background, real reaction not posed, grainy iPhone quality"
        )
        
        # Option C: The "Weird" / "Gross" Visual (Confusion Trigger)
        weird_visual = (
            f"Close-up macro photo of weird unexpected detail about '{image_hook}', "
            f"magnified mistake or strange contradiction, confusing composition, "
            f"makes viewer ask 'what the hell is that?', "
            f"amateur photography, grainy texture, harsh lighting, "
            f"NOT aesthetically pleasing, pattern interrupt visual, "
            f"user-generated content style, candid first-person POV"
        )
        
        # Randomly select one framework for variety
        chosen_style = random.choice([raw_native, breaking_news, weird_visual])
        
        safe_prompt = urllib.parse.quote(chosen_style)
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1200&height=630&nologo=true"
        
        # Calculate reading time (~200 words per minute)
        word_count = len(urllib.parse.unquote(content_html).split())
        reading_time = max(1, round(word_count / 200))
        
        # HTML Template for individual post (High Readability Spec)
        post_html = f"""
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
            {datetime.now().strftime('%B %d, %Y')} &bull; ⏱️ {reading_time} min read
        </div>
        
        <h1 style="font-family: 'Outfit', sans-serif; font-size: 4rem; line-height: 1.1; margin-bottom: 2rem; font-weight: 700; color: #F8FAFC;">{title}</h1>
        
        <!-- Hero Image -->
        <img src="{image_url}" alt="Hero Image" style="width: 100%; border-radius: 12px; margin-bottom: 3rem; box-shadow: 0 10px 40px rgba(0,0,0,0.5);">

        <!-- Quick Summary Box (High Readability Spec) -->
        <div class="quick-summary">
            <strong>TL;DR:</strong> 
            <p>Our deep analysis of this development reveals critical shifts in the AI landscape. We've distilled the noise into the absolute essentials you need to know to stay ahead.</p>
        </div>

        <div class="article-body" style="font-family: 'Verdana', sans-serif; font-size: 20px; line-height: 1.8; color: #CBD5E1;">
            {content_html}
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
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(post_html)
            
        print(f"✅ Blog post created: {filepath}")
        return filename

    def update_index(self, title, summary, filename, image_url=None):
        """
        Injects the new post into the top of index.html using the new Forest Design.
        """
        index_path = os.path.join(BLOG_DIR, "index.html")
        
        if not image_url:
            # Generate 'Native Card' Image - raw, attention-grabbing thumbnail
            safe_prompt = urllib.parse.quote(f"Raw smartphone photo about {title}, authentic native social media style, high contrast, pattern interrupt visual, attention-grabbing composition, mint green accent")
            image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=600&height=400&nologo=true"

        # New Forest-Style Card HTML
        new_entry = f"""
        <article class="article-card">
            <div class="card-image-placeholder" style="background-image: url('{image_url}');">
                <span class="category-pill">AI Update</span>
            </div>
            <div class="card-content">
                <h2><a href="posts/{filename}">{title}</a></h2>
                <p class="article-snippet">{summary}...</p>
                <div class="card-meta">
                    <span class="date">{datetime.now().strftime('%b %d')}</span>
                    <a href="posts/{filename}" class="read-more-btn"></a>
                </div>
            </div>
        </article>
        """
        
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 🛑 Prevention: Check if this file is already linked in the index
            if f'href="posts/{filename}"' in content:
                print(f"⏭️ Skipping index update: {filename} already exists in index.html")
                return
            
            # Find the injection point (after <main id="news-feed">)
            # We look for the comment or the opening tag
            marker = '<main id="news-feed">'
            if marker in content:
                updated_content = content.replace(marker, marker + "\n" + new_entry)
                
                with open(index_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print(f"✅ Index.html updated with new Image Card: {filename}")
            else:
                print("❌ Could not find injection marker in index.html")
                
        except Exception as e:
            print(f"❌ Error updating index: {e}")

    def deploy_to_github(self):
        """
        Commits and pushes the new changes to GitHub so the link becomes live.
        """
        import subprocess
        
        print("☁️ Auto-Deploying to GitHub...")
        try:
            # 1. Add changes
            subprocess.run(["C:\\Program Files\\Git\\cmd\\git.exe", "add", "."], check=True)
            
            # 2. Commit
            try:
                subprocess.run(["C:\\Program Files\\Git\\cmd\\git.exe", "commit", "-m", "Auto-publish new article"], check=True)
            except subprocess.CalledProcessError:
                print("⚠️ Nothing to commit (files already exist). Proceeding to push...")
            
            # 3. Push
            # Note: This relies on your cached credentials.
            subprocess.run(["C:\\Program Files\\Git\\cmd\\git.exe", "push"], check=True)
            
            print("✅ Successfully deployed to https://aicorelogic-ops.github.io/ai-core-logic/")
            return True
        except Exception as e:
            print(f"❌ Deploy failed: {e}")
            return False

if __name__ == "__main__":
    # Test Run
    gen = BlogGenerator()
    # New Test Article for Facebook Verification
    title = "The Rise of Autonomous Business Agents"
    content = """
    <p>Imagine a world where your software doesn't just wait for your input, but proactively manages your business logic. 
    <strong>Autonomous Agents</strong> are the next evolution of AI, capable of negotiating, scheduling, and optimizing workflows 24/7.</p>
    <p>In this post, we explore how AI Core Logic is pioneering the use of these agents to reduce operational overhead by up to 40%.</p>
    """
    fname = gen.create_post(title, content, "https://example.com/agents")
    gen.update_index(title, "Why 2026 is the year of the Autonomous Agent.", fname)
    
    # Deploy to live site
    gen.deploy_to_github()
