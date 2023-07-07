from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_migrate, sender=AppConfig)
def create_register_interval_30_minutes_task(sender, **kwargs):
    try:
        interval, created = IntervalSchedule.objects.get_or_create(
            every=30, period=IntervalSchedule.MINUTES
        )
        task, created = PeriodicTask.objects.update_or_create(
            name="Check register tokens expired",
            defaults={
                "task": "apps.users.tasks.check_expired_register_tokens",
                "interval": interval,
                "start_time": str(timezone.now()),
            },
        )
    except ObjectDoesNotExist:
        pass
