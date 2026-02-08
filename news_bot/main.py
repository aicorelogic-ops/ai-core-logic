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
                article['link']
            )
            
            # B. Update Index
            blog_gen.update_index(
                article['title'], 
                "New AI Analysis available.", # Simple snippet
                filename
            )
            
            # C. Prepare Facebook Link
            # IMPORTAT: Since this is local, we don't have a real URL yet.
            # We will post a dummy link or the file path for now.
            # In production, this would be: https://your-site.com/blog/posts/{filename}
            blog_url = f"https://aicorelogic.com/news/{filename}" 
            
            fb_message = content_package['facebook_msg'].replace("[LINK]", blog_url)
            
            # D. Post to Facebook
            print(f"🚀 Publishing to Facebook...")
            publisher.post_content(fb_message, link=blog_url)
            
            # Sleep to avoid spamming
            time.sleep(10)
        else:
            print("❌ Failed to process article.")

if __name__ == "__main__":
    run_bot()
