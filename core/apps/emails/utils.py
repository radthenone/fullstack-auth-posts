import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.template.loader import get_template


def send_mail(
    subject: str,
    message_data: dict | str,
    from_email: str,
    to_email: str,
    template_name: str = None,
):
    """
    Sends an email with the specified subject, message data, sender email, and recipient email.

    Parameters:
        - subject (str): The subject of the email.
        - message_data (dict | str): The data to be included in the email message. Can be either a dictionary or a string.
        - from_email (str): The email address of the sender.
        - to_email (str): The email address of the recipient.
        - template_name (str, optional): The name of the template to be used for the email content. Defaults to None.

    Raises:
        - ValueError: If none of the function parameters are specified.

    Returns:
        None
    """
    if not any(
        [
            subject,
            message_data,
            from_email,
            to_email,
            template_name,
        ]
    ):
        raise ValueError("Data are not specified")

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    if template_name and isinstance(message_data, dict):
        message_type = "html"
        template_name = f"{template_name}.html"
        html_template = get_template(template_name)
        html_content = html_template.render(message_data)
        msg.attach(MIMEText(html_content, _subtype=message_type))
    else:
        message_type = "plain"
        text_content = message_data
        msg.attach(MIMEText(text_content, _subtype=message_type))

    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp:
            smtp.send_message(msg)
        logging.info("Email sent successfully!")
    except Exception as error:
        logging.error(error)


class CreateMail(dict):
    def __init__(
        self,
        send_email: str,
        title: str,
        info: str,
        extra_message: dict | None = None,
        **kwargs,
    ):
        if extra_message is None:
            extra_message = {}
        super().__init__(**kwargs)
        self["email"] = send_email
        self["message"] = {
            "title": title,
            "email": send_email,
            "info": info,
            **extra_message,
        }
