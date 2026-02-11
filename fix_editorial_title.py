import os
from pathlib import Path

POSTS_DIR = r"c:\Users\OlgaKorniichuk\Documents\antiGravity Projects\Facebok AI.corelogic\blog\posts"

def main():
    posts_dir = Path(POSTS_DIR)
    html_files = sorted(posts_dir.glob("*.html"))
    
    count = 0
    target_string = "AI Core Logic Prospect"
    replacement_string = "AI Core Logic Editorial"
    
    print(f"Scanning {len(html_files)} files...")
    
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if target_string in content:
                new_content = content.replace(target_string, replacement_string)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"[FIXED] {filepath.name}")
                count += 1
            else:
                # Check if it already has the corect title
                if replacement_string in content:
                    print(f"[SKIP] Already correct: {filepath.name}")
                else:
                    print(f"[WARN] Target string not found in: {filepath.name}")
                    
        except Exception as e:
            print(f"[ERROR] {filepath.name}: {e}")

    print(f"\nValues updated: {count}")

if __name__ == "__main__":
    main()
