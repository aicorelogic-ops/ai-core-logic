import os
import re
import time
import google.generativeai as genai
from pathlib import Path
from news_bot.settings import GOOGLE_API_KEY

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

POSTS_DIR = Path("blog/posts")
STATIC_TEXT = "We analyze the intersection of logistics, automation, and AI to deliver actionable insights for modern businesses. No hype, just practical strategy."

def generate_prospect(content):
    """Generates a unique editorial prospect based on the article content."""
    prompt = f"""
    Analyze this blog post content and generate a 'Editorial Prospect' (Unique Insight) for the author bio section.
    
    CRITICAL INSTRUCTIONS:
    - Write specific to THIS article's topic.
    - Length: 2-3 sentences (50-70 words max).
    - Tone: No-nonsense, insider, "Real Truth", "Hidden Implication".
    - Start with a hook like "Let's be real,", "Here's the thing,", "The bottom line is,", "Reality check:", etc.
    - Do NOT use "We analyze..." or generic company slogans.
    - Return ONLY the text.

    CONTENT:
    {content[:3000]}... (truncated)
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"  [AI ERROR] {e}")
        return None

def main():
    if not POSTS_DIR.exists():
        print(f"Directory not found: {POSTS_DIR}")
        return

    files = list(POSTS_DIR.glob("*.html"))
    print(f"Scanning {len(files)} posts for static editorial text...")

    updated_count = 0
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for the static text (or a substantial part of it to be safe)
            if "No hype, just practical strategy" in content:
                print(f"\nProcessing: {filepath.name}")
                
                # Extract body text for context
                body_match = re.search(r'<div class="article-body".*?>([\s\S]*?)<hr', content)
                clean_body = ""
                if body_match:
                    raw_html = body_match.group(1)
                    clean_body = re.sub(r'<[^>]+>', ' ', raw_html).strip()
                else:
                    # Fallback: just use what we can find
                    clean_body = re.sub(r'<[^>]+>', ' ', content[:4000])

                # Generate new text
                new_prospect = generate_prospect(clean_body)
                
                if new_prospect:
                    # Replace the specific static block
                    # The static text is usually inside a <p> tag in the author-bio div
                    # We'll use a direct string replace for the core static sentence to avoid regex complexity issues
                    new_content = content.replace(STATIC_TEXT, new_prospect)
                    
                    # Safety check: if exact string match failed (maybe whitespace diffs), try a more loose replacement
                    if new_content == content:
                         # Try replacing just the "No hype..." part if the full string failed
                         print("  [WARN] Exact string match failed, trying loose match...")
                         loose_static = "We analyze the intersection of logistics, automation, and AI to deliver actionable insights for modern businesses. No hype, just practical strategy."
                         new_content = content.replace(loose_static, new_prospect)

                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"  [SUCCESS] Updated editorial prospect.")
                        updated_count += 1
                        # Sleep briefly to avoid rate limits
                        time.sleep(2) 
                    else:
                        print(f"  [FAIL] Could not replace text in {filepath.name}")
                else:
                    print(f"  [SKIP] AI generation failed.")
            else:
                # print(f".", end="", flush=True) # Progress dot for skipped
                pass

        except Exception as e:
            print(f"Error processing {filepath.name}: {e}")

    print(f"\n\nDone! Repalced editorial text in {updated_count} files.")

if __name__ == "__main__":
    main()
