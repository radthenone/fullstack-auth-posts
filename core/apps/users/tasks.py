from celery import shared_task
from celery.utils.log import get_task_logger
from config.celery import app

from apps.api.tokens import decode_token
from apps.emails.utils import send_mail
from apps.users.models import User

logger = get_task_logger(__name__)


@app.task
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
        logger.info("Friend request send")
    except ValueError as error:
        logger.error(error)


@shared_task
def remove_user_expired_tokens():
    logger.info("Removing expired tokens")
    for user in User.objects.all():
        for email, token in user.friend_requests.items():
            data = decode_token(token)
            if "errors" in data:
                user.friend_requests.pop(email)
                user.save()
    logger.info("Expired tokens removed")
