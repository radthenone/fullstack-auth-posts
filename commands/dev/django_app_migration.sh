#!/bin/bash
# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset


if [ -z "${1:-}" ]; then
    echo "Give app name in django directory"
    echo "You can add app like:"
    echo "./commands/dev/django_app_migration.sh <APP_NAME>"
else
    app_name="$1"
    echo "Start process $app_name"
    docker-compose run --rm django sh -c "python manage.py makemigrations $app_name"
    docker-compose run --rm django sh -c "python manage.py migrate $app_name"
fi
