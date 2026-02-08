import os
from datetime import datetime

BLOG_DIR = "blog"
POSTS_DIR = os.path.join(BLOG_DIR, "posts")

# Ensure posts directory exists
os.makedirs(POSTS_DIR, exist_ok=True)

class BlogGenerator:
    def create_post(self, title, content_html, original_link):
        """
        Creates a new HTML file for the blog post and returns its relative path.
        """
        # Create a safe filename
        safe_title = "".join([c if c.isalnum() else "-" for c in title]).lower()
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-{safe_title[:30]}.html"
        filepath = os.path.join(POSTS_DIR, filename)
        
        # HTML Template for individual post
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
    <div class="logo"><a href="../index.html" style="text-decoration:none; color:inherit;">AI Core Logic</a></div>
    <div class="subtitle">Intelligence for Business</div>
</header>

<main>
    <article class="article-card">
        <div class="article-date">{datetime.now().strftime('%B %d, %Y')}</div>
        <h1>{title}</h1>
        <div class="article-body">
            {content_html}
        </div>
        <hr style="border-color: #233554; margin: 2rem 0;">
        <p><em>Source: <a href="{original_link}" target="_blank" style="color: var(--brand-blue);">Read original article</a></em></p>
        <br>
        <a href="../index.html" class="read-more">← Back to Home</a>
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

    def update_index(self, title, summary, filename):
        """
        Injects the new post into the top of index.html
        """
        index_path = os.path.join(BLOG_DIR, "index.html")
        
        # New entry HTML
        new_entry = f"""
    <article class="article-card">
        <div class="article-date">{datetime.now().strftime('%B %d')}</div>
        <h2><a href="posts/{filename}">{title}</a></h2>
        <p class="article-snippet">{summary}...</p>
        <a href="posts/{filename}" class="read-more">Read Analysis →</a>
    </article>
        """
        
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find the injection point (after <main id="news-feed">)
            marker = '<main id="news-feed">'
            if marker in content:
                updated_content = content.replace(marker, marker + "\n" + new_entry)
                
                with open(index_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print("✅ Index.html updated.")
            else:
                print("❌ Could not find injection marker in index.html")
                
        except Exception as e:
            print(f"❌ Error updating index: {e}")

if __name__ == "__main__":
    # Test
    gen = BlogGenerator()
    fname = gen.create_post("Test Article", "<p>This is a test.</p>", "http://google.com")
    gen.update_index("Test Article", "This is a short summary.", fname)
