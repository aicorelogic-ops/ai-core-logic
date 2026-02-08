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
        You are an expert AI Analyst for 'AI Core Logic'.
        
        Input:
        Title: {article['title']}
        Summary: {article['summary']}
        
        Task: Create TWO outputs in a strictly formatted way.
        
        Output 1: A BLOG POST (HTML Format)
        - Use <h3> for subheaders.
        - Use <p> for paragraphs.
        - Use <ul><li> for lists.
        - Tone: Detailed, analytical, educational.
        - content: 
            - "What is it?"
            - "Why it matters for Business/Logistics"
            - "Our Take/Prediction"
        
        Output 2: A FACEBOOK POST (Plain Text)
        - Hook: "🚀 New AI Tool..."
        - Teaser: "We analyzed how [Tool] affects your business..."
        - CTA: "Read the full analysis here: [LINK]" (Place holder [LINK])
        
        RETURN FORMAT:
        Separate the two with a delimiter "|||||".
        First part = HTML. Second part = Facebook Text.
        """

        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            # Split the response
            if "|||||" in text:
                parts = text.split("|||||")
                return {
                    "blog_html": parts[0].strip(),
                    "facebook_msg": parts[1].strip()
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
