import os, json, smtplib, ssl, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from src.feeds import top10  # nuestro módulo

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_APP_PASS")
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
    try:
        import yaml
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

        prompts = [
            "Prompt 1: ¿Cómo automatizar tus tareas repetitivas hoy con IA?",
            "Prompt 2: Crea un mini-curso de 30 min con ChatGPT y Notion."
        ]
        date = datetime.date.today().strftime("%d/%m/%Y")
        html = Template(open("src/template.html").read()).render(stories=stories, prompts=prompts, date=date)
        text = f"Café con IA – {date}\n" + \
               "\n".join(f"- {s['title']}: {s['link']}" for s in stories) + \
               "\n\nPrompts:\n" + "\n".join(prompts)
        send(html, text)
    except Exception as e:
        import traceback
        print("ERROR:", e, flush=True)
        traceback.print_exc()