import os
import google.generativeai as genai
from dotenv import load_dotenv
from news_bot.blog_generator import BlogGenerator

# Load Environment Variables
load_dotenv(os.path.join("news_bot", ".env"))
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in news_bot/.env")

genai.configure(api_key=API_KEY)

# The "Sabri Suby" System Prompt
SYSTEM_PROMPT = """
You are a Direct Response Copywriter expert in the style of Sabri Suby.
Your goal is to write a High Value Content Offer (HVCO) blog post.

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

ARTICLES = [
    {
        "type": "Provocative",
        "title": "The Death of the Middle Manager",
        "summary": "Why AI Agents are flattening logistics orgs and saving 40% overhead.",
        "prompt": """
        Write a blog post titled "The Death of the Middle Manager: How AI Agents are Flattening Logistics Orgs".
        Key Points: 1. Hook: Middle Management is the "silent killer". 2. Pain: Telephone game. 3. Solution: AI Agents. 4. Proof: Negotiation in 300ms. 5. Prediction: 90% fewer managers.
        """,
        "social_prompt": """
        Write a Facebook Ad for this article. 
        Style: Sabri Suby. Aggressive. Pattern interrupting.
        Structure: 
        1. Call out the audience (Logistics Owners/Managers).
        2. Agitate the pain (Burning profit, 3am calls).
        3. The Big Reveal (The Death of the Middle Manager).
        4. Curiosity gap to get the click.
        Keep it long-form and punchy. Include a link placeholder [LINK].
        """
    },
    {
        "type": "Case Study",
        "title": "Case Study: Automating a 50-Person Dispatch Team",
        "summary": "The exact blueprint we used to recover 20 hours/week per dispatcher.",
        "prompt": """
        Write a Case Study titled "We Automated a 50-Person Dispatch Team. Here's the Exact Blueprint."
        Key Points: 1. Problem: 4k emails/day. 2. Bottleneck: Humans reading slow. 3. Fix: Inbox Agent. 4. Result: 20hrs saved/week.
        """,
        "social_prompt": """
        Write a Facebook Ad for this Case Study. 
        Style: Sabri Suby. 'I found a secret' tone.
        Call out: Business owners struggling with scaling.
        Agitate: Tired of your team drowning in admin?
        Solution: The 'Inbox Agent' blueprint.
        Proof: 20 hours saved every single week.
        Include a link placeholder [LINK].
        """
    },
    {
        "type": "Tutorial",
        "title": "Tutorial: Build Your Own 'Email Sorter' Bot",
        "summary": "A 10-minute guide to building your first AI logic filter.",
        "prompt": """
        Write a technical Tutorial titled "How to Build Your Own 'Email Sorter' Bot in 10 Minutes".
        Key Points: 1. Promise: No-code logic. 2. Stack: Python/Gemini. 3. Concept: Auto-sorting. 4. Benefit: Inbox peace.
        """,
        "social_prompt": """
        Write a Facebook Ad for this Tutorial.
        Style: 'You're being lied to' energy. 
        Hook: You don't need a dev team to automate your life.
        Agitate: Your inbox is a graveyard of wasted time.
        Offer: A 10-minute blueprint to reclaim your peace.
        Include a link placeholder [LINK].
        """
    }
]


def generate_hvco():
    print("🚀 Starting HVCO Generator (Sabri Mode)...")
    
    from news_bot.publisher import FacebookPublisher
    blog_gen = BlogGenerator()
    fb_pub = FacebookPublisher()
    model = genai.GenerativeModel('models/gemini-2.0-flash')

    import time
    from google.api_core import exceptions
    import urllib.parse

    for article in ARTICLES:
        print(f"\n✍️ Writing: {article['title']}...")
        
        # 1. Generate Blog Content
        content_html = None
        for attempt in range(5):
            try:
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\nTASK:\n{article['prompt']}")
                content_html = response.text.replace("```html", "").replace("```", "")
                break
            except exceptions.ResourceExhausted:
                time.sleep(20 * (2 ** attempt))

        if not content_html: continue

        # 2. Generate Social Ad Copy
        social_copy = None
        for attempt in range(5):
            try:
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\nTASK:\n{article['social_prompt']}")
                social_copy = response.text.replace("```text", "").replace("```", "").strip()
                break
            except exceptions.ResourceExhausted:
                time.sleep(20 * (2 ** attempt))

        # 3. Create 'Screaming' Visual Prompt
        # High contrast, bold, editorial, attention-grabbing
        screaming_prompt = urllib.parse.quote(f"Bold high-impact editorial illustration: {article['title']}. Vibrant neon colors, high contrast, dramatic shadows, futuristic digital art style, ultra-detailed, 8k, attention-grabbing composition")
        image_url = f"https://image.pollinations.ai/prompt/{screaming_prompt}?width=1200&height=630&nologo=true"

        # 4. Create Blog Post
        filename = blog_gen.create_post(
            title=article['title'],
            content_html=content_html,
            original_link="https://aicorelogic-ops.github.io/ai-core-logic/",
            image_url=image_url
        )
        
        blog_gen.update_index(
            title=article['title'],
            summary=article['summary'],
            filename=filename,
            image_url=image_url
        )

        # 5. Post to Facebook as PHOTO POST (Screaming Visual + Ad Copy)
        live_link = f"https://aicorelogic-ops.github.io/ai-core-logic/blog/posts/{filename}"
        final_social_msg = social_copy.replace("[LINK]", live_link)
        
        print(f"📢 Posting to Facebook: {article['title']}...")
        fb_pub.post_photo(photo_url=image_url, message=final_social_msg)
        
        print("💤 Cooling down API...")
        time.sleep(30)

    # Deploy Blog
    print("\n☁️ Deploying all changes to GitHub...")
    blog_gen.deploy_to_github()


if __name__ == "__main__":
    generate_hvco()
