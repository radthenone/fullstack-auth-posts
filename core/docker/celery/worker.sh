#!/bin/bash

set -o errexit
set -o nounset

# celery worker
# perform tasks from the queue in reality
sleep 2
watchfiles \
    --filter python \
    'celery -A config.celery worker -l INFO --logfile=logs/celery.log'

exec "$@"
