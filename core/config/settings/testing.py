from config.settings.base import *  # noqa
import environ  # noqa

environ.Env.read_env(str(BASE_DIR / ".envs" / "testing.env"))
env = environ.Env()

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "SECRET_KEY",
    default="!!!SET DJANGO_SECRET_KEY!!!",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# DEBUGING FOR TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore # noqa F405

# LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            + "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

REST_FRAMEWORK.update({"TEST_REQUEST_DEFAULT_FORMAT": "json"})

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

BROKER_BACKEND = "memory"
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_BROKER_URL = "memory://"
CELERY_RESULT_BACKEND = "cache+memory://"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.get_value(var="POSTGRES_HOST", default="localhost"),
        "PORT": env.get_value(var="POSTGRES_PORT", default="5433"),
        "NAME": env.get_value(var="POSTGRES_DB", default="test"),
        "USER": env.get_value(var="POSTGRES_USER", default="test"),
        "PASSWORD": env.get_value(var="POSTGRES_PASSWORD", default="test"),
        "ATOMIC_REQUESTS": True,
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
