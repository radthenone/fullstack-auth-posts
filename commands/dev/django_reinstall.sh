#!/bin/bash
# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

./commands/dev/django_reset_migrations.sh
./commands/dev/django_app_migration.sh users
docker-compose up --build -d
