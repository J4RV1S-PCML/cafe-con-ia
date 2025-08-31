import os, json, smtplib, ssl, datetime, feedparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
RECIPIENTS = json.loads(os.getenv("RECIPIENTS"))

def top10():
    urls = [
    "https://venturebeat.com/ai/feed",  # sin espacio
    "https://www.deeplearning.ai/thebatch/feed"
    ]
    items = []
    for u in urls:
        items += feedparser.parse(u).entries
    items = sorted(items, key=lambda e: e.published_parsed, reverse=True)[:10]
    return [{"title": i.title, "link": i.link,
             "summary": i.summary[:180]+"…"} for i in items]

if __name__ == "__main__":
    stories = top10()
    prompts = [
        "Prompt 1: ¿Cómo automatizar tus tareas repetitivas hoy con IA?",
        "Prompt 2: Crea un mini-curso de 30 min con ChatGPT y Notion."
    ]
    date = datetime.date.today().strftime("%d/%m/%Y")
    html = Template(open("src/template.html").read()).render(stories=stories,
                                                             prompts=prompts,
                                                             date=date)
    text = f"Café con IA – {date}\n" + \
           "\n".join(f"- {s['title']}: {s['link']}" for s in stories) + \
           "\n\nPrompts:\n" + "\n".join(prompts)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Café con IA – Top 10 del {date}"
    msg["From"] = GMAIL_USER
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        for r in RECIPIENTS:
            server.sendmail(GMAIL_USER, r, msg.as_string())