from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask


@receiver(post_migrate, sender=AppConfig)
def create_register_interval_30_minutes_task(sender, **kwargs):
    interval, _ = IntervalSchedule.objects.get_or_create(
        every=30, period=IntervalSchedule.MINUTES
    )
    task, _ = PeriodicTask.objects.get_or_create(
        name="Check register tokens expired",
        task="apps.users.tasks.check_expired_register_tokens",
        interval=interval,
        start_time=str(timezone.now()),
    )
