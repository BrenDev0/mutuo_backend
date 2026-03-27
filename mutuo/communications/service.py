import smtplib
from pathlib import Path
from email.message import EmailMessage

from mutuo.settings import settings


def create_verification_email(
    code: int,
    recipient_email: str
):
    template_path = Path(__file__).parent/"templates"/"verify_email.html"

    with open(template_path, 'r', encoding="utf-8") as f:
        template = f.read()

    email_body = template.replace('{{verification_code}}', str(code))
    
    email_message = EmailMessage()
    email_message["From"] = settings.MAILER_USER
    email_message["To"] = recipient_email
    email_message["Subject"] = "Verificar Correo Electrónico"
    email_message.set_content(email_body, subtype="html")

    return email_message


def send_email(
    email_message: EmailMessage
) -> None:
    with smtplib.SMTP(settings.MAILER_HOST, settings.MAILER_PORT) as server:
        server.starttls()
        server.login(settings.MAILER_USER, settings.MAILER_PASSWORD)
        server.send_message(email_message)

            
