#!/bin/bash

set -o errexit
set -o nounset

worker_ready() {
    celery -A config.celery inspect ping
}

until worker_ready; do
    >&2 echo 'Celery workers not available'
    sleep 1
done
>&2 echo 'Celery workers is available'

echo "========== CELERY FLOWER ON =========="
# Flowers
# graphical interface for celery workers
sleep 5
celery \
    -A config.celery \
    -b "${CELERY_BROKER_URL}" \
    flower \
    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"

exec "$@"
