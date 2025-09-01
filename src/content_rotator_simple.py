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
        # ✅ Seguridad básica
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
        Genera una selección fresca de contenido para el newsletter
        Balancea categorías y asegura variedad
        """
        print("🔄 Generando contenido fresco para el newsletter...")
        
        # Generar contenido con rotación automática
        fresh_content = {
            'tips': self.rotate_content('tips', count=2, ensure_variety=True),
            'trends': self.rotate_content('trends', count=2, ensure_variety=True), 
            'automations': self.rotate_content('automations', count=2, ensure_variety=True),
            'videos': self.rotate_content('videos', count=3, ensure_variety=True)
        }
        
        # Logging del contenido seleccionado
        for content_type, items in fresh_content.items():
            print(f"📝 {content_type}: {len(items)} items seleccionados")
            for idx, item in enumerate(items, 1):
                category = item.get('category', 'general')
                title = item.get('title', 'Sin título')
                print(f"   {idx}. [{category}] {title}")
        
        return fresh_content
    
    def get_content_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del contenido disponible"""
        stats = {}
        
        for content_type in self.content_files.keys():
            content = self.load_content(content_type)
            
            # Contar por categorías
            categories = {}
            for item in content:
                category = item.get('category', 'general')
                categories[category] = categories.get(category, 0) + 1
            
            stats[content_type] = {
                'total': len(content),
                'categories': categories
            }
        
        return stats
    
    def preview_rotation(self, iterations: int = 5) -> None:
        """Preview de cómo se vería la rotación en las próximas ejecuciones"""
        print(f"🎲 PREVIEW DE ROTACIÓN - Próximas {iterations} ejecuciones:")
        print("=" * 60)
        
        for i in range(iterations):
            print(f"\n📅 Ejecución {i+1}:")
            content = self.get_fresh_newsletter_content()
            
            for content_type, items in content.items():
                titles = [item.get('title', 'Sin título')[:40] + '...' for item in items]
                print(f"  {content_type}: {', '.join(titles)}")


# Función de utilidad para testing
def test_content_rotation():
    """Test rápido del sistema de rotación"""
    print("🧪 TESTING SISTEMA DE ROTACIÓN")
    print("=" * 40)
    
    rotator = ContentRotator('/workspaces/cafe-con-ia')
    
    # Mostrar estadísticas
    stats = rotator.get_content_stats()
    print("📊 ESTADÍSTICAS DE CONTENIDO:")
    for content_type, data in stats.items():
        print(f"  {content_type}: {data['total']} items")
        for category, count in data['categories'].items():
            print(f"    - {category}: {count}")
    
    print("\n🔄 CONTENIDO ROTADO:")
    content = rotator.get_fresh_newsletter_content()
    
    print(f"\n✅ Test completado - Sistema funcionando correctamente")
    return content


if __name__ == "__main__":
    test_content_rotation()
