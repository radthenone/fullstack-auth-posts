#!/bin/bash
# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

echo "Give app name if want delete app migrations or delete all"
if [ -z "${1:-}" ]; then
    find . -path "*/migrations/*" -name "*.py" -not -path "*__init__*" -delete
    find . -path "*/migrations/*.pyc" -delete
    echo "All Migrations deleted"

    docker-compose stop
    docker rm fullstack_auth_postgres
    docker volume rm -f fullstack-auth-posts_postgres_data
    echo "Database deleted"
    docker volume create fullstack-auth-posts_postgres_data
    docker-compose up postgres --build -d
    docker-compose up django --build -d
    echo "end process"
else
    app_name="$1"
    echo "Start process $app_name"

    find . -path "*/migrations/$app_name/*" -name "*.py" -not -path "*__init__*" -delete
    find . -path "*/migrations/$app_name/*.pyc" -delete
    echo "App $app_name migrations deleted"

    docker-compose stop
    docker rm fullstack_auth_postgres
    docker volume rm -f fullstack-auth-posts_postgres_data
    echo "Database deleted"
    docker volume create fullstack-auth-posts_postgres_data
    docker-compose up postgres --build -d
    docker-compose up django --build -d
    echo "end process"

fi
