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
        
        
        # ALWAYS generate custom scroll-stopping image with TEXT OVERLAY
        # Extract a hook from the title for the image (first 60 chars or shocking part)
        image_hook = title[:60] if len(title) <= 60 else title.split(':')[0][:60]
        
        # Add aggressive visual tactics like the copywriting
        import random
        image_styles = [
            # Style 1: Bold Text Shock
            f"Bold text overlay on dark background: '{image_hook.upper()}', "
            f"fire emoji 🔥, warning symbol ⚠️, high contrast neon colors, "
            f"viral social media post aesthetic, attention-grabbing typography",
            
            # Style 2: Alert/Breaking News
            f"Smartphone notification screenshot style: 🚨 ALERT banner, "
            f"text: '{image_hook}', red and black color scheme, "
            f"breaking news aesthetic, high urgency visual",
            
            # Style 3: Stat Shock
            f"Bold statistics typography on gradient background about {title}, "
            f"large numbers, percentage symbols, dollar signs, "
            f"neon accent colors, viral content style, pattern interrupt visual"
        ]
        
        chosen_style = random.choice(image_styles)
        safe_prompt = urllib.parse.quote(chosen_style)
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1200&height=630&nologo=true"
        
        # HTML Template for individual post (Updated with Hero Image)
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
    <meta property="og:url" content="https://aicorelogic-ops.github.io/ai-core-logic/blog/posts/{filename}" />

    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
<header>
    <div class="nav-left">
        <a href="../index.html" class="logo-link">
            <img src="../assets/brand-logo.png" alt="AI.Core Logic" class="logo-img">
        </a>
    </div>
    <!-- Simple Nav for Article Page -->
    <nav class="nav-center">
        <a href="../index.html">Home</a>
    </nav>
</header>

<main style="max-width: 800px; margin: 0 auto; padding: 2rem;">
    <article class="article-details">
        <div class="article-date" style="color: var(--accent-mint);">{datetime.now().strftime('%B %d, %Y')}</div>
        <h1 style="font-size: 3rem; line-height: 1.2; margin-bottom: 2rem;">{title}</h1>
        
        <!-- Hero Image -->
        <img src="{image_url}" alt="Article Image" style="width: 100%; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5); object-fit: cover;">

        <div class="article-body" style="font-size: 1.1rem; color: #e2e8f0;">
            {content_html}
        </div>
        
        <hr style="border-color: rgba(255,255,255,0.1); margin: 3rem 0;">
        <p><em>Source: <a href="{original_link}" target="_blank" style="color: var(--accent-mint);">Read original article</a></em></p>
        <br>
        <a href="../index.html" class="cta-button primary">← Back to Home</a>
    </article>
</main>

<footer>
    <p>&copy; 2026 AI Core Logic.</p>
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
            
            # Find the injection point (after <main id="news-feed">)
            # We look for the comment or the opening tag
            marker = '<main id="news-feed">'
            if marker in content:
                updated_content = content.replace(marker, marker + "\n" + new_entry)
                
                with open(index_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print("✅ Index.html updated with new Image Card.")
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
