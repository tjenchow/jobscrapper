import smtplib
import traceback
from email.mime.text import MIMEText

def send_digest(jobs, config):
    body = "Your weekly job digest:\n\n"
    for j in jobs:
        body += f"[{j['score']}/10] {j['title']} — {j['company']}\n"
        body += f"  Reason: {j['reason']}\n"
        body += f"  Link: {j['url']}\n\n"

    msg = MIMEText(body)
    msg["Subject"] = "Job digest"
    msg["From"] = config["email_from"]
    msg["To"] = config["email_to"]

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(config["email_from"], config["email_pass"])
            server.send_message(msg)
    except Exception as e:
        print("ERROR:")
        traceback.print_exc()