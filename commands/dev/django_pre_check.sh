#!/bin/bash
echo "Start tests and linter configuration"

docker-compose exec -it django bash -c "docker/debug/pre_django.sh"

echo "End of tests and linter configuration"
