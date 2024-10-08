# Generated by Django 4.2.8 on 2023-12-06 10:53

import apps.users.models.abstract_models
import apps.users.utils
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("username", models.CharField(blank=True, max_length=150)),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_email",
                                message="Enter a valid email address with either .com or .pl domain.",
                                regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.(com|pl)$",
                            )
                        ],
                        verbose_name="Email",
                    ),
                ),
                ("friend_requests", models.JSONField(blank=True, default=dict)),
                ("failed_login_attempts", models.IntegerField(default=0)),
                ("is_locked", models.BooleanField(default=False)),
                ("verified", models.BooleanField(default=False)),
                ("change_password", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "ordering": ["-date_joined"],
            },
        ),
        migrations.CreateModel(
            name="Roles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="BASIC", max_length=20)),
                ("description", models.TextField(default="")),
            ],
            options={
                "verbose_name": "role",
                "verbose_name_plural": "roles",
            },
        ),
        migrations.CreateModel(
            name="UserBasic",
            fields=[
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=apps.users.utils.avatar_upload_path,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "birth_date",
                    models.DateField(
                        blank=True,
                        null=True,
                        validators=[
                            apps.users.models.abstract_models.Validators.validate_birth_date
                        ],
                        verbose_name="Birth Date",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="basic_profile",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("is_basic", models.BooleanField(default=True, editable=False)),
                ("is_premium", models.BooleanField(default=False, editable=False)),
            ],
            options={
                "verbose_name": "basic user",
                "verbose_name_plural": "basic users",
            },
        ),
        migrations.CreateModel(
            name="UserPremium",
            fields=[
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=apps.users.utils.avatar_upload_path,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "birth_date",
                    models.DateField(
                        blank=True,
                        null=True,
                        validators=[
                            apps.users.models.abstract_models.Validators.validate_birth_date
                        ],
                        verbose_name="Birth Date",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="premium_profile",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("is_basic", models.BooleanField(default=False, editable=False)),
                ("is_premium", models.BooleanField(default=True, editable=False)),
            ],
            options={
                "verbose_name": "premium user",
                "verbose_name_plural": "premium users",
            },
        ),
        migrations.CreateModel(
            name="Friendship",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_accepted", models.BooleanField(default=False)),
                ("is_blocked", models.BooleanField(default=False)),
                (
                    "from_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="from_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "to_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="to_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="user",
            name="friends",
            field=models.ManyToManyField(
                blank=True, through="users.Friendship", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="roles",
            field=models.ManyToManyField(related_name="roles", to="users.roles"),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(
                fields=["-date_joined"], name="users_user_date_jo_5abcb7_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(
                fields=("email", "username"), name="unique_user"
            ),
        ),
    ]
