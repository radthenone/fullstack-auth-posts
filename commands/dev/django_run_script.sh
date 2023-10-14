#!/bin/bash
# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

if [ -z "${1:-}" ]; then
    echo "Add filename from 'core\scripts' directory name"
else
    filename="$1"
    docker-compose exec -it django \
    sh -c "python manage.py runscript $filename"

fi