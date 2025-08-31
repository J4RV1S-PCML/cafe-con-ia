import feedparser, datetime, yaml

def load_feeds(path="rss_sources.yml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def top10():
    urls = load_feeds()
    items = []
    for url in urls:
        feed = feedparser.parse(url)
        items += feed.entries
    # fallback fecha
    for e in items:
        if not e.get('published_parsed'):
            e.published_parsed = datetime.datetime.utcnow().timetuple()
    items = sorted(items, key=lambda e: e.published_parsed, reverse=True)[:10]
    return [
        {
            "title": e.title,
            "link": e.link,
            "summary": (e.get('summary', '') or e.get('description', ''))[:180] + "…"
        }
        for e in items
    ]