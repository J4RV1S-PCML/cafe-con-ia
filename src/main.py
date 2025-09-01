import os, json, smtplib, ssl, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from src.feeds_simple import top10  # nuestro módulo simplificado
from src.content_rotator import ContentRotator  # Sistema de rotación automática
from src.simple_security import validate_environment, secure_content  # Seguridad básica

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
RECIPIENTS = json.loads(os.getenv("RECIPIENTS"))

def send(html, text):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Café con IA – Top 10 del {datetime.date.today():%d/%m/%Y}"
    msg["From"] = GMAIL_USER
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        for r in RECIPIENTS:
            server.sendmail(GMAIL_USER, r, msg.as_string())

if __name__ == "__main__":
    print("DEBUG: Script started", flush=True)
    
    # ✅ VALIDACIÓN DE SEGURIDAD BÁSICA
    try:
        validate_environment()
        print("🔒 Seguridad básica aplicada")
    except ValueError as e:
        print(f"❌ Error de seguridad: {e}")
        exit(1)
    
    try:
        import yaml
        print("DEBUG: GMAIL_USER =", repr(GMAIL_USER), flush=True)
        print(f"DEBUG: GMAIL_PASS raw repr: {repr(GMAIL_PASS)}", flush=True)
        if GMAIL_PASS:
            print(f"DEBUG: GMAIL_PASS length = {len(GMAIL_PASS)}", flush=True)
            print(f"DEBUG: GMAIL_PASS bytes = {list(GMAIL_PASS.encode())}", flush=True)
            GMAIL_PASS = GMAIL_PASS.strip()
            print(f"DEBUG: GMAIL_PASS after strip: {repr(GMAIL_PASS)} length = {len(GMAIL_PASS)}", flush=True)
            print(f"DEBUG: GMAIL_PASS is set: {bool(GMAIL_PASS)}", flush=True)
        else:
            print("DEBUG: GMAIL_PASS is set: False", flush=True)
        print("DEBUG: RECIPIENTS =", repr(RECIPIENTS), flush=True)
        # Mostrar feeds cargados
        with open("rss_sources.yml", "r", encoding="utf-8") as f:
            feeds = yaml.safe_load(f)
        print(f"DEBUG feeds loaded ({len(feeds)}):", feeds, flush=True)

        stories = top10()
        print(f"DEBUG stories count: {len(stories) if stories else 0}", flush=True)
        if stories:
            for idx, s in enumerate(stories):
                print(f"Story {idx+1}: {json.dumps(s, ensure_ascii=False, indent=2)}", flush=True)
        else:
            print("DEBUG stories: No stories found.", flush=True)

        # 🔄 SISTEMA DE ROTACIÓN AUTOMÁTICA DE CONTENIDO IA
        print("🔄 Iniciando rotación automática de contenido...", flush=True)
        rotator = ContentRotator()
        
        # Obtener contenido rotado automáticamente
        fresh_content = rotator.get_fresh_newsletter_content()
        
        # Logging de contenido seleccionado
        print("📋 Contenido seleccionado para esta edición:", flush=True)
        for content_type, items in fresh_content.items():
            print(f"  {content_type}: {len(items)} items", flush=True)
            for idx, item in enumerate(items):
                category = item.get('category', 'general')
                title = item.get('title', 'Sin título')
                print(f"    {idx+1}. [{category}] {title}", flush=True)
        
        # Usar contenido rotado en lugar de cargar archivos YAML estáticos
        # ✅ Aplicar seguridad básica al contenido
        tips = secure_content(fresh_content['tips'])
        trends = secure_content(fresh_content['trends'])
        automations = secure_content(fresh_content['automations'])
        videos = secure_content(fresh_content['videos'])
        date = datetime.date.today().strftime("%d/%m/%Y")
        html = Template(open("src/template.html").read()).render(
            stories=stories[:10],
            tips=tips,
            trends=trends,
            automations=automations,
            videos=videos,
            date=date
        )
        text = f"Café con IA – {date}\n" + \
               "\n".join(f"- {s['title']}: {s['link']}" for s in stories) + \
               "\n\nTips:\n" + "\n".join(f"- {tip['title']}: {tip['link']}" for tip in tips) + \
               "\n\nTendencias:\n" + "\n".join(f"- {trend['title']}: {trend['link']}" for trend in trends) + \
               "\n\nAutomatización:\n" + "\n".join(f"- {auto['title']}: {auto['link']}" for auto in automations) + \
               "\n\nVideos recomendados:\n" + "\n".join(f"{v['title']}: {v['link']}" for v in videos)
        print("DEBUG: About to login to SMTP", flush=True)
        print("DEBUG: GMAIL_USER =", GMAIL_USER, flush=True)
        print("DEBUG: GMAIL_PASS length =", len(GMAIL_PASS) if GMAIL_PASS else 0, flush=True)
        send(html, text)
    except Exception as e:
        import traceback
        print("ERROR:", e, flush=True)
        traceback.print_exc()