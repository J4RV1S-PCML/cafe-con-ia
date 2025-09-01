import feedparser, datetime, yaml
from src.simple_security import SimpleSecurityGuard

def load_feeds(path="rss_sources.yml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def top10():
    """
    Obtiene las top 10 noticias con validación de seguridad básica
    """
    urls = load_feeds()
    guard = SimpleSecurityGuard()
    items = []
    
    print("🔍 Procesando feeds RSS...")
    
    for url in urls:
        try:
            # Validar que la URL sea de un dominio confiable
            if not guard.is_safe_url(url):
                print(f"⚠️ URL no confiable omitida: {url}")
                continue
                
            print(f"📡 Procesando: {url}")
            feed = feedparser.parse(url)
            
            if hasattr(feed, 'entries'):
                for entry in feed.entries:
                    # Crear item básico
                    item = {
                        'title': entry.get('title', 'Sin título'),
                        'link': entry.get('link', ''),
                        'published': entry.get('published_parsed', None)
                    }
                    
                    # Validar contenido básico
                    if guard.validate_content(item):
                        items.append(item)
                        
        except Exception as e:
            print(f"❌ Error procesando {url}: {e}")
            continue
    
    # Ordenar por fecha y tomar top 10
    items.sort(key=lambda x: x.get('published') or datetime.datetime.now().timetuple(), reverse=True)
    top_items = items[:10]
    
    print(f"✅ {len(top_items)} noticias procesadas y validadas")
    return top_items
