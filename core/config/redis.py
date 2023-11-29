import redis as redis_lib
from django.conf import settings

cache = redis_lib.Redis(
    host=str(settings.REDIS_CACHES["REDIS_HOST"]),
    port=int(settings.REDIS_CACHES["REDIS_PORT"]),
    db=int(settings.REDIS_CACHES["REDIS_DB"]),
)
