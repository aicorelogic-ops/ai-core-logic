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
        
        # Image Logic: Use Original OR Generate AI
        if not image_url:
            # Create a more descriptive prompt using the title
            # We add "visual representation" to ensure it's not text-heavy
            safe_prompt = urllib.parse.quote(f"editorial illustration for news article: {title}. cyberpunk style, neon, data visualization, minimalist, 3d render, high quality, 8k, dark blue and mint green palette")
            image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1200&height=600&nologo=true"
        
        # HTML Template for individual post (Updated with Hero Image)
        post_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | AI Core Logic</title>
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
            # Generate AI Image URL for the Card (Smaller)
            safe_prompt = urllib.parse.quote(f"minimalist abstract icon for {title}, dark background, mint green, high tech, 3d render")
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
    # Create a realistic test article to see the AI image generation in action
    title = "The Dawn of Autonomous Logistics"
    content = """
    <p>Artificial Intelligence is no longer just a buzzword; it is the backbone of modern supply chains. 
    From predictive analytics to autonomous delivery drones, logic-driven systems are reshaping how we move goods.</p>
    <p>In this test of our new <strong>Visual Engine</strong>, we are demonstrating how AI can automatically 
    visualize the context of an article and generate a relevant header image without human intervention.</p>
    """
    fname = gen.create_post(title, content, "https://example.com")
    gen.update_index(title, "How AI is reshaping modern supply chains with logic-driven systems", fname)
    
    # Deploy to live site
    gen.deploy_to_github()
