from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.users.models import Profile, UserBasic, UserPremium, User
from uuid import uuid4


@receiver(post_save, sender=Profile)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.roles == UserPremium.user.PREMIUM:
            UserPremium.objects.create(user=instance.user, is_premium=True, is_basic=False)
        elif instance.roles == UserBasic.user.BASIC:
            UserBasic.objects.create(user=instance.user, is_premium=False, is_basic=True)


@receiver(pre_save, sender=User)
def create_username(sender, instance, **kwargs):
    if instance.username == "":
        instance.username = instance.email.split('@')[0] + str(uuid4().hex)
