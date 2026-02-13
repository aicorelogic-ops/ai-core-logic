import os
import google.generativeai as genai
from dotenv import load_dotenv
from news_bot.blog_generator import BlogGenerator
from news_bot.collector import NewsCollector
from news_bot.article_tracker import ArticleTracker
import time
from google.api_core import exceptions
import urllib.parse
import re

# Load Environment Variables
load_dotenv(os.path.join("news_bot", ".env"))
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in news_bot/.env")

genai.configure(api_key=API_KEY)

# The "Sabri Suby" System Prompt - ENHANCED with NotebookLM Hyper-Dopamine Principles
SYSTEM_PROMPT = """
You are a Direct Response Copywriter expert in the style of Sabri Suby.
Your goal is to write a High Value Content Offer (HVCO) blog post.

CORE PRINCIPLES (From NotebookLM Research):
- "Forum Foraging": Use the prospect's exact language and words (as if from Reddit/Facebook comments)
- 80/20 Rule: 80% about PROSPECT'S pain/desires, only 20% about you/solution
- Sell the CLICK: Big specific benefit + burning intrigue (not the full pitch)
- 6th Grade Reading Level: Short, punchy sentences. No complex jargon.
- Long-Form Converts: Buyers need details. Don't be afraid of length.

Style Guidelines:
- Use short, punchy sentences. (The "Slippery Slope" method).
- Agitate the pain strongly before offering the solution.
- Use subheads to break up text.
- Tone: Authoritative, slightly controversial, but backed by logic.
- NO fluff. NO generic "In today's fast-paced world..." intros.
- Start with a "Pattern Interrupt" hook.

Format options:
- Use <b> bold </b> for emphasis.
- Use <ul><li> for lists.
- Use <h3> for subheaders.
- Output MUST be raw HTML (no <html> tags, just the body content).
"""

def score_viral_potential(article):
    """
    Scores an article 0-100 based on viral potential using Gemini.
    """
    try:
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        
        prompt = f"""Score this article for VIRAL POTENTIAL in the logistics/business automation niche (0-100).

Title: {article['title']}
Summary: {article.get('summary', '')[:500]}

Scoring Factors:
1. SPECIFICITY: Does it have specific numbers/data? ($40k, 30% increase, etc.)
2. CONTROVERSY: Is it provocative or posted by a major player (Elon, Bezos, etc)?
3. URGENCY: Does it create time pressure or FOMO?
4. RELEVANCE: Will logistics/small business owners care?
5. CLICKBAIT FACTOR: Does the title create a curiosity gap?

Return ONLY a number 0-100. No explanation."""

        response = model.generate_content(prompt)
        text = response.text.strip()
        match = re.search(r'\d+', text)
        if match:
            score = int(match.group())
            return max(0, min(100, score))
        return 50
    except Exception as e:
        print(f"⚠️ Scoring error: {e}")
        return 50

