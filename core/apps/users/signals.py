from uuid import uuid4

from apps.users.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def create_username(sender, instance, **kwargs):
    if instance.username == "":
        instance.username = instance.email.split("@")[0] + str(uuid4().hex)
