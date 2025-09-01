#!/usr/bin/env python3
"""
Content Rotator - Sistema de rotación automática de contenido IA
Selecciona contenido aleatorio de las bases de datos YAML expandidas
para mantener el newsletter fresco y variado.
"""
import yaml
import random
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from src.simple_security import SimpleSecurityGuard


class ContentRotator:
    """Maneja la rotación automática de contenido para el newsletter"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.content_files = {
            'tips': 'tips.yml',
            'trends': 'trends.yml', 
            'automations': 'automations.yml',
            'videos': 'videos.yml'
        }
        # 🔒 Seguridad básica
        self.security_guard = SimpleSecurityGuard()
        print("✅ Sistema de rotación iniciado con seguridad básica")
        
    def load_content(self, content_type: str) -> List[Dict[str, Any]]:
        """Carga el contenido desde archivo YAML con validación básica"""
        file_path = self.base_path / self.content_files[content_type]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
                if content is None:
                    return []
                
                if not isinstance(content, list):
                    return []
                
                # ✅ Validación básica de seguridad
                safe_content = []
                
                for item in content:
                    if self.security_guard.validate_content(item):
                        safe_content.append(item)
                    else:
                        print(f"⚠️ Item filtrado en {content_type}: {item.get('title', 'Sin título')}")
                
                print(f"✅ {content_type}: {len(safe_content)}/{len(content)} items válidos")
                return safe_content
                
        except FileNotFoundError:
            print(f"⚠️  Archivo no encontrado: {file_path}")
            return []
        except Exception as e:
            print(f"❌ Error al leer YAML {file_path}: {e}")
            return []
                    
                    # Validar título
                    if 'title' in item:
                        is_safe, sanitized_title, threats = self.security_guard.scan_content(
                            item['title'], f'{content_type}_title'
                        )
                        if not is_safe:
                            print(f"⚠️  Amenaza detectada en título: {item['title'][:50]}...")
                            item_safe = False
                        sanitized_item['title'] = sanitized_title
                        threats_found += len(threats)
                    
                    # Validar descripción
                    if 'desc' in item:
                        is_safe, sanitized_desc, threats = self.security_guard.scan_content(
                            item['desc'], f'{content_type}_desc'
                        )
                        if not is_safe:
                            print(f"⚠️  Amenaza detectada en descripción: {item.get('title', 'Sin título')}")
                            item_safe = False
                        sanitized_item['desc'] = sanitized_desc
                        threats_found += len(threats)
                    
                    # Validar enlaces
                    if 'link' in item:
                        is_safe, sanitized_link, threats = self.security_guard.scan_content(
                            item['link'], f'{content_type}_link'
                        )
                        if not is_safe:
                            print(f"🚨 Enlace malicioso detectado y removido: {item['link']}")
                            item_safe = False
                        sanitized_item['link'] = sanitized_link
                        threats_found += len(threats)
                    
                    # Solo incluir items seguros
                    if item_safe:
                        safe_content.append(sanitized_item)
                    else:
                        print(f"🛡️  Item removido por seguridad: {item.get('title', 'Sin título')}")
                
                if threats_found > 0:
                    print(f"🔒 Seguridad {content_type}: {threats_found} amenazas detectadas y neutralizadas")
                
                return safe_content
                
        except FileNotFoundError:
            print(f"⚠️  Archivo no encontrado: {file_path}")
            return []
        except yaml.YAMLError as e:
            print(f"❌ Error al leer YAML {file_path}: {e}")
            return []
    
    def rotate_content(self, content_type: str, count: int = 2, 
                      category_filter: str = None, 
                      ensure_variety: bool = True) -> List[Dict[str, Any]]:
        """
        Selecciona contenido aleatorio con opciones avanzadas
        
        Args:
            content_type: Tipo de contenido (tips, trends, automations, videos)
            count: Número de elementos a seleccionar
            category_filter: Filtrar por categoría específica 
            ensure_variety: Asegurar variedad de categorías cuando sea posible
        """
        all_content = self.load_content(content_type)
        
        if not all_content:
            print(f"⚠️  No hay contenido disponible para {content_type}")
            return []
        
        # Filtrar por categoría si se especifica
        if category_filter:
            filtered_content = [
                item for item in all_content 
                if item.get('category') == category_filter
            ]
            if filtered_content:
                all_content = filtered_content
        
        # Si queremos asegurar variedad, intentamos seleccionar de diferentes categorías
        if ensure_variety and len(all_content) >= count:
            return self._select_with_variety(all_content, count)
        
        # Selección aleatoria simple
        selected_count = min(count, len(all_content))
        return random.sample(all_content, selected_count)
    
    def _select_with_variety(self, content: List[Dict], count: int) -> List[Dict]:
        """Selecciona contenido asegurando variedad de categorías cuando sea posible"""
        # Agrupar por categorías
        categories = {}
        for item in content:
            category = item.get('category', 'general')
            if category not in categories:
                categories[category] = []
            categories[category].append(item)
        
        selected = []
        categories_list = list(categories.keys())
        
        # Intentar seleccionar uno de cada categoría primero
        for i in range(count):
            if i < len(categories_list):
                category = categories_list[i]
                if categories[category]:
                    item = random.choice(categories[category])
                    selected.append(item)
                    categories[category].remove(item)
            else:
                # Si ya usamos todas las categorías, seleccionar de cualquiera
                remaining = []
                for cat_items in categories.values():
                    remaining.extend(cat_items)
                if remaining:
                    selected.append(random.choice(remaining))
        
        return selected
    
    def get_fresh_newsletter_content(self) -> Dict[str, List[Dict]]:
        """
        Genera una selección fresca de contenido para el newsletter con validación de seguridad
        Balancea categorías y asegura variedad
        """
        print("🔄 Generando contenido fresco con validación de seguridad...")
        
        # Generar contenido con rotación normal
        fresh_content = {
            'tips': self.rotate_content('tips', count=2, ensure_variety=True),
            'trends': self.rotate_content('trends', count=2, ensure_variety=True), 
            'automations': self.rotate_content('automations', count=2, ensure_variety=True),
            'videos': self.rotate_content('videos', count=3, ensure_variety=True)
        }
        
        # 🔒 VALIDACIÓN FINAL DE SEGURIDAD DEL NEWSLETTER COMPLETO
        print("🛡️  Realizando validación final de seguridad...")
        
        # Aplicar escaneo de seguridad a todo el contenido
        sanitized_content = self.security_guard.scan_newsletter_content(fresh_content)
        
        # Verificar que tenemos suficiente contenido después de la sanitización
        for content_type, items in sanitized_content.items():
            if content_type.startswith('_'):  # Skip metadatos de seguridad
                continue
                
            required_count = {
                'tips': 2, 'trends': 2, 'automations': 2, 'videos': 3
            }.get(content_type, 2)
            
            if len(items) < required_count:
                print(f"⚠️  Contenido insuficiente en {content_type} después de filtrado: {len(items)}/{required_count}")
                # Intentar obtener más contenido seguro
                additional_content = self.rotate_content(content_type, count=required_count*2, ensure_variety=False)
                for item in additional_content:
                    if len(items) >= required_count:
                        break
                    # Validar item adicional
                    item_data = {content_type: [item]}
                    validated_data = self.security_guard.scan_newsletter_content(item_data)
                    if validated_data.get(content_type) and len(validated_data[content_type]) > 0:
                        items.append(validated_data[content_type][0])
        
        # Mostrar resumen de seguridad
        if '_security' in sanitized_content:
            security_info = sanitized_content['_security']
            print(f"🔒 Resumen de seguridad:")
            print(f"   • Amenazas detectadas: {security_info.get('threats_detected', 0)}")
            print(f"   • Amenazas críticas: {security_info.get('threats_critical', 0)}")
            print(f"   • Amenazas altas: {security_info.get('threats_high', 0)}")
            print(f"   • Estado: {'✅ SEGURO' if security_info.get('is_safe', False) else '⚠️ AMENAZAS DETECTADAS'}")
            
            # Remover metadatos de seguridad del contenido final
            del sanitized_content['_security']
        
        return sanitized_content
    
    def get_themed_content(self, theme: str) -> Dict[str, List[Dict]]:
        """
        Genera contenido temático específico
        
        Temas disponibles:
        - 'development': Programación y desarrollo
        - 'business': Aplicaciones empresariales  
        - 'automation': Automatización y workflows
        - 'fundamentals': Conceptos básicos de IA
        - 'tools': Herramientas y aplicaciones
        """
        theme_mapping = {
            'development': ['development', 'programming', 'code'],
            'business': ['business', 'enterprise', 'marketing'],
            'automation': ['automation', 'workflow', 'no-code'],
            'fundamentals': ['fundamentals', 'education', 'learning'],
            'tools': ['tools', 'applications', 'platforms']
        }
        
        categories = theme_mapping.get(theme, [theme])
        result = {}
        
        for content_type in self.content_files.keys():
            themed_items = []
            for category in categories:
                items = self.rotate_content(content_type, count=1, category_filter=category)
                themed_items.extend(items)
            
            # Si no encontramos suficiente contenido temático, complementar con aleatorio
            if len(themed_items) < 2:
                additional = self.rotate_content(content_type, count=2-len(themed_items))
                themed_items.extend(additional)
            
            result[content_type] = themed_items[:2]  # Máximo 2 por sección
        
        return result
    
    def generate_statistics(self) -> Dict[str, Any]:
        """Genera estadísticas del contenido disponible"""
        stats = {}
        
        for content_type in self.content_files.keys():
            content = self.load_content(content_type)
            categories = {}
            
            for item in content:
                category = item.get('category', 'general')
                categories[category] = categories.get(category, 0) + 1
            
            stats[content_type] = {
                'total_items': len(content),
                'categories': categories,
                'most_common_category': max(categories.items(), key=lambda x: x[1])[0] if categories else None
            }
        
        return stats
    
    def preview_rotation(self, rotations: int = 3) -> None:
        """Previsualiza varias rotaciones para validar variedad"""
        print(f"🔄 Previsualizando {rotations} rotaciones de contenido:")
        print("=" * 60)
        
        for i in range(rotations):
            print(f"\n📰 **Rotación {i+1}**")
            content = self.get_fresh_newsletter_content()
            
            for content_type, items in content.items():
                print(f"\n**{content_type.title()}:**")
                for item in items:
                    category = item.get('category', 'general')
                    title = item.get('title', 'Sin título')
                    print(f"  • [{category}] {title}")


def main():
    """Función principal para testing y preview"""
    rotator = ContentRotator()
    
    print("🤖 Sistema de Rotación de Contenido IA")
    print("=====================================")
    
    # Mostrar estadísticas
    stats = rotator.generate_statistics()
    print("\n📊 **Estadísticas de Contenido:**")
    for content_type, data in stats.items():
        print(f"  {content_type}: {data['total_items']} items, "
              f"categorías: {len(data['categories'])}")
    
    # Previsualizar rotaciones
    rotator.preview_rotation(rotations=3)
    
    print("\n✅ Sistema de rotación listo!")
    print("💡 Tip: El contenido se rotará automáticamente en cada ejecución del newsletter")


if __name__ == "__main__":
    main()
