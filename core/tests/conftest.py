import pytest
from apps.api.tokens import encode_token
from django.db import connections
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config.settings.testing import env
from django.core.management import call_command
from config.env import BASE_DIR
from pathlib import Path
from django.conf import settings


def run_sql(sql):
    conn = psycopg2.connect(
        dbname=env("POSTGRES_DB"),
        password=env("POSTGRES_PASSWORD"),
        user=env("POSTGRES_USER"),
        host=env("POSTGRES_HOST"),
        port=env("POSTGRES_PORT"),
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.fixture(scope="session")
def loaddata_fixtures():
    def _load():
        call_command(
            "loaddata",
            f"{Path(BASE_DIR / 'fixtures' / 'roles.json').as_posix()}",
        )

    return _load


@pytest.fixture(scope="session")
def django_db_setup(
    django_db_blocker,
    loaddata_fixtures,
):
    test_db = "test_db"
    settings.DATABASES["default"]["NAME"] = test_db

    run_sql(f"DROP DATABASE IF EXISTS {test_db}")
    run_sql(f"CREATE DATABASE {test_db}")
    with django_db_blocker.unblock():
        call_command("migrate", "--noinput")  # noqa
        loaddata_fixtures()
    yield

    for connection in connections.all():
        connection.close()

    run_sql(f"DROP DATABASE {test_db}")


class RedisMock:
    def __init__(self):
        self.redis = {}

    def set(self, key, value):
        self.redis[key] = value

    def get(self, key):
        return self.redis.get(key, None)


@pytest.fixture(scope="function")
def api_cache(mocker):
    cache_mock = mocker.Mock()
    redis_mock = RedisMock()
    cache_mock.get = redis_mock.get
    cache_mock.set = redis_mock.set
    return cache_mock


@pytest.fixture(scope="function")
def api_tokens(mocker, api_cache):
    api_cache.set(key="refresh", value="test-refresh-token")
    access_mock = mocker.patch(
        "apps.auth.utils.access_token", return_value="test-access-token"
    )
    values = {
        "access": access_mock.return_value,
        "refresh": api_cache.get(key="refresh"),
    }
    return values


@pytest.fixture(scope="function")
def api_auth(mocker, api_tokens):
    token_mock = mocker.patch("apps.auth.utils.auth_login", return_value=api_tokens)
    return token_mock.return_value


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def auth_client(api_client, api_auth):
    token = api_auth["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client
