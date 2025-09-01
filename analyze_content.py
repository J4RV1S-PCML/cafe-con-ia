#!/usr/bin/env python3
"""
Análisis de categorías disponibles en el contenido IA
"""
import yaml
from collections import defaultdict

def analyze_categories():
    print("📊 ANÁLISIS DE CATEGORÍAS DE CONTENIDO IA")
    print("=" * 50)
    
    content_files = ['tips.yml', 'trends.yml', 'automations.yml', 'videos.yml']
    
    for file_name in content_files:
        print(f"\n📁 {file_name.upper()}")
        print("-" * 30)
        
        try:
            with open(f'/workspaces/cafe-con-ia/{file_name}', 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
                
            if not content:
                print("  ⚠️  Sin contenido")
                continue
            
            # Contar categorías
            categories = defaultdict(int)
            total_items = len(content)
            
            for item in content:
                category = item.get('category', 'sin-categoria')
                categories[category] += 1
            
            print(f"  📈 Total items: {total_items}")
            print(f"  🏷️  Categorías encontradas:")
            
            for category, count in sorted(categories.items()):
                percentage = (count / total_items) * 100
                print(f"    • {category}: {count} items ({percentage:.1f}%)")
        
        except FileNotFoundError:
            print(f"  ❌ Archivo no encontrado: {file_name}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n✅ Análisis completado")

if __name__ == "__main__":
    analyze_categories()
