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

            # E. Post to Facebook as PHOTO POST (Higher Engagement)
            # Hyper-dopamine strategy: Photo posts stop the scroll, link is in caption
            print(f"🚀 Publishing to Facebook as photo post...")
            
            # Get the image URL (use article image or the generated one from blog)
            photo_url = article.get('image_url')
            if not photo_url:
                # Fallback: generate a native-style attention-grabbing image
                import urllib.parse
                safe_prompt = urllib.parse.quote(f"Breaking news smartphone photo: {article['title']}. Red circle highlight, BREAKING banner, native social media style, high engagement")
                photo_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1200&height=630&nologo=true"
            
            publisher.post_photo(photo_url=photo_url, message=fb_message)
            
            # Sleep to avoid spamming
            time.sleep(10)
        else:
            print("❌ Failed to process article.")

if __name__ == "__main__":
    run_bot()
