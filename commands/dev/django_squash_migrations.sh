#!/bin/bash
# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

if [ -z "${1:-}" ] || [ -z "${2:-}" ]; then
    echo "Give app name and number like 'app_name 0001' to squash migrations"
else
    app_name="$1"
    number_squash="$2"
    docker-compose exec -it django \
    sh -c "echo 'yes' | python manage.py squashmigrations $app_name $number_squash"
fi
