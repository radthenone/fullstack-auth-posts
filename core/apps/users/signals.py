from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def create_username(sender, instance, **kwargs):
    from apps.users.utils import set_username
    if instance.username == "":
        instance.username = set_username(instance.email)
