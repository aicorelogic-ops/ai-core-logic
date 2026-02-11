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
        - HIGH-READABILITY: Structure for scanners first. Most important info at the TOP.
        - HIGH-AROUSAL EMOTION: Evoke awe, anxiety, or anger to drive virality.
        - NO FLUFF: One idea per sentence. 6th grade reading level.
        - MOBILE-FIRST: Paragraphs must be 1-3 sentences max.
        
        Task: Create TWO outputs in a strictly formatted way.
        
        Output 1: A BLOG POST (HTML Format)
        **STRUCTURE SPECS:**
        
        1. **PATTERN INTERRUPT HOOK**: Start with a shocking statement or number.
        
        2. **PPT INTRO (Preview, Proof, Transition)**:
           - PREVIEW: What is this post about?
           - PROOF: Why should they listen? (Expertise/Data)
           - TRANSITION: Move them into the body content.
           
        3. **INVERTED PYRAMID**: Put the "Who, What, When, Where, Why" in the first 2 paragraphs.
        
        4. **LAYER-CAKE SCANNING**:
           - Use BOLD and DESCRIPTIVE H2/H3 headers.
           - Use BULLET POINTS (<ul><li>) for key data.
           - NO generic headers like "Introduction" or "Conclusion".
           
        5. **SABRI SUBY STYLE**: 80% agitation of pain/desire, 20% solution.
        
        6. **TAC CONCLUSION (Transition, Ask, Call to Action)**:
           - TRANSITION: Signal the end of the content.
           - ASK: Ask a specific question to encourage comments/shares.
           - CALL TO ACTION: Tell them exactly what to do next.
        
        **CONTENT RULES**:
        - Use H2 for major segments and H3 for sub-points.
        - Keep paragraphs 1-3 sentences for mobile readability.
        - Take a strong stance. Be opinionated.
        
        Output 2: A FACEBOOK POST (Research-Backed Engagement Formula)
        
        **CONTENT STRATEGY FRAMEWORK:**
        Apply the PPT Formula for maximum impact:
        1. **PREVIEW (Line 1)**: Front-load the most shocking/valuable insight in the FIRST 2-3 WORDS
           - Users scan in F-pattern (top left is critical)
           - First line must stand alone and arrest scrolling
        
        2. **PROOF (Line 2)**: Establish credibility or amp emotion
           - Cite data, trends, or amplify the "why this matters NOW"
           - Must evoke HIGH-AROUSAL emotion (choose ONE):
             * ✅ AWE/EXCITEMENT (wonder, breakthrough)
             * ✅ ANXIETY (urgency, fear of missing out) 
             * ✅ ANGER (injustice, outrage)
             * ❌ AVOID: Sadness, contentment (low arousal = no shares)
        
        3. **TRANSITION (Lines 3-4)**: Deliver practical value in 1-2 punchy lines
           - Short paragraphs (1-2 sentences each) get 2x more eye fixations
           - Each line should be scannable on its own
        
        **FORMATTING FOR SCANNABILITY:**
        - **MAX 60-80 WORDS TOTAL** (ultra-brevity)
        - Line breaks after every 1-2 sentences (white space = focus)
        - 2-3 emojis max (visual breaks, not clutter)
        - NO markdown bolding
        - Use [BRACKETS] around 1 key term for 38% higher CTR
        
        **TAC CLOSE (Call to Action):**
        - **T**ransition: Signal the end
        - **A**sk: Specific 2-second question (not "thoughts?")
        - **C**TA: Direct command ("Click," "Read," "Share")
        
        **HEADLINE HOOK:**
        - 3 relevant hashtags (social proof + discoverability)
        - End with: "Full story: [LINK] || Image Idea: [Brief scene for news graphic]"
        
        **VISUAL GUIDANCE:**
        - Suggest scene with FACES (multiple faces = maximum attention)
        - Align mood with arousal emotion (urgent/exciting/shocking)
        
        Output 3: A TL;DR SUMMARY (2-3 Bullet Points)
        **PURPOSE**: Distill the entire article into actionable key takeaways
        
        **FORMAT**:
        - Exactly 2-3 bullet points
        - Each bullet should be ONE sentence (15-20 words max)
        - Focus on ACTIONABLE insights or shocking facts
        - Use plain text (no markdown symbols like • or -)
        
        Output 4: EDITORIAL PROSPECT (Unique Insight)
        **PURPOSE**: A short, punchy opinion/take on why this matters (for the author bio section)
        
        **FORMAT**:
        - A 2-3 sentence paragraph (50-70 words)
        - Written in a "no-nonsense, insider" voice
        - Explain the "Real Truth" or "Hidden Implication" of this news
        - Start with a strong hook like "Let's be real," "Here's the thing," or "The bottom line is"
        
        CRITICAL RETURN FORMAT:
        - Separate outputs with EXACT delimiter: "|||||"
        - First part = HTML blog
        - Second part = Plain text Facebook post
        - Third part = TL;DR bullet points
        - Fourth part = Editorial Prospect text
        """

        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            # Split the response
            if "|||||" in text:
                parts = text.split("|||||")
                blog_html = parts[0].strip()
                facebook_msg = parts[1].strip() if len(parts) > 1 else ""
                tldr_raw = parts[2].strip() if len(parts) > 2 else ""
                editorial_prospect = parts[3].strip() if len(parts) > 3 else "We analyze the intersection of logistics, automation, and AI to deliver actionable insights for modern businesses. No hype, just practical strategy."
                
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
                
                # Process TL;DR - format as HTML bullet list
                tldr_html = ""
                if tldr_raw:
                    # Clean up labels
                    tldr_raw = tldr_raw.replace('**OUTPUT 3:**', '').replace('OUTPUT 3:', '')
                    tldr_raw = tldr_raw.replace('**TL;DR:**', '').replace('TL;DR:', '').strip()
                    
                    # Split into bullets and format
                    bullets = [line.strip() for line in tldr_raw.split('\n') if line.strip()]
                    if bullets:
                        tldr_html = "<ul style='margin: 0; padding-left: 1.5rem; line-height: 1.8;'>" 
                        for bullet in bullets:
                            tldr_html += f"<li style='margin-bottom: 0.75rem;'>{bullet}</li>"
                        tldr_html += "</ul>"
                
                if not tldr_html:
                    # Fallback
                    tldr_html = "Key insights and actionable takeaways to stay ahead in the AI landscape."
                
                return {
                    "blog_html": blog_html,
                    "facebook_msg": facebook_msg,
                    "tldr_summary": tldr_html,
                    "editorial_prospect": editorial_prospect
                }
            else:
                # Fallback if AI forgets delimiter
                return {
                    "blog_html": f"<p>{text}</p>",
                    "facebook_msg": "New AI Update! Check our blog. [LINK]",
                    "tldr_summary": "Key insights from this AI development."
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
