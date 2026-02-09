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

ARTICLES = [
    {
        "type": "Provocative",
        "title": "The Death of the Middle Manager",
        "summary": "Why AI Agents are flattening logistics orgs and saving 40% overhead.",
        "prompt": """
        Write a blog post titled "The Death of the Middle Manager: How AI Agents are Flattening Logistics Orgs".
        
        STRUCTURE (80% PAIN, 20% SOLUTION):
        1. Hook: Pattern interrupt - "Middle Management is the 'silent profit killer'. Here's the proof."
        2. Agitate Pain: The telephone game, lost hours, 3am emergency calls, burning overhead
        3. The Discovery: AI Agents negotiate in 300ms (use specific numbers)
        4. Why It Matters: Specific benefit for logistics owners (e.g., "40% overhead reduction")
        5. Prediction: Where this is headed (90% fewer managers by 2027)
        
        Use prospect language: "You're paying a middle manager $80k to forward emails."
        """,
        "social_prompt": """
        Write a Facebook Ad for this article (LONG-FORM 200+ words).
        
        HYPER-DOPAMINE STRUCTURE:
        1. Call out the audience: "Logistics owners with 10+ person teams..."
        2. Agitate specific pain: "You're burning $15k/month on middle managers who just... forward emails. 
           At 3am, they call YOU anyway. The 'telephone game' is costing you deals."
        3. Curiosity Gap: "We discovered something that cuts management overhead by 40%. No layoffs. No drama."
        4. Specific Benefit + Intrigue: "AI Agents that negotiate carrier rates in 300 milliseconds."
        5. The Big Reveal: "The Death of the Middle Manager" (title drop)
        6. CTA: "The full blueprint is here: [LINK]"
        
        Style: Long copy, emojis (🚨⚡), pattern interrupt, specific numbers, NOT vague clickbait.
        """
    },
    {
        "type": "Case Study",
        "title": "Case Study: Automating a 50-Person Dispatch Team",
        "summary": "The exact blueprint we used to recover 20 hours/week per dispatcher.",
        "prompt": """
        Write a Case Study titled "We Automated a 50-Person Dispatch Team. Here's the Exact Blueprint."
        
        STRUCTURE:
        1. Hook: "4,000 emails a day. 50 people drowning. One solution."
        2. The Problem: 80% PAIN - Humans reading slow, errors, burnout, 3am calls
        3. The Bottleneck: Show the exact pain point (use real scenarios)
        4. The Fix: Inbox Agent - but focus on RESULTS, not tech specs
        5. Result: 20 hours saved/week per dispatcher (specific number)
        
        Use prospect language: "Your dispatchers are buried in admin hell."
        """,
        "social_prompt": """
        Write a Facebook Ad for this Case Study (LONG-FORM 200+ words).
        
        HYPER-DOPAMINE STRUCTURE:
        1. Call out: "Business owners struggling to scale past 20 employees..."
        2. Agitate: "Your team is drowning in admin. 4,000 emails/day. Errors. Burnout. You can't hire fast enough."
        3. 'Secret' Tone: "I found a blueprint that gave me back 20 hours per person. Every single week."
        4. Proof: Real numbers - "50-person dispatch team, 4k emails, 20 hours saved/week"
        5. The Hook: "The 'Inbox Agent' blueprint"
        6. CTA: "Steal the exact blueprint here: [LINK]"
        
        Style: 'I cracked the code' energy, specific proof, long-form copy.
        """
    },
    {
        "type": "Tutorial",
        "title": "Tutorial: Build Your Own 'Email Sorter' Bot",
        "summary": "A 10-minute guide to building your first AI logic filter.",
        "prompt": """
        Write a technical Tutorial titled "How to Build Your Own 'Email Sorter' Bot in 10 Minutes".
        
        STRUCTURE:
        1. Hook: "You don't need a $50k dev team. Here's proof."
        2. Pain (80%): "Your inbox is a graveyard. 800 unread. Missed deals. Anxiety."
        3. Promise: No-code logic, anyone can do this
        4. The Stack: Python + Gemini (but keep it simple)
        5. The Concept: Auto-sorting magic
        6. The Benefit: Inbox peace (emotional outcome)
        
        Make it accessible to non-technical readers.
        """,
        "social_prompt": """
        Write a Facebook Ad for this Tutorial (LONG-FORM 200+ words).
        
        HYPER-DOPAMINE STRUCTURE:
        1. 'You're being lied to' Hook: "They told you that you need a dev team to automate. That's a lie."
        2. Agitate: "Your inbox: 800 unread. You miss deals. You feel behind. Every. Single. Day."
        3. The Reveal: "I built an 'Email Sorter' bot in 10 minutes. Zero code. Zero devs."
        4. Specific Benefit: "Inbox goes from 800 → 0. Autopilot."
        5. The Offer: "I'm giving you the exact 10-minute blueprint."
        6. CTA: "Reclaim your peace here: [LINK]"
        
        Style: Rebellious, specific, long-form, emojis (🔥💡).
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

        # 3. Create 'Native Hyper-Dopamine' Visual Prompt
        # NotebookLM Strategy: Raw, iPhone photo style, pattern interrupts (red circles, breaking news banners)
        # Avoid polished "ad look" - use native social media aesthetic
        import random
        native_styles = [
            f"iPhone smartphone photo: {article['title']}. Red circle highlighting key element, BREAKING NEWS banner overlay, raw authentic photography, native social media aesthetic, high engagement",
            f"Raw smartphone photo with reaction shot inset: {article['title']}. Dual image composition, authentic native style, pattern interrupt visual, high contrast",
            f"Breaking news style screenshot: {article['title']}. News notification aesthetic, bold text overlay, authentic smartphone capture, attention-grabbing"
        ]
        chosen_style = random.choice(native_styles)
        screaming_prompt = urllib.parse.quote(chosen_style)
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
