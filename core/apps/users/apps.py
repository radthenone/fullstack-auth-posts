from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"

    def ready(self):
        try:
            from django.db.models.signals import post_migrate  # noqa F401

            import apps.users.signals  # noqa F401

            post_migrate.connect(
                apps.users.signals.create_register_interval_30_minutes_task,
                sender=self,
            )
        except ImportError:
            pass
