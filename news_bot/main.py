import time
from .collector import NewsCollector
from .processor import NewsProcessor
from .publisher import FacebookPublisher
from .blog_generator import BlogGenerator
from .article_tracker import ArticleTracker
# from .viral_reel_generator import ViralReelGenerator  # Removed per user request
from .image_design_helper import analyze_article_visual_context, create_news_overlay_prompt

def run_bot():
    print("Starting AI Core Logic News Bot...")

    # Initialize tracker
    tracker = ArticleTracker()
    
    # 1. Collect
    collector = NewsCollector()
    # Using 72 hours window for testing to ensure we find something
    articles = collector.fetch_news(hours_back=72)
    print(f"Found {len(articles)} potential articles.")

    if not articles:
        print("No new articles found. Sleeping.")
        return

    # 2. Score Articles for Viral Potential (Select BEST, not newest)
    print("Scoring articles for viral potential...")
    
    def score_viral_potential(article):
        # (existing scoring logic unchanged)
        try:
            import google.generativeai as genai
            from .settings import GOOGLE_API_KEY
            
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel('gemini-flash-latest')
            
            prompt = f"""Score this article for VIRAL POTENTIAL in the logistics/business automation niche (0-100).

Title: {article['title']}
Summary: {article.get('summary', '')[:300]}

Scoring Factors:
1. SPECIFICITY: Does it have specific numbers/data? ($40k, 30% increase, etc.)
2. CONTROVERSY: Is it provocative or against conventional wisdom?
3. URGENCY: Does it create time pressure or FOMO?
4. EMOTIONAL HOOK: Does it trigger fear, curiosity, or anger?
5. RELEVANCE: Will logistics/small business owners care?
6. CLICKBAIT FACTOR: Does the title create a curiosity gap?

Return ONLY a number 0-100. No explanation."""

            response = model.generate_content(prompt)
            score = int(response.text.strip())
            return max(0, min(100, score))  # Clamp between 0-100
        except Exception as e:
            print(f"Scoring error: {e}")
            return 50  # Default middle score if error
    
    # Score all articles
    articles_with_scores = []
    for article in articles:
        # Check if already processed
        if tracker.is_processed(article['link']):
            print(f"  Skipping score for processed article: {article['title'][:60].encode('ascii', 'ignore').decode('ascii')}...")
            continue
            
        score = score_viral_potential(article)
        articles_with_scores.append((article, score))
        print(f"  '{article['title'][:60].encode('ascii', 'ignore').decode('ascii')}...' -> Score: {score}")
    
    if not articles_with_scores:
        print("All found articles have already been processed. Nothing to do.")
        return

    # Select the HIGHEST scoring article
    best_article, best_score = max(articles_with_scores, key=lambda x: x[1])
    print(f"\nSelected BEST article (Score: {best_score}): {best_article['title'].encode('ascii', 'ignore').decode('ascii')}\n")
    
    # 3. Process & Publish the BEST article
    processor = NewsProcessor()
    publisher = FacebookPublisher()
    blog_gen = BlogGenerator()
    # viral_gen = ViralReelGenerator()  # Removed per user request

    # Process only the BEST article (highest viral score)
    # UPDATED: Loop through top 3 articles in case the best one is a duplicate
    articles_with_scores.sort(key=lambda x: x[1], reverse=True)
    
    selected_article = None
    
    for article, score in articles_with_scores[:3]:
        print(f"Checking candidate: {article['title'].encode('ascii', 'ignore').decode('ascii')} (Score: {score})")
        
        # Check against existing filesystem (Title Similarity)
        is_dup, existing_file = blog_gen.is_duplicate_title(article['title'])
        if is_dup:
             print(f"  SKIP: Similar article already exists: {existing_file}")
             # Mark as processed so we don't check it again next time
             tracker.mark_as_processed(article['link'], {'title': article['title'], 'status': 'duplicate_skipped'})
             continue
             
        selected_article = article
        break
    
    if not selected_article:
        print("All top candidates were duplicates or processed. Sleeping.")
        return

    for article in [selected_article]:  # Process only the winner
        print(f"Processing: {article['title'].encode('ascii', 'ignore').decode('ascii')}")
        
        # Generates DICT: {'blog_html': ..., 'facebook_msg': ...}
        content_package = processor.summarize(article)
        
        if content_package:
            # A. Create Blog Post
            filename = blog_gen.create_post(
                article['title'], 
                content_package['blog_html'], 
                article['link'],
                image_url=article.get('image_url'),
                tldr_summary=content_package.get('tldr_summary'),
                editorial_prospect=content_package.get('editorial_prospect')
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
                print("GitHub deploy reported failure (might just be 'no changes'), proceeding anyway...")

            # E. Post Viral Photo to Facebook
            print(f"Publishing to Facebook as viral photo post...")
            
            fb_caption = content_package['facebook_msg'].replace("[LINK]", blog_url)
            image_idea = ""
            
            # Extract Image Design/Idea specs - handle multiple formats
            # Format 1: || Image Design: (preferred)
            if "|| Image Design:" in fb_caption:
                parts = fb_caption.split("|| Image Design:")
                fb_caption = parts[0].strip()
                image_idea = parts[1].strip()
            # Format 2: || Image Idea: (legacy)
            elif "|| Image Idea:" in fb_caption:
                parts = fb_caption.split("|| Image Idea:")
                fb_caption = parts[0].strip()
                image_idea = parts[1].strip()
            # Format 3: Image Idea: (AI forgot delimiter)
            elif "Image Idea:" in fb_caption:
                parts = fb_caption.split("Image Idea:")
                fb_caption = parts[0].strip()
                image_idea = parts[1].strip()
            # Format 4: Image Design: (AI forgot delimiter)
            elif "Image Design:" in fb_caption:
                parts = fb_caption.split("Image Design:")
                fb_caption = parts[0].strip()
                image_idea = parts[1].strip()
            
            # Final cleanup: remove any remaining image-related instruction text
            import re
            fb_caption = re.sub(r'\s*\|\|\s*Image (Design|Idea):.*$', '', fb_caption, flags=re.IGNORECASE | re.DOTALL)
            fb_caption = re.sub(r'\s*Image (Design|Idea):.*$', '', fb_caption, flags=re.IGNORECASE | re.DOTALL)
            fb_caption = fb_caption.strip()
            
            import urllib.parse
            
            # NEW APPROACH: Use news overlay style inspired by ABC News / Variety graphics
            print(f"Analyzing article for visual design specs...")
            design_specs = analyze_article_visual_context(article)
            print(f"   Design specs: {design_specs['category_badge']} | {design_specs['emotion_trigger']} mood")
            
            # Generate professional news-style prompt
            final_image_prompt = create_news_overlay_prompt(article, design_specs, image_idea)
            
            # Sanitize prompt for URL (Pollinations doesn't like newlines or excessive length)
            clean_prompt = final_image_prompt.replace('\n', ' ').replace('\r', '').replace('  ', ' ').strip()
            # Limit to 800 chars to be safe (URL limits)
            if len(clean_prompt) > 800:
                clean_prompt = clean_prompt[:800]
            
            safe_prompt = urllib.parse.quote(clean_prompt)
            photo_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1200&height=630&nologo=true"
            
            photo_post_id = publisher.post_photo(photo_url=photo_url, message=fb_caption)
            
            # F. REEL GENERATION REMOVED PER USER REQUEST
            # (Previously created and posted viral reels here)
            video_post_id = None
            
            # F. TRACK ARTICLE AS PROCESSED
            tracker.mark_as_processed(article['link'], {
                'title': article['title'],
                'blog_path': f"blog/posts/{filename}",
                'facebook_photo_id': photo_post_id,
                'facebook_video_id': video_post_id
            })
            
            # Sleep to avoid spamming
            time.sleep(10)
        else:
            print("Failed to process article.")

if __name__ == "__main__":
    run_bot()
