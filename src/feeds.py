import feedparser, datetime, urllib.request, yaml

def fetch(url: str):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return feedparser.parse(urllib.request.urlopen(req).read())

def load_feeds(path="rss_sources.yml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def top10():
    urls = load_feeds()
    items = []
    for u in urls:
        items += fetch(u).entries
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