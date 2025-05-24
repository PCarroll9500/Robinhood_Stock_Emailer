import os
import smtplib
from email.message import EmailMessage

EMAIL = os.environ["EMAIL_ADDRESS"]
PASSWORD = os.environ["EMAIL_PASSWORD"]
RECIPIENT = os.environ["RECIPIENT_EMAIL"]

msg = EmailMessage()
msg.set_content("✅ This is a test email from GitHub Actions using secrets.")
msg["Subject"] = "Test Email"
msg["From"] = EMAIL
msg["To"] = RECIPIENT

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL, PASSWORD)
    smtp.send_message(msg)