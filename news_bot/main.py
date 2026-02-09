import time
from .collector import NewsCollector
from .processor import NewsProcessor
from .publisher import FacebookPublisher
from .blog_generator import BlogGenerator

def run_bot():
    print("🤖 Starting AI Core Logic News Bot...")

    # 1. Collect
    collector = NewsCollector()
    # Using 72 hours window for testing to ensure we find something
    articles = collector.fetch_news(hours_back=72)
    print(f"📥 Found {len(articles)} potential articles.")

    if not articles:
        print("😴 No new articles found. Sleeping.")
        return

    # 2. Process & Publish
    processor = NewsProcessor()
    publisher = FacebookPublisher()
    blog_gen = BlogGenerator()

    for article in articles:
        print(f"📝 Processing: {article['title']}")
        
        # Generates DICT: {'blog_html': ..., 'facebook_msg': ...}
        content_package = processor.summarize(article)
        
        if content_package:
            # A. Create Blog Post
            filename = blog_gen.create_post(
                article['title'], 
                content_package['blog_html'], 
                article['link'],
                image_url=article.get('image_url')
            )
            
            # B. Update Index
            blog_gen.update_index(
                article['title'], 
                "New AI Analysis available.", # Simple snippet
                filename,
                image_url=article.get('image_url')
            )
            
            # C. Prepare Facebook Link
            # Production URL structure for GitHub Pages
            blog_url = f"https://aicorelogic-ops.github.io/ai-core-logic/blog/posts/{filename}" 
            
            fb_message = content_package['facebook_msg'].replace("[LINK]", blog_url)
            
            # D. Deploy to GitHub
            is_deployed = blog_gen.deploy_to_github()
            
            if not is_deployed:
                print("⚠️ GitHub deploy reported failure (might just be 'no changes'), proceeding anyway...")

            # E. Post to Facebook (ALWAYS try to post, the link is likely fine)
            print(f"🚀 Publishing to Facebook...")
            publisher.post_content(fb_message, link=blog_url)
            
            # Sleep to avoid spamming
            time.sleep(10)
        else:
            print("❌ Failed to process article.")

if __name__ == "__main__":
    run_bot()
