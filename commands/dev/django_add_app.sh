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
    echo "./commands/dev/django_add_app.sh <APP_NAME>"
else
    app_name="$1"
    echo "Start process $app_name"
    docker-compose exec -it django sh -c "python manage.py startapp $app_name;
    mv $app_name apps;
    rm -f $app_name
    "
    echo "1. change apps.py in your app folder"
    echo "in apps/<app-name>/apps.py change name to: apps.<app-name>"
    echo "2. add your app to project LOCAL_APPS"
    echo "in config/settings.base LOCAL_APPS add apps.<app-name>"
    echo "3. in config urls add paths to your app"
    echo "in config/urls.py add path('api/<app-name>/', include('apps.<app-name>.urls')),"

file_name="urls.py"
content=$(cat <<EOF
from django.urls import include, path
from typing import Any, Callable, List, Optional, Union

urlpatterns: List[Union[str, Callable[..., Any], Optional[str]]] = [
    # list of URL patterns here
]
EOF
)

    echo "$content" > "./apps/$app_name/$file_name"

    echo "Python file '$file_name' created with content:"
fi
