#!/bin/bash
# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

sleep 2

echo "========== DJANGO MIGRATIONS =========="
python manage.py migrate

echo "========== DJANGO SUPERUSER =========="
admin_exists() {
    python <<END
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
if User.objects.filter(is_superuser=True).exists():
    print("True")
else:
    print("False")
END
}

if [[ $(admin_exists) == "False" ]]; then
    echo "Admin user does not exist. Creating..."
    export DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME}"
    export DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL}"
    export DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD}"
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL"
else
    echo "Admin user exists. No action required."
fi

echo "Continuing with the execution."

echo "========== DJANGO RUNSERVER =========="
python manage.py runserver_plus 0.0.0.0:8000

exec "$@"
