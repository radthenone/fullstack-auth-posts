import smtplib
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from apps.users.models import EmailSend, RegisterToken, User


@shared_task
def send_confirmation_email(
    sender_email: str,
    receiver_email: str,
    add_subject: str,
    message: str,
) -> None:
    subject = add_subject

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp:
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print("An error occurred while sending the email:", str(e))


@shared_task
def check_expired_register_tokens():
    expired_tokens = RegisterToken.objects.filter(
        created_at__lte=timezone.now() - timedelta(minutes=30)
    )
    for token in expired_tokens:
        email = token.user.email
        user = User.objects.filter(email=email)
        email_send = EmailSend.objects.filter(
            recipient_list__contains=[email],
            from_email=settings.DEFAULT_EMAIL,
        )
        user.delete()
        email_send.delete()
    expired_tokens.delete()
