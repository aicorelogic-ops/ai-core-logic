import os
from datetime import datetime

BLOG_DIR = "blog"
POSTS_DIR = os.path.join(BLOG_DIR, "posts")

# Ensure posts directory exists
os.makedirs(POSTS_DIR, exist_ok=True)

import urllib.parse

class BlogGenerator:
    def __init__(self):
        self.posts_dir = POSTS_DIR

    def create_slug(self, title):
        """Creates a URL-friendly slug from the title."""
        safe_title = "".join([c if c.isalnum() or c.isspace() else "-" for c in title]).lower()
        return "-".join(safe_title.split())[:50] # Limit slug length

    def calculate_read_time(self, content):
        """Calculates estimated reading time based on content word count."""
        # Assuming content is HTML, we need to strip tags for accurate word count
        import re
        clean_content = re.sub(r'<[^>]+>', '', content)
        word_count = len(clean_content.split())
        return max(1, round(word_count / 200)) # 200 words per minute

    def create_post(self, title, content, link, image_url=None, tldr_summary=None, editorial_prospect=None):
        """
        Generates a static HTML page for the blog post.
        """
        # Create slug
        slug = self.create_slug(title)
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"{date_str}-{slug}.html"
        filepath = os.path.join(self.posts_dir, filename)
        
        # If no image provided, generate one using Viral Pattern Interrupt Strategy
        if not image_url:
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
        
        # Calculate read time
        read_time = self.calculate_read_time(content)
        
        # Prepare Editorial Prospect
        if not editorial_prospect:
            editorial_prospect = "We analyze the intersection of logistics, automation, and AI to deliver actionable insights for modern businesses. No hype, just practical strategy."
            
        editorial_bio_html = f'''
        <!-- Editorial Attribution (Brand Logo + Dynamic Prospect) -->
        <div class="author-bio" style="background: #0F1419; padding: 2rem; border-radius: 8px; border-left: 4px solid #00F0FF;">
             <div style="display: flex; align-items: flex-start; gap: 1.5rem;">
                <img src="../assets/brand-logo.png" alt="AI Core Logic" style="width: 60px; height: 60px; object-fit: contain;">
                <div>
                    <h4 style="margin: 0 0 0.5rem 0; font-family: 'Outfit', sans-serif; color: #00F0FF; font-size: 1.1rem;">AI Core Logic Editorial</h4>
                    <p style="margin: 0; font-size: 0.95rem; color: #94A3B8; line-height: 1.6; font-style: italic;">"{editorial_prospect}"</p>
                </div>
            </div>
        </div>
        '''

        # Generate HTML content
        post_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | AI Core Logic</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #00F0FF;
            --secondary: #7000FF;
            --bg: #050507;
            --surface: #0F1419;
            --text: #E2E8F0;
            --text-dim: #94A3B8;
        }}
        
        body {{
            background-color: var(--bg);
            color: var(--text);
            font-family: 'Outfit', sans-serif;
            margin: 0;
            line-height: 1.6;
        }}
        
        /* Navbar */
        nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 5%;
            background: rgba(5, 5, 7, 0.95);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 1000;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .logo {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
        }}
        
        .logo-img {{
            width: 40px;
            height: 40px;
            object-fit: contain;
        }}
        
        .logo-text {{
            font-weight: 700;
            font-size: 1.25rem;
            color: #fff;
            letter-spacing: -0.5px;
        }}
        
        .logo-text span {{ color: var(--primary); }}
        
        .nav-links a {{
            color: var(--text-dim);
            text-decoration: none;
            margin-left: 2rem;
            font-weight: 500;
            transition: color 0.2s;
        }}
        
        .nav-links a:hover {{ color: var(--primary); }}
        
        /* Hero Section */
        .article-hero {{
            position: relative;
            height: 50vh;
            min-height: 400px;
            background: url('{image_url}') center/cover no-repeat;
            display: flex;
            align-items: flex-end;
            padding-bottom: 4rem;
        }}
        
        .article-hero::after {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(to top, var(--bg) 0%, rgba(5,5,7,0.7) 50%, rgba(5,5,7,0.3) 100%);
        }}
        
        .hero-content {{
            position: relative;
            z-index: 1;
            width: 90%;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .category-pill {{
            background: rgba(0, 240, 255, 0.1);
            color: var(--primary);
            padding: 0.25rem 0.75rem;
            border-radius: 100px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: inline-block;
            margin-bottom: 1rem;
            border: 1px solid rgba(0, 240, 255, 0.2);
        }}
        
        h1 {{
            font-size: clamp(2rem, 5vw, 3.5rem);
            line-height: 1.1;
            margin: 0 0 1rem 0;
            background: linear-gradient(to right, #fff, #94A3B8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .meta-info {{
            font-size: 0.9rem;
            color: var(--text-dim);
            display: flex;
            gap: 1.5rem;
        }}

        /* Key Takeaways Box (NEW) */
        .quick-summary {{
            background: rgba(0, 240, 255, 0.03);
            border-left: 4px solid var(--primary);
            padding: 1.5rem 2rem;
            margin: 2rem 0;
            border-radius: 0 8px 8px 0;
            font-size: 1.05rem;
        }}
        .quick-summary strong {{ color: var(--primary); display: block; margin-bottom: 0.5rem; }}
        
        /* Article Body */
        .article-container {{
            width: 90%;
            max-width: 800px;
            margin: 0 auto;
            padding: 4rem 0;
        }}
        
        .article-body {{
            font-size: 1.15rem;
            line-height: 1.8;
            color: #CBD5E1;
        }}
        
        .article-body h2 {{
            color: #fff;
            margin: 3rem 0 1.5rem 0;
            font-size: 1.75rem;
        }}
        
        .article-body p {{ margin-bottom: 1.5rem; }}
        
        /* Footer */
        footer {{
            border-top: 1px solid rgba(255,255,255,0.1);
            padding: 3rem 0;
            text-align: center;
            margin-top: 4rem;
            color: var(--text-dim);
        }}

        .back-btn {{
            display: inline-block;
            margin-top: 3rem;
            background: var(--primary);
            color: #000;
            padding: 1rem 2rem;
            border-radius: 100px;
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.2s;
        }}
        
        .back-btn:hover {{ transform: scale(1.05); }}
    </style>
</head>
<body>

<nav>
    <a href="../index.html" class="logo">
        <img src="../assets/brand-logo.png" alt="Logo" class="logo-img">
        <div class="logo-text">AI.CORE <span>LOGIC</span></div>
    </a>
    <div class="nav-links">
        <a href="../index.html">Home</a>
    </div>
</nav>

<header class="article-hero">
    <div class="hero-content">
        <span class="category-pill">AI Market Analysis</span>
        <h1>{title}</h1>
        <div class="meta-info">
            <span>{date_str}</span>
            <span>•</span>
            <span>{read_time} min read</span>
        </div>
    </div>
</header>

<main class="article-container">
    <!-- Quick Summary Section -->
    <div class="quick-summary">
        <strong>💡 Key TakeAways:</strong> 
        {{TLDR_SUMMARY}}
    </div>

    <!-- Main Content -->
    <div class="article-body">
        {content}
        <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 3rem 0;">
        
        {editorial_bio_html}
    </div>
    
    <a href="../index.html" class="back-btn">← Back to News Feed</a>
</main>

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
        
        # Replace TL;DR placeholder with actual content
        if not tldr_summary:
            tldr_summary = "Key insights and actionable takeaways to stay ahead in the AI landscape."
        
        post_html = post_html.replace("{{TLDR_SUMMARY}}", tldr_summary)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(post_html)
            
        print(f"Blog post created: {filepath}")
        return filename

    def update_index(self, title, summary, filename, image_url=None):
        """
        Rebuilds the entire site (index.html, category pages, etc.) by calling generate_categories.py.
        This ensures the new post is correctly categorized and added to all relevant pages.
        """
        import subprocess
        print("Rebuilding site structure (Index + Categories)...")
        
        # Path to generate_categories.py (assumed to be in project root)
        # We need to find the root directory relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir) # up one level from 'news_bot'
        script_path = os.path.join(project_root, "generate_categories.py")
        
        try:
            subprocess.run(["python", script_path], check=True, cwd=project_root)
            print("Site rebuild complete.")
        except Exception as e:
            print(f"Error rebuilding site: {e}")

    def deploy_to_github(self):
        """
        Commits and pushes the new changes to GitHub so the link becomes live.
        """
        import subprocess
        
        print("Auto-Deploying to GitHub...")
        try:
            # 1. Add changes
            subprocess.run(["C:\\Program Files\\Git\\cmd\\git.exe", "add", "."], check=True)
            
            # 2. Commit
            try:
                subprocess.run(["C:\\Program Files\\Git\\cmd\\git.exe", "commit", "-m", "Auto-publish new article"], check=True)
            except subprocess.CalledProcessError:
                print("Nothing to commit (files already exist). Proceeding to push...")
            
            # 3. Push
            # Note: This relies on your cached credentials.
            subprocess.run(["C:\\Program Files\\Git\\cmd\\git.exe", "push"], check=True)
            
            print("Successfully deployed to https://aicorelogic-ops.github.io/ai-core-logic/")
            return True
        except Exception as e:
            print(f"Deploy failed: {e}")
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
