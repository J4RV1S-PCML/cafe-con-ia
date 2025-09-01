#!/usr/bin/env python3
"""
RSS Security Monitor - Sistema de monitoreo de seguridad para fuentes RSS
Valida y filtra contenido RSS para prevenir ataques de prompt injection
"""
import re
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import urllib.parse
from src.security_guard import PromptInjectionGuard


class RSSSecurityMonitor:
    """
    Monitorea la seguridad de las fuentes RSS y valida el contenido entrante
    """
    
    def __init__(self):
        self.security_guard = PromptInjectionGuard()
        self.trusted_domains = self._setup_trusted_domains()
        self.quarantine_log = []
        self.validation_stats = {
            'total_processed': 0,
            'threats_blocked': 0,
            'sources_blocked': 0,
            'last_scan': None
        }
    
    def _setup_trusted_domains(self) -> List[str]:
        """Lista de dominios confiables para fuentes RSS"""
        return [
            # Fuentes académicas y de investigación
            'arxiv.org', 'nature.com', 'science.org', 'mit.edu',
            'stanford.edu', 'berkeley.edu', 'deepmind.com',
            
            # Organizaciones de IA confiables
            'openai.com', 'anthropic.com', 'huggingface.co',
            'stability.ai', 'google.com', 'research.google',
            
            # Medios de comunicación establecidos
            'techcrunch.com', 'venturebeat.com', 'wired.com',
            'technologyreview.com', 'theguardian.com', 'nytimes.com',
            
            # Plataformas educativas
            'deeplearning.ai', 'coursera.org', 'kaggle.com',
            'machinelearningmastery.com', 'analyticsvidhya.com',
            
            # Comunidades técnicas establecidas
            'reddit.com', 'stackoverflow.com', 'github.com',
            'news.ycombinator.com'
        ]
    
    def validate_rss_source(self, rss_url: str) -> Dict[str, Any]:
        """
        Valida una fuente RSS antes de incluirla en el sistema
        
        Returns:
            Dict con información de validación y estado de seguridad
        """
        validation_result = {
            'url': rss_url,
            'is_safe': False,
            'trust_level': 'unknown',
            'threats': [],
            'recommendations': []
        }
        
        try:
            # Parsear URL
            parsed_url = urllib.parse.urlparse(rss_url)
            domain = parsed_url.netloc.lower()
            
            # Verificar protocolo
            if parsed_url.scheme not in ['http', 'https']:
                validation_result['threats'].append({
                    'type': 'invalid_protocol',
                    'severity': 'high',
                    'description': f'Protocolo no seguro: {parsed_url.scheme}'
                })
                return validation_result
            
            # Verificar dominio confiable
            is_trusted = any(trusted in domain for trusted in self.trusted_domains)
            if is_trusted:
                validation_result['trust_level'] = 'high'
                validation_result['is_safe'] = True
            else:
                validation_result['trust_level'] = 'low'
                validation_result['recommendations'].append(
                    'Dominio no está en lista de confianza - requiere validación manual'
                )
            
            # Verificar patrones sospechosos en URL
            suspicious_patterns = [
                r'\.tk$|\.ml$|\.ga$|\.cf$',  # TLD sospechosos
                r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',  # IP directa
                r'localhost|127\.0\.0\.1',  # URLs locales
                r'[^\w\-\.]',  # Caracteres raros en dominio
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, domain):
                    validation_result['threats'].append({
                        'type': 'suspicious_domain',
                        'severity': 'medium',
                        'description': f'Patrón sospechoso en dominio: {pattern}'
                    })
                    validation_result['is_safe'] = False
            
            # Verificar longitud anormal de URL
            if len(rss_url) > 500:
                validation_result['threats'].append({
                    'type': 'abnormal_url_length',
                    'severity': 'low',
                    'description': 'URL excesivamente larga'
                })
            
            # Si no hay amenazas críticas y es un dominio conocido, marcar como seguro
            critical_threats = [t for t in validation_result['threats'] if t['severity'] == 'high']
            if not critical_threats and (is_trusted or len(validation_result['threats']) == 0):
                validation_result['is_safe'] = True
            
        except Exception as e:
            validation_result['threats'].append({
                'type': 'parsing_error',
                'severity': 'high',
                'description': f'Error al procesar URL: {str(e)}'
            })
        
        return validation_result
    
    def scan_rss_feed_content(self, feed_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Escanea el contenido de un feed RSS en busca de amenazas
        """
        safe_items = []
        
        for item in feed_items:
            is_item_safe = True
            sanitized_item = item.copy()
            
            # Validar título
            if 'title' in item:
                is_safe, sanitized_title, threats = self.security_guard.scan_content(
                    item['title'], 'rss_title'
                )
                if not is_safe:
                    print(f"🚨 RSS: Título malicioso detectado: {item['title'][:50]}...")
                    is_item_safe = False
                sanitized_item['title'] = sanitized_title
            
            # Validar descripción/resumen
            if 'description' in item:
                is_safe, sanitized_desc, threats = self.security_guard.scan_content(
                    item['description'], 'rss_description'
                )
                if not is_safe:
                    print(f"🚨 RSS: Descripción maliciosa detectada en: {item.get('title', 'Sin título')}")
                    is_item_safe = False
                sanitized_item['description'] = sanitized_desc
            
            # Validar enlaces
            if 'link' in item:
                is_safe, sanitized_link, threats = self.security_guard.scan_content(
                    item['link'], 'rss_link'
                )
                if not is_safe:
                    print(f"🚨 RSS: Enlace malicioso detectado: {item['link']}")
                    is_item_safe = False
                sanitized_item['link'] = sanitized_link
            
            # Agregar a cuarentena si es peligroso
            if not is_item_safe:
                self.quarantine_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'item': item,
                    'reason': 'security_threat_detected'
                })
                self.validation_stats['threats_blocked'] += 1
            else:
                safe_items.append(sanitized_item)
            
            self.validation_stats['total_processed'] += 1
        
        self.validation_stats['last_scan'] = datetime.now().isoformat()
        return safe_items
    
    def validate_rss_sources_file(self, sources_file_path: str) -> Dict[str, Any]:
        """
        Valida todas las fuentes RSS en el archivo de configuración
        """
        import yaml
        
        validation_report = {
            'total_sources': 0,
            'safe_sources': 0,
            'unsafe_sources': 0,
            'unknown_sources': 0,
            'detailed_results': []
        }
        
        try:
            with open(sources_file_path, 'r', encoding='utf-8') as f:
                sources = yaml.safe_load(f)
            
            if not sources:
                return validation_report
            
            print("🔍 Validando fuentes RSS...")
            
            for source in sources:
                validation_result = self.validate_rss_source(source)
                validation_report['detailed_results'].append(validation_result)
                validation_report['total_sources'] += 1
                
                if validation_result['is_safe']:
                    validation_report['safe_sources'] += 1
                    status = "✅"
                elif validation_result['threats']:
                    validation_report['unsafe_sources'] += 1
                    status = "🚨"
                else:
                    validation_report['unknown_sources'] += 1
                    status = "⚠️"
                
                # Mostrar resumen por fuente
                domain = urllib.parse.urlparse(source).netloc
                threats_count = len(validation_result['threats'])
                print(f"  {status} {domain} - Amenazas: {threats_count}")
        
        except Exception as e:
            print(f"❌ Error validando fuentes RSS: {e}")
        
        return validation_report
    
    def generate_security_report(self) -> str:
        """Genera un reporte de seguridad en formato texto"""
        report = []
        report.append("🔒 REPORTE DE SEGURIDAD RSS")
        report.append("=" * 35)
        report.append(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Estadísticas generales
        report.append("📊 ESTADÍSTICAS:")
        report.append(f"  • Items procesados: {self.validation_stats['total_processed']}")
        report.append(f"  • Amenazas bloqueadas: {self.validation_stats['threats_blocked']}")
        report.append(f"  • Fuentes bloqueadas: {self.validation_stats['sources_blocked']}")
        report.append(f"  • Último escaneo: {self.validation_stats['last_scan'] or 'Nunca'}")
        report.append("")
        
        # Items en cuarentena
        if self.quarantine_log:
            report.append("🚨 ITEMS EN CUARENTENA:")
            recent_quarantine = self.quarantine_log[-5:]  # Últimos 5
            for item in recent_quarantine:
                title = item['item'].get('title', 'Sin título')[:50]
                report.append(f"  • {item['timestamp']}: {title}...")
            report.append("")
        
        # Recomendaciones
        report.append("💡 RECOMENDACIONES:")
        report.append("  • Revisar items en cuarentena regularmente")
        report.append("  • Actualizar lista de dominios confiables")
        report.append("  • Monitorear logs de seguridad")
        report.append("  • Implementar alertas automáticas")
        
        return "\n".join(report)
    
    def get_quarantine_items(self, limit: int = 10) -> List[Dict]:
        """Obtiene items en cuarentena para revisión manual"""
        return self.quarantine_log[-limit:] if self.quarantine_log else []
    
    def clear_quarantine(self) -> int:
        """Limpia la cuarentena y retorna cantidad de items removidos"""
        count = len(self.quarantine_log)
        self.quarantine_log.clear()
        return count


def validate_rss_security():
    """Función principal para validar la seguridad de las fuentes RSS"""
    monitor = RSSSecurityMonitor()
    
    # Validar archivo de fuentes RSS
    sources_file = '/workspaces/cafe-con-ia/rss_sources.yml'
    validation_report = monitor.validate_rss_sources_file(sources_file)
    
    print(f"\n📋 RESUMEN DE VALIDACIÓN RSS:")
    print(f"  Total fuentes: {validation_report['total_sources']}")
    print(f"  ✅ Seguras: {validation_report['safe_sources']}")
    print(f"  🚨 Peligrosas: {validation_report['unsafe_sources']}")
    print(f"  ⚠️  Desconocidas: {validation_report['unknown_sources']}")
    
    # Mostrar fuentes problemáticas
    unsafe_sources = [r for r in validation_report['detailed_results'] if not r['is_safe']]
    if unsafe_sources:
        print(f"\n🚨 FUENTES CON PROBLEMAS:")
        for source in unsafe_sources:
            domain = urllib.parse.urlparse(source['url']).netloc
            threats = len(source['threats'])
            print(f"  • {domain}: {threats} amenazas detectadas")
    
    return validation_report


if __name__ == "__main__":
    validate_rss_security()
