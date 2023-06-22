from uuid import uuid4

from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def create_username(sender, instance, **kwargs):
    if instance.username == "":
        username = instance.email.split("@")[0]
        uuid_hash = str(uuid4().hex)
        instance.username = f"{username}_{uuid_hash}"
