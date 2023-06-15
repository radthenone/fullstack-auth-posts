from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import Profile, UserBasic, UserPremium


@receiver(post_save, sender=Profile)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.roles == UserPremium.user.PREMIUM:
            UserPremium.objects.create(user=instance.user, is_premium=True, is_basic=False)
        elif instance.roles == UserBasic.user.BASIC:
            UserBasic.objects.create(user=instance.user, is_premium=False, is_basic=True)
