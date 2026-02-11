"""
Script to regenerate TL;DR summaries AND editorial prospects for all existing blog posts.
Uses Gemini AI to analyze each article and generate specific takeaways and editorial opinions.
"""

import os
import re
from pathlib import Path
import google.generativeai as genai
from news_bot.settings import GOOGLE_API_KEY

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

POSTS_DIR = r"c:\Users\OlgaKorniichuk\Documents\antiGravity Projects\Facebok AI.corelogic\blog\posts"

def extract_article_content(html_content):
    """Extract article title and body content from HTML"""
    
    # Extract title
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
    title = title_match.group(1) if title_match else "Article"
    
    # Extract article body (between <div class="article-body"> and </div>)
    body_match = re.search(r'<div class="article-body"[^>]*>(.*?)</div>\s*<hr', html_content, re.DOTALL)
    body_html = body_match.group(1) if body_match else ""
    
    # Strip HTML tags for analysis
    clean_text = re.sub(r'<[^>]+>', ' ', body_html)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    return title, clean_text

def generate_insights(title, content):
    """Use Gemini to generate both TL;DR summary AND Editorial Prospect"""
    
    prompt = f"""
    Analyze this blog post and generate TWO distinct outputs:
    
    1. TL;DR Summary (3 bullet points)
    2. Editorial Prospect (A short, punchy opinion/take on why this matters)
    
    Title: {title}
    
    Content: {content[:3000]}
    
    OUTPUT 1: TL;DR
    - Exactly 2-3 bullet points
    - Each bullet ONE sentence (15-20 words max)
    - Actionable insights or shocking facts
    - Plain text (no bullet symbols)
    
    OUTPUT 2: EDITORIAL TAKE
    - A 2-3 sentence paragraph (50-70 words)
    - Written in a "no-nonsense, insider" voice
    - Explain the "Real Truth" or "Hidden Implication" of this news
    - Start with a strong hook like "Let's be real," "Here's the thing," or "The bottom line is"
    - Focus on the business/AI intersection
    
    FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
    || TLDR ||
    Bullet 1 text
    Bullet 2 text
    Bullet 3 text
    || EDITORIAL ||
    Your editorial paragraph text here...
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Parse the response
        tldr_text = ""
        editorial_text = ""
        
        if "|| TLDR ||" in text and "|| EDITORIAL ||" in text:
            parts = text.split("|| EDITORIAL ||")
            tldr_part = parts[0].replace("|| TLDR ||", "").strip()
            editorial_text = parts[1].strip()
            
            # Process TLDR bullets
            bullets = [line.strip() for line in tldr_part.split('\n') if line.strip()]
            
            if bullets:
                tldr_html = "<ul style='margin: 0; padding-left: 1.5rem; line-height: 1.8;'>"
                for bullet in bullets[:3]:
                    # Clean bullets
                    bullet = re.sub(r'^[•\-\*]\s*', '', bullet)
                    tldr_html += f"<li style='margin-bottom: 0.75rem;'>{bullet}</li>"
                tldr_html += "</ul>"
                tldr_text = tldr_html
                
        return tldr_text, editorial_text
            
    except Exception as e:
        print(f"[ERROR] Gemini error: {e}")
        return None, None

def update_html_content(html_content, new_tldr, new_editorial):
    """Replace both the TL;DR section and the Editorial/Author Bio section"""
    
    # 1. Update TL;DR
    # Pattern to find the quick-summary div content
    tldr_pattern = r'(<div class="quick-summary">.*?<strong>💡 Key TakeAways:</strong>)(.*?)(</div>)'
    
    def tldr_replace(match):
        # Keep opening div and header, replace content, keep closing div
        return f'{match.group(1)}\n{new_tldr}\n{match.group(3)}'
    
    # Note: re.DOTALL is needed for multi-line matching
    updated_html = re.sub(tldr_pattern, tldr_replace, html_content, flags=re.DOTALL)
    
    # 2. Update Editorial/Author Bio
    # Find the author-bio div
    bio_pattern = r'(<!-- Editorial Attribution.*?-->\s*<div class="author-bio".*?>)(.*?)(</div>)'
    
    new_bio_content = f'''
            <div style="display: flex; align-items: flex-start; gap: 1.5rem;">
                <img src="../assets/brand-logo.png" alt="AI Core Logic" style="width: 60px; height: 60px; object-fit: contain;">
                <div>
                    <h4 style="margin: 0 0 0.5rem 0; font-family: 'Outfit', sans-serif; color: #00F0FF; font-size: 1.1rem;">AI Core Logic Editorial</h4>
                    <p style="margin: 0; font-size: 0.95rem; color: #94A3B8; line-height: 1.6; font-style: italic;">"{new_editorial}"</p>
                </div>
            </div>'''
            
    def bio_replace(match):
        return f'{match.group(1)}{new_bio_content}{match.group(3)}'
        
    updated_html = re.sub(bio_pattern, bio_replace, updated_html, flags=re.DOTALL)
    
    return updated_html

def process_blog_post(filepath):
    """Process a single blog post"""
    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract article content
        title, body = extract_article_content(content)
        
        if not body:
            print(f"[SKIP] {filepath.name} - Could not extract content")
            return False
        
        # Generate Insights
        print(f"[PROCESSING] {filepath.name}...")
        print(f"   Title: {title[:60]}...")
        
        tldr_html, editorial_text = generate_insights(title, body)
        
        if not tldr_html or not editorial_text:
            print(f"[ERROR] Failed to generate insights")
            return False
        
        # Update HTML
        updated_content = update_html_content(content, tldr_html, editorial_text)
        
        # Only write if changes were made
        if updated_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"[OK] Updated with TL;DR and Editorial Prospect")
            return True
        else:
            print(f"[SKIP] No changes needed or pattern mismatch")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error processing {filepath}: {e}")
        return False

def main():
    """Process all blog posts"""
    posts_dir = Path(POSTS_DIR)
    html_files = sorted(posts_dir.glob("*.html"))
    
    print(f"Found {len(html_files)} blog posts to process...")
    print(f"Generating TL;DRs and Editorial Prospects...\n")
    print("="*60)
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for i, filepath in enumerate(html_files, 1):
        print(f"\n[{i}/{len(html_files)}] {filepath.name}")
        result = process_blog_post(filepath)
        
        if result:
            updated_count += 1
        elif result is False:
            error_count += 1
        else:
            skipped_count += 1
    
    print(f"\n{'='*60}")
    print(f"[OK] Updated: {updated_count} posts")
    print(f"[ERROR] Errors: {error_count} posts")
    print(f"[SKIP] Skipped: {skipped_count} posts")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
