from email.message import EmailMessage
import ssl
import smtplib

from settings.settings import EMAIL_HOST, EMAIL_SENDER, EMAIL_PASSWORD


def send_email(receiver, subject, body):
    try:
        em = EmailMessage()
        em["From"] = EMAIL_SENDER
        em["To"] = receiver
        em["Subject"] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(EMAIL_HOST, port=465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, receiver, em.as_string())
    except Exception:
        # TODO: Log
        pass
