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
    print("DEBUG: Script started (test)", flush=True)
    raise Exception("DEBUG: Forzando excepción para probar logs")
    # El resto del código original va aquí...