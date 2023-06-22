from celery import shared_task
from django.contrib.postgres.fields import ArrayField
from django.core.mail import send_mail
from django.db import models


class EmailSend(models.Model):
    subject = models.CharField(max_length=50, blank=False)
    message = models.TextField(max_length=250, blank=False)
    from_email = models.EmailField(unique=True)
    recipient_list = ArrayField(models.EmailField())
    fail_silently = models.BooleanField(default=False)

    @staticmethod
    @shared_task
    def send_emails_async(email_send_id):
        try:
            email_send = EmailSend.objects.get(id=email_send_id)
            send_mail(
                email_send.subject,
                email_send.message,
                email_send.from_email,
                email_send.recipient_list,
                fail_silently=email_send.fail_silently,
            )
        except EmailSend.DoesNotExist:
            pass

    def send_emails(self):
        self.save()
        EmailSend.send_emails_async.delay(self.id)
