"""
Seguridad Básica para Newsletter - Solo lo esencial
"""
import html
import urllib.parse

class SimpleSecurityGuard:
    """Seguridad mínima necesaria para el newsletter"""
    
    # Dominios confiables para RSS
    TRUSTED_DOMAINS = [
        'techcrunch.com', 'venturebeat.com', 'wired.com',
        'arxiv.org', 'nature.com', 'science.org',
        'openai.com', 'anthropic.com', 'huggingface.co',
        'deepmind.com', 'stability.ai', 'youtube.com',
        'mit.edu', 'stanford.edu', 'berkeley.edu'
    ]
    
    @staticmethod
    def is_safe_url(url):
        """Verificar si una URL es de un dominio confiable"""
        try:
            parsed = urllib.parse.urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remover www. si existe
            if domain.startswith('www.'):
                domain = domain[4:]
            
            return domain in SimpleSecurityGuard.TRUSTED_DOMAINS
        except:
            return False
    
    @staticmethod
    def sanitize_html(content):
        """Escapar HTML para prevenir inyección básica"""
        if not content:
            return ""
        return html.escape(str(content))
    
    @staticmethod
    def validate_content(item):
        """Validar que un item de contenido sea seguro"""
        if not isinstance(item, dict):
            return False
        
        # Verificar campos requeridos
        required_fields = ['title', 'link']
        if not all(field in item for field in required_fields):
            return False
        
        # Verificar URL
        if not SimpleSecurityGuard.is_safe_url(item['link']):
            return False
        
        # Sanitizar contenido de texto
        item['title'] = SimpleSecurityGuard.sanitize_html(item['title'])
        if 'description' in item:
            item['description'] = SimpleSecurityGuard.sanitize_html(item['description'])
        
        return True

def validate_environment():
    """Validar que las variables de entorno estén configuradas"""
    import os
    
    required_vars = ['GMAIL_USER', 'GMAIL_PASS', 'RECIPIENTS']
    missing = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        raise ValueError(f"Variables de entorno faltantes: {', '.join(missing)}")
    
    print("✅ Variables de entorno validadas")

# Función simple para usar en el proyecto
def secure_content(content_list):
    """Aplicar seguridad básica a una lista de contenido"""
    guard = SimpleSecurityGuard()
    safe_content = []
    
    for item in content_list:
        if guard.validate_content(item):
            safe_content.append(item)
        else:
            print(f"⚠️ Contenido filtrado: {item.get('title', 'Sin título')}")
    
    return safe_content
