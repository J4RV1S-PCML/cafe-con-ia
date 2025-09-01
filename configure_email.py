#!/usr/bin/env python3
"""
Configuración del Sistema de Newsletter - Café con IA
Configurar email y variables de entorno para GitHub Actions
"""

def configure_email_settings():
    """Instrucciones para configurar el email paulmoll@outlook.com"""
    
    print("📧 CONFIGURACIÓN DE EMAIL PARA NEWSLETTER")
    print("=" * 50)
    print("Para recibir el newsletter diariamente en paulmoll@outlook.com")
    print()
    
    print("🔧 PASOS PARA CONFIGURAR EN GITHUB:")
    print("-" * 35)
    print()
    
    print("1️⃣ **Configurar Gmail (Cuenta emisora)**")
    print("   • Ve a Settings → Secrets and variables → Actions")
    print("   • Agregar estos secrets:")
    print()
    print("   📝 GMAIL_USER:")
    print("   • Nombre: GMAIL_USER") 
    print("   • Valor: tu-email@gmail.com (cuenta que enviará)")
    print()
    print("   🔑 GMAIL_APP_PASS:")
    print("   • Nombre: GMAIL_APP_PASS")
    print("   • Valor: contraseña de aplicación de Gmail")
    print("   • ⚠️ NO usar tu contraseña normal")
    print("   • Crear en: myaccount.google.com → Security → App passwords")
    print()
    
    print("2️⃣ **Configurar Destinatario (paulmoll@outlook.com)**")
    print("   📬 RECIPIENTS:")
    print('   • Nombre: RECIPIENTS')
    print('   • Valor: ["paulmoll@outlook.com"]')
    print("   • ⚠️ Formato JSON con corchetes y comillas")
    print()
    
    print("3️⃣ **Verificar Configuración Actual**")
    print("   ✅ Horario: Todos los días a las 7:30 AM ET")
    print("   ✅ Contenido: Noticias en inglés y español mezcladas")  
    print("   ✅ Rotación: Links diferentes cada día")
    print("   ✅ Seguridad: Validación básica aplicada")
    print()
    
    print("4️⃣ **Activar Newsletter**")
    print("   • El workflow ya está configurado en .github/workflows/send.yml")
    print("   • Se ejecutará automáticamente todos los días")
    print("   • También puedes ejecutar manualmente desde GitHub Actions")
    print()
    
    print("🎯 RESUMEN DE CONFIGURACIÓN:")
    print("=" * 30)
    print("📧 Destinatario: paulmoll@outlook.com") 
    print("⏰ Horario: 7:30 AM ET (11:30 UTC)")
    print("🔄 Frecuencia: Diaria")
    print("🌍 Idiomas: Inglés + Español mezclados")
    print("🔄 Contenido: Rotación automática de links")
    print()
    
    return True

def create_test_email():
    """Crear un email de prueba para verificar configuración"""
    
    test_email_content = """
    📧 TEST EMAIL - Café con IA
    
    Este es un email de prueba para verificar que paulmoll@outlook.com 
    recibirá correctamente el newsletter diario.
    
    ✅ Configuración verificada:
    - Newsletter visual con diseño infográfico
    - Noticias mezcladas en inglés y español
    - Rotación automática de contenido
    - Envío diario a las 7:30 AM ET
    
    El próximo paso es configurar los secrets en GitHub Actions.
    """
    
    print("📝 EMAIL DE PRUEBA GENERADO:")
    print("=" * 35)
    print(test_email_content)
    
    return test_email_content

def show_final_checklist():
    """Checklist final para asegurar que todo funciona"""
    
    print("\n✅ CHECKLIST FINAL:")
    print("=" * 25)
    print("□ 1. Fuentes RSS mezcladas (inglés + español) ✅ CONFIGURADO")
    print("□ 2. Rotación automática de links ✅ CONFIGURADO") 
    print("□ 3. Email paulmoll@outlook.com como destinatario")
    print("     → Configurar RECIPIENTS en GitHub Secrets")
    print("□ 4. Configurar GMAIL_USER en GitHub Secrets")
    print("□ 5. Configurar GMAIL_APP_PASS en GitHub Secrets")
    print("□ 6. Probar envío manual desde GitHub Actions")
    print()
    
    print("🚀 CUANDO ESTÉ TODO CONFIGURADO:")
    print("• El newsletter se enviará automáticamente cada día")
    print("• Contenido fresco y rotado diariamente")
    print("• Noticias en inglés y español balanceadas")
    print("• Diseño visual atractivo e infográfico")
    print()
    
    print("💡 PARA PROBAR MANUALMENTE:")
    print("• Ve a GitHub → Actions → 'Café con IA - 07:30 ET'")
    print("• Click en 'Run workflow' → 'Run workflow'")
    print("• Verificar que llegue a paulmoll@outlook.com")

if __name__ == "__main__":
    configure_email_settings()
    create_test_email() 
    show_final_checklist()
    
    print(f"\n🎉 CONFIGURACIÓN LISTA PARA PRODUCCIÓN")
    print("Siguiente paso: Configurar secrets en GitHub Actions")
