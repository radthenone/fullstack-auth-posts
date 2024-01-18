from django.db import models

from apps.users.managers import CustomRolesManager


class Roles(models.Model):
    name = models.CharField(max_length=20, default="BASIC")
    description = models.TextField(default="")
    objects = CustomRolesManager()

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "role"
        verbose_name_plural = "roles"
