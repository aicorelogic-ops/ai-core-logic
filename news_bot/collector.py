import feedparser
from datetime import datetime, timedelta
from .settings import RSS_FEEDS, KEYWORDS

class NewsCollector:
    def __init__(self):
        self.feeds = RSS_FEEDS

    def fetch_news(self, hours_back=72):
        """Fetch news from the last N hours."""
        recent_news = []
        time_threshold = datetime.now() - timedelta(hours=hours_back)

        for feed_url in self.feeds:
            print(f"Checking {feed_url}...")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries:
                # Check date
                published = getattr(entry, "published_parsed", None)
                if published:
                    pub_date = datetime(*published[:6])
                    if pub_date < time_threshold:
                        continue
                
                # Check keywords
                title = entry.title.lower()
                summary = getattr(entry, "summary", "").lower()
                
                # Image Extraction
                image_url = None
                if "media_content" in entry:
                    image_url = entry.media_content[0]["url"]
                elif "media_thumbnail" in entry:
                    image_url = entry.media_thumbnail[0]["url"]
                elif "links" in entry:
                    for link in entry.links:
                        if link.rel == "enclosure" and "image" in link.type:
                            image_url = link.href
                            break
                
                if any(kw in title or kw in summary for kw in KEYWORDS):
                    recent_news.append({
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.summary,
                        "published": pub_date,
                        "image_url": image_url
                    })
        
        return recent_news

if __name__ == "__main__":
    collector = NewsCollector()
    news = collector.fetch_news()
    print(f"Found {len(news)} relevant articles.")
    for n in news:
        print(f"- {n['title']}")
