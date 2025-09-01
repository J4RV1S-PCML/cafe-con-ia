#!/usr/bin/env python3
"""
Demo del sistema de rotación automática de contenido IA
"""
import sys
import os
sys.path.append('/workspaces/cafe-con-ia')

from src.content_rotator import ContentRotator

def demo_rotation():
    print("🤖 DEMO: Sistema de Rotación Automática de Contenido IA")
    print("=" * 60)
    
    # Inicializar rotador
    rotator = ContentRotator("/workspaces/cafe-con-ia")
    
    # Mostrar estadísticas
    stats = rotator.generate_statistics()
    print("\n📊 Estadísticas de Contenido Disponible:")
    total_items = 0
    for content_type, data in stats.items():
        items = data['total_items']
        categories = len(data['categories'])
        total_items += items
        print(f"  ✅ {content_type.title()}: {items} items en {categories} categorías")
    
    print(f"\n🎯 Total de contenido: {total_items} items")
    print("\n🔄 Generando 3 rotaciones de ejemplo...\n")
    
    # Generar rotaciones de ejemplo
    for i in range(3):
        print(f"📰 ROTACIÓN {i+1}")
        print("-" * 30)
        
        fresh_content = rotator.get_fresh_newsletter_content()
        
        for content_type, items in fresh_content.items():
            print(f"\n{content_type.upper()}:")
            for idx, item in enumerate(items, 1):
                category = item.get('category', 'general')
                title = item.get('title', 'Sin título')[:50] + '...' if len(item.get('title', '')) > 50 else item.get('title', 'Sin título')
                print(f"  {idx}. [{category}] {title}")
        
        print()
    
    print("✅ DEMO COMPLETADA")
    print("💡 El sistema funcionará automáticamente en cada ejecución del newsletter")

if __name__ == "__main__":
    demo_rotation()
