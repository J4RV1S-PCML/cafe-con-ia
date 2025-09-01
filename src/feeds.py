import feedparser, datetime, yaml
from src.simple_security import SimpleSecurityGuard

def load_feeds(path="rss_sources.yml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def top10():
    """
    Obtiene las top 10 noticias con validación de seguridad integrada
    """
    # 🔒 Inicializar monitor de seguridad
    security_monitor = RSSSecurityMonitor()
    
    urls = load_feeds()
    items = []
    
    print("🔍 Procesando feeds RSS con validación de seguridad...")
    
    for url in urls:
        try:
            # Validar fuente RSS antes de procesarla
            validation_result = security_monitor.validate_rss_source(url)
            
            if not validation_result['is_safe']:
                print(f"🚨 Fuente RSS bloqueada por seguridad: {url}")
                continue
            
            # Procesar feed si es seguro
            feed = feedparser.parse(url)
            
            # Validar contenido del feed
            feed_items = []
            for entry in feed.entries:
                feed_items.append({
                    'title': getattr(entry, 'title', ''),
                    'description': getattr(entry, 'summary', '') or getattr(entry, 'description', ''),
                    'link': getattr(entry, 'link', ''),
                    'published_parsed': getattr(entry, 'published_parsed', None)
                })
            
            # Aplicar filtrado de seguridad al contenido
            safe_items = security_monitor.scan_rss_feed_content(feed_items)
            
            # Convertir de vuelta al formato original
            for safe_item, original_entry in zip(safe_items, feed.entries):
                original_entry.title = safe_item['title']
                original_entry.summary = safe_item['description']
                original_entry.link = safe_item['link']
                items.append(original_entry)
                
        except Exception as e:
            print(f"⚠️  Error procesando feed {url}: {e}")
            continue
    
    # fallback fecha
    for e in items:
        if not e.get('published_parsed'):
            e.published_parsed = datetime.datetime.utcnow().timetuple()
    
    items = sorted(items, key=lambda e: e.published_parsed, reverse=True)[:10]
    
    result = []
    for e in items:
        # Validación final de seguridad para cada item
        title = getattr(e, 'title', '')
        link = getattr(e, 'link', '')
        summary = (getattr(e, 'summary', '') or getattr(e, 'description', ''))[:180] + "…"
        
        # Escaneo final de seguridad
        is_title_safe, safe_title, _ = security_monitor.security_guard.scan_content(title, 'final_title')
        is_link_safe, safe_link, _ = security_monitor.security_guard.scan_content(link, 'final_link')
        is_summary_safe, safe_summary, _ = security_monitor.security_guard.scan_content(summary, 'final_summary')
        
        if is_title_safe and is_link_safe and is_summary_safe:
            result.append({
                "title": safe_title,
                "link": safe_link,
                "summary": safe_summary
            })
    
    print(f"✅ Feeds procesados: {len(result)} noticias seguras seleccionadas")
    return result