"""
Script to update all existing blog posts with new TL;DR and footer design.
Applies the improvements made to the blog template to all existing posts.
"""

import os
import re
from pathlib import Path

POSTS_DIR = r"c:\Users\OlgaKorniichuk\Documents\antiGravity Projects\Facebok AI.corelogic\blog\posts"

def update_tldr_section(html_content):
    """Replace old TL;DR with new format (placeholder for now)"""
    
    # Old TL;DR pattern
    old_tldr_pattern = r'<div class="quick-summary">\s*<strong>TL;DR:</strong>\s*<p>Our deep analysis.*?</p>\s*</div>'
    
    # New TL;DR with placeholder
    new_tldr = '''<div class="quick-summary">
            <strong>💡 Key TakeAways:</strong> 
            <p>Key insights and actionable takeaways from this analysis to help you stay ahead in the AI landscape.</p>
        </div>'''
    
    # Replace
    updated_html = re.sub(old_tldr_pattern, new_tldr, html_content, flags=re.DOTALL)
    
    return updated_html

def update_author_bio(html_content):
    """Replace old circular logo author bio with new simplified design"""
    
    # Old author bio pattern (with circular logo)
    old_bio_pattern = r'<!-- Author Bio Section -->.*?<div class="author-bio".*?</div>\s*</div>'
    
    # New simplified bio
    new_bio = '''<!-- Editorial Attribution (Simplified) -->
        <div class="author-bio" style="background: #0F1419; padding: 2rem; border-radius: 8px; border-left: 4px solid #00F0FF;">
            <div>
                <h4 style="margin: 0 0 0.75rem 0; font-family: 'Outfit', sans-serif; color: #00F0FF; font-size: 1.1rem;">📊 AI Core Logic Editorial</h4>
                <p style="margin: 0; font-size: 0.95rem; color: #94A3B8; line-height: 1.6;">We analyze the intersection of logistics, automation, and AI to deliver actionable insights for modern businesses. No hype, just practical strategy.</p>
            </div>
        </div>'''
    
    # Replace
    updated_html = re.sub(old_bio_pattern, new_bio, html_content, flags=re.DOTALL)
    
    return updated_html

def update_blog_post(filepath):
    """Update a single blog post file"""
    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply updates
        content = update_tldr_section(content)
        content = update_author_bio(content)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"[ERROR] Error updating {filepath}: {e}")
        return False

def main():
    """Update all blog posts"""
    posts_dir = Path(POSTS_DIR)
    html_files = list(posts_dir.glob("*.html"))
    
    print(f"Found {len(html_files)} blog posts to update...\n")
    
    updated_count = 0
    skipped_count = 0
    
    for filepath in html_files:
        filename = filepath.name
        if update_blog_post(filepath):
            print(f"[OK] Updated: {filename}")
            updated_count += 1
        else:
            print(f"[SKIP] Skipped: {filename} (no changes needed)")
            skipped_count += 1
    
    print(f"\n{'='*60}")
    print(f"[OK] Updated: {updated_count} posts")
    print(f"[SKIP] Skipped: {skipped_count} posts")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
