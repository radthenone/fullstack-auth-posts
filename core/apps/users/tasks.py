from celery import shared_task
import logging
from apps.emails.utils import send_mail


@shared_task
def send_friend_request(
    from_email: str,
    to_email: str,
):
    try:
        send_mail(
            subject=f"Friend request from {from_email}",
            message_data={
                "message": "I want to invite to be my friend",
                "email": from_email,
            },
            from_email=from_email,
            to_email=to_email,
            template_name="emails/",
        )
        logging.info("Friend request send")
    except ValueError as error:
        logging.error(error)
