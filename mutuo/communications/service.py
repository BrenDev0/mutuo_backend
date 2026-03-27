import smtplib
from email.message import EmailMessage

from mutuo.settings import settings


def send_email(
    email_message: EmailMessage
) -> None:
    with smtplib.SMTP(settings.MAILER_HOST, settings.MAILER_PORT) as server:
        server.starttls()
        server.login(settings.MAILER_USER, settings.MAILER_PASSWORD)
        server.send_message(email_message)

            
