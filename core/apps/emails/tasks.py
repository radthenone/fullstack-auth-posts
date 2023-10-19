from celery import shared_task
import logging
from apps.emails.utils import send_mail
from django.conf import settings


@shared_task
def send_register_email(email: str, message: dict):
    logging.info("Sending register email")
    send_mail(
        subject=message.get("title"),
        message_data=message,
        from_email=settings.DEFAULT_EMAIL,
        to_email=email,
        template_name="emails/register/register",
    )
    logging.info("Register email sent")