def generate_hvco():
    print("🚀 Starting HVCO Generator (Live RSS Mode)...")
    
    from news_bot.publisher import FacebookPublisher
    blog_gen = BlogGenerator()
    fb_pub = FacebookPublisher()
    tracker = ArticleTracker()
    model = genai.GenerativeModel('models/gemini-2.0-flash')

    # 1. FETCH LIVE NEWS
    print("📡 Fetching live news from RSS feeds...")
    collector = NewsCollector()
    raw_articles = collector.fetch_news(hours_back=48)
    
    if not raw_articles:
        print("❌ No news found in the last 48 hours.")
        return

    print(f"🔍 Found {len(raw_articles)} articles. Filtering and scoring...")

    # 2. FILTER & SCORE
    scored_articles = []
    
    for art in raw_articles:
        # A. Check Tracker (URL history)
        if tracker.is_processed(art['link']):
            print(f"   [SKIP] Already processed URL: {art['title'][:30]}...")
            continue

        # B. Check Blog Title (to prevent duplicates from different URLs)
        is_dup, existing_file = blog_gen.is_duplicate_title(art['title'])
        if is_dup:
            print(f"   [SKIP] Title collision with blog: {art['title'][:30]}...")
            continue

        # C. Score Viral Potential
        score = score_viral_potential(art)
        print(f"   [SCORE: {score}] {art['title'][:60]}...")
        
        if score > 60: # Only consider decent articles
            art['viral_score'] = score
            scored_articles.append(art)

    if not scored_articles:
        print("❌ No articles met the viral threshold (>60). Exiting.")
        return

    # 3. SELECT WINNER
    # Sort by score desc
    scored_articles.sort(key=lambda x: x['viral_score'], reverse=True)
    selected_article = scored_articles[0]
    
    print(f"\n🏆 WINNER: {selected_article['title']} (Score: {selected_article['viral_score']})")

    # 4. GENERATE DYNAMIC PROMPTS
    # We construct the Sabri Suby prompts dynamically based on the winner's content
    
    print("🧠 Constructing High-Value Prompts...")
    
    article_title = selected_article['title']
    article_summary = selected_article['summary']
    
    selected_article['prompt'] = f"""
    Write a blog post titled "{article_title}".
    
    CONTEXT from Source:
    "{article_summary}"
    
    STRUCTURE (80% PAIN, 20% SOLUTION):
    1. Hook: Pattern interrupt related to "{article_title}".
    2. Agitate Pain: Why is this relevant/painful for logistics & business owners?
    3. The Discovery/Insight: The core news update from the context.
    4. Why It Matters: Specific benefit or impact (save money, save time, avoid risk).
    5. Prediction/Takeaway: Where this is headed.
    
    Use prospect language. No fluff.
    """
    
    selected_article['social_prompt'] = f"""
    Write a Facebook Ad for this article (LONG-FORM 200+ words).
    Topic: {article_title}
    
    HYPER-DOPAMINE STRUCTURE:
    1. Call out the audience (Logistics/Business Owners).
    2. Agitate specific pain or FOMO related to this news.
    3. Curiosity Gap: "We just saw this update..."
    4. The Big Reveal: "{article_title}"
    5. CTA: "Read the full breakdown: [LINK]"
    6. HASHTAGS: Include 5-7 relevant hashtags (e.g. #AI, #Logistics, #Automation).
    
    REQUIREMENTS:
    - Use emojis (🚨, 📉, 🚀) to stop the scroll.
    - BE SPECIFIC.
    """

    # 5. EXECUTION LOOP (Same as before)
    for article in [selected_article]:
        print(f"\n✍️ Writing Blog Post...")
        
        # A. Generate Blog Content
        content_html = None
        for attempt in range(3):
            try:
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\nTASK:\n{article['prompt']}")
                content_html = response.text.replace("```html", "").replace("```", "")
                break
            except Exception as e:
                print(f"   Error generating blog: {e}. Retrying...")
                time.sleep(5)

        if not content_html:
            print("❌ Failed to generate blog content.")
            continue

        # B. Generate Social Ad Copy
        print(f"✍️ Writing Facebook Ad...")
        social_copy = None
        for attempt in range(3):
            try:
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\nTASK:\n{article['social_prompt']}")
                social_copy = response.text.replace("```text", "").replace("```", "").strip()
                
                # Cleanup
                social_copy = re.sub(r'^\*\*[^*]+\*\*\s*', '', social_copy) # Remove bold headers
                social_copy = social_copy.replace('**Facebook Ad:**', '').strip()
                break
            except Exception as e:
                print(f"   Error generating ad: {e}. Retrying...")
                time.sleep(5)

        # C. Create 'Corporate News' Visual Prompt
        from news_bot.image_design_helper import analyze_article_visual_context, create_news_overlay_prompt
        
        print(f"🎨 Designing Corporate News Graphic...")
        
        # Analyze article context for design specs
        design_specs = analyze_article_visual_context({
            'title': article['title'], 
            'summary': article['summary']
        })
        
        # Generate the Prompt
        news_prompt = create_news_overlay_prompt({
            'title': article['title']
        }, design_specs)
        
        encoded_prompt = urllib.parse.quote(news_prompt)
        # Using Pollinations with high quality settings
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&nologo=true&model=flux"

        # D. Create Blog Post File
        filename = blog_gen.create_post(
            title=article['title'],
            content=content_html,
            link="https://aicorelogic-ops.github.io/ai-core-logic/",
            image_url=image_url
        )
        
        blog_gen.update_index(
            title=article['title'],
            summary=article['summary'],
            filename=filename,
            image_url=image_url
        )

        # E. Post to Facebook
        live_link = f"https://aicorelogic-ops.github.io/ai-core-logic/blog/posts/{filename}"
        final_social_msg = social_copy.replace("[LINK]", live_link)
        
        print(f"📢 Posting to Facebook...")
        post_id = fb_pub.post_photo(photo_url=image_url, message=final_social_msg)
        
        if post_id:
            print(f"✅ Automatically posted to Facebook! ID: {post_id}")
            # F. Mark as Processed
            tracker.mark_as_processed(article['link'], {
                'title': article['title'], 
                'blog_file': filename,
                'image_url': image_url,
                'fb_post_id': post_id
            })
        else:
            print("⚠️ Facebook posting failed. Article NOT marked as fully processed (check logs).")

        
        print("💤 Cooling down API...")
        time.sleep(5)

    # Deploy Blog
    print("\n☁️ Deploying all changes to GitHub...")
    blog_gen.deploy_to_github()

if __name__ == "__main__":
    generate_hvco()
