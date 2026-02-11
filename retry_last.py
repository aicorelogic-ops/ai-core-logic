from news_bot.article_tracker import ArticleTracker
import os

def untrack_last():
    tracker = ArticleTracker()
    recent = tracker.list_all_articles()
    if not recent:
        print("No articles to untrack.")
        return

    last_article = recent[0] # Newest first
    print(f"Untracking: {last_article['title']}")
    
    # Get metadata to find file path
    info = tracker.get_article_info(last_article['url'])
    if info and 'blog_path' in info:
        path = info['blog_path']
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"Deleted file: {path}")
            except Exception as e:
                print(f"Error deleting file: {e}")
                
    tracker.remove_article(last_article['url'])

if __name__ == "__main__":
    untrack_last()
