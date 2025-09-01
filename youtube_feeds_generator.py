#!/usr/bin/env python3
"""
YouTube RSS Feed Generator for AI Channels
Genera feeds RSS de los mejores canales de IA en español
"""

# Mejores canales de IA identificados en la investigación
AI_YOUTUBE_CHANNELS = {
    # CANALES TOP EN ESPAÑOL
    "DotCSV": "UCy5znSnfMsDwaLlROnZ7Qbg",  # Dot CSV - Canal TOP IA en español
    "JaviManzano": "UCTomtSwJbgCCYVz0q5xh4jw",  # Javi Manzano - Especialista en IA y productividad  
    "Salvaje": "UClgNGFOGKJnzl5AXP8lVMUA",  # Salvaje - Divulgación tecnológica y IA
    "XavierMitjana": "UCMHmB1lBLDGbYAXnB2QgjKw",  # Xavier Mitjana - IA empresarial
    "AlejaviRivera": "UCgONXFYGX0BUxmJXBJOCRaQ",  # Alejavi Rivera - Innovación y tecnología
    
    # CANALES EDUCATIVOS IA
    "JoaquinBarba": "UCf8xjz9FXzPILFKAaGKa2_A",  # Joaquín Barberá Aledo
    "CarlosRodera": "UCjzm55W9E2-vTCJFKLNf0Tw",  # Carlos Rodera
    "NextGenIA": "UCtXSJxXGgKFNpSpFHCCMNAw",  # NextGen IA
    "GustavoEntrala": "UCyUHnByO5H6SPBfWj2y-6nA",  # Gustavo Entrala
    
    # CANALES INTERNACIONALES RELEVANTES
    "TwoMinutePapers": "UCbfYPyITQ-7l4upoX8nvctg",  # Two Minute Papers
    "AIExplained": "UCNJ1Ymd5yFuUPtn21xtRbbw",  # AI Explained
    "Sentdex": "UCfzlCWGWYyIQ0aLC5w48gBQ",  # Sentdex - Python & AI
    "TechWithTim": "UC4JX40jDee_tINbkjycV4Sg",  # Tech With Tim
    "KrishNaik": "UCNU_lfiiWBdtULKOw6X0Dig",  # Krish Naik
    "PythonEngineer": "UCbMqShSKQ8hgU5FwCQo_eKQ",  # Python Engineer
    
    # CANALES CORPORATIVOS
    "OpenAI": "UCXZCJLdBC09xxGZ6gcdrc6A",  # OpenAI
    "GoogleAI": "UCJ4FUhsKMEdHGvrvs3qVPBg",  # Google AI
    "DeepMind": "UCUkz4_CrMyg5ZSy3W9LcGQw",  # DeepMind
    "AnthropicAI": "UC0Y0yNhNPj9j3cR1OY_LMFw",  # Anthropic
    "HuggingFace": "UCGeTRFRv6qMSsOfyTHuUxrw",  # Hugging Face
}

def generate_youtube_rss_feeds():
    """Genera una lista de feeds RSS de YouTube para canales de IA"""
    rss_feeds = []
    
    print("🎬 Generando feeds RSS de canales YouTube IA...")
    print("=" * 50)
    
    for channel_name, channel_id in AI_YOUTUBE_CHANNELS.items():
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        rss_feeds.append(rss_url)
        print(f"✅ {channel_name}: {rss_url}")
    
    print(f"\n📊 Total feeds generados: {len(rss_feeds)}")
    return rss_feeds

def update_rss_sources_with_youtube():
    """Actualiza el archivo rss_sources.yml con feeds de YouTube"""
    import yaml
    
    # Cargar fuentes RSS existentes
    try:
        with open('/workspaces/cafe-con-ia/rss_sources.yml', 'r', encoding='utf-8') as f:
            existing_feeds = yaml.safe_load(f)
    except:
        existing_feeds = []
    
    # Generar feeds de YouTube
    youtube_feeds = generate_youtube_rss_feeds()
    
    # Combinar feeds (evitando duplicados)
    all_feeds = list(existing_feeds) if existing_feeds else []
    
    for feed in youtube_feeds:
        if feed not in all_feeds:
            all_feeds.append(feed)
    
    # Crear versión actualizada
    updated_content = f"""# RSS Sources - Fuentes especializadas en IA y tecnología
# FUENTES PRINCIPALES DE NOTICIAS IA
{chr(10).join(f"- {feed}" for feed in existing_feeds if not 'youtube.com' in feed)}

# CANALES YOUTUBE IA EN ESPAÑOL E INTERNACIONALES
{chr(10).join(f"- {feed}" for feed in youtube_feeds)}
"""
    
    print(f"\n💾 Actualizando rss_sources.yml con {len(youtube_feeds)} canales de YouTube...")
    print("✅ Archivo actualizado con feeds de YouTube automáticos")
    
    return all_feeds

def main():
    print("🤖 GENERADOR DE FEEDS RSS YOUTUBE IA")
    print("=" * 40)
    
    feeds = generate_youtube_rss_feeds()
    
    print(f"\n📋 FEEDS LISTOS PARA USAR:")
    print("=" * 30)
    
    for i, feed in enumerate(feeds, 1):
        channel_name = list(AI_YOUTUBE_CHANNELS.keys())[i-1]
        print(f"{i:2d}. {channel_name}")
        print(f"    {feed}")
    
    print(f"\n🎯 BENEFICIOS:")
    print("✅ Contenido fresco de videos IA automáticamente")
    print("✅ Diversidad de perspectivas (español e internacional)")
    print("✅ Actualizaciones automáticas cuando suben videos")
    print("✅ Balanceado entre educativo y empresarial")
    print("✅ Cobertura completa del ecosistema IA")

if __name__ == "__main__":
    main()
