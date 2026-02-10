import os
import google.generativeai as genai
import traceback
from .settings import GOOGLE_API_KEY

if not GOOGLE_API_KEY:
    print("Warning: GOOGLE_API_KEY is not set.")

# Configure Gemini
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest')
except Exception as e:
    print(f"Error configuring Gemini: {e}")
    model = None

class NewsProcessor:
    def summarize(self, article):
        """
        Takes an article dict and returns a DICT with:
        - 'blog_html': Full HTML analysis for the website.
        - 'facebook_msg': Short teaser for social media.
        """
        if not model:
            print("Skipping summarization: Gemini model not initialized.")
            return None

        prompt = f"""
        You are a Direct Response Copywriter for 'AI Core Logic' - writing in the style of Sabri Suby.
        
        Input:
        Title: {article['title']}
        Summary: {article['summary']}
        
        CORE PRINCIPLES:
        - 80% about the PROSPECT'S pain/desires, only 20% about the solution
        - Use short, punchy sentences (6th grade reading level)
        - NO fluff or generic intros like "In today's world..."
        - Sell the CLICK, not the product
        
        Task: Create TWO outputs in a strictly formatted way.
        
        Output 1: A BLOG POST (HTML Format)
        - Start with a PATTERN INTERRUPT hook (not generic intro)
        - Use <h3> for subheaders to break up text
        - Use <p> for paragraphs, <b> for emphasis, <ul><li> for lists
        - Structure:
            1. Hook: Pattern interrupt (e.g., "Your dispatcher is burning $10k/month. Here's proof.")
            2. Agitate the Pain: What's really costing them (use specific numbers/scenarios)
            3. The Discovery: What we found that changes everything
            4. Why It Matters: Specific benefit for logistics/business owners
            5. The Prediction: Where this is headed
        - Long-form content (buyers need details to convert)
        - Use subheads like "The Silent Profit Killer", "What We Discovered", "The 40% Rule"
        
        Output 2: A FACEBOOK POST (Plain Text, LONG-FORM 200+ words)
        - Call out the audience: "Logistics owners..." / "If you manage a dispatch team..."
        - Agitate specific pain: Use emotional, relatable scenarios (e.g., "Tired of 3am calls about missing invoices?")
        - Create burning curiosity: Specific benefit + intrigue (e.g., "The one automation recovering 20 hours per dispatcher")
        - NOT clickbait - be specific enough to attract the right people
        - Include emojis for pattern interrupt (🚨, 🔥, ⚡, 💡)
        - Long copy converts better - answer objections, build intrigue
        - End with: "Full breakdown here: [LINK]"
        - CRITICAL: Include 5-7 relevant hashtags at the very end (e.g., #AI #Logistics #Automation #BusinessGrowth #AITools #SupplyChain #TechInnovation)
        
        CRITICAL RETURN FORMAT:
        - DO NOT include labels like "Output 1:" or "Output 2:" in your response
        - DO NOT include any markdown formatting indicators like **text** in the Facebook post
        - Separate the two outputs ONLY with the delimiter "|||||"
        - First part = HTML blog content (can use HTML tags)
        - Second part = Plain text Facebook post (NO labels, NO markdown, NO formatting indicators)
        - The Facebook post should start IMMEDIATELY with the content, not with any header
        """

        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            # Split the response
            if "|||||" in text:
                parts = text.split("|||||")
                blog_html = parts[0].strip()
                facebook_msg = parts[1].strip()
                
                # Clean up Facebook message - remove any instruction labels or formatting indicators
                # Remove common AI output labels
                facebook_msg = facebook_msg.replace('**OUTPUT 2: A FACEBOOK POST (Plain Text, LONG-FORM 200+ words)**', '')
                facebook_msg = facebook_msg.replace('OUTPUT 2: A FACEBOOK POST (Plain Text, LONG-FORM 200+ words)', '')
                facebook_msg = facebook_msg.replace('**OUTPUT 2:**', '')
                facebook_msg = facebook_msg.replace('OUTPUT 2:', '')
                facebook_msg = facebook_msg.replace('**Facebook Post:**', '')
                facebook_msg = facebook_msg.replace('Facebook Post:', '')
                
                # Clean up any remaining markdown bold markers in plain text
                import re
                # Only remove ** markers if they're wrapping instruction-like text at the start
                if facebook_msg.startswith('**'):
                    facebook_msg = re.sub(r'^\*\*[^*]+\*\*\s*', '', facebook_msg)
                
                facebook_msg = facebook_msg.strip()
                
                return {
                    "blog_html": blog_html,
                    "facebook_msg": facebook_msg
                }
            else:
                # Fallback if AI forgets delimiter
                return {
                    "blog_html": f"<p>{text}</p>",
                    "facebook_msg": "New AI Update! Check our blog. [LINK]"
                }

        except Exception as e:
            print(f"Error generating summary with Gemini: {e}")
            with open("error_log.txt", "w", encoding="utf-8") as panic_log:
                traceback.print_exc(file=panic_log)
            return None

if __name__ == "__main__":
    # Test run
    processor = NewsProcessor()
    sample_article = {
        "title": "New AI Tool Automates Invoice Processing",
        "summary": "A new startup has released a tool that reads PDF invoices with 99% accuracy.",
        "link": "http://example.com"
    }
    result = processor.summarize(sample_article)
    print("BLOG:", result['blog_html'][:50] if result else "None")
    print("FB:", result['facebook_msg'] if result else "None")
