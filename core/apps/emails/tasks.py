from celery import shared_task
import logging
from apps.emails.utils import send_mail
from django.conf import settings


@shared_task
def send_register_email(data: dict):
    logging.info("Sending register email")
    send_mail(
        subject=data.get("message").get("title"),
        message_data=data.get("message"),
        from_email=settings.DEFAULT_EMAIL,
        to_email=data.get("email"),
        template_name="emails/register.html",
    )
    logging.info("Register email sent")
