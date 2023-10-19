from django.contrib.auth import get_user_model
from pprint import pprint
from django.db import connection


def run():
    user = get_user_model()

    # print all user models
    pprint(user.objects.all())

    # show sql queries
    pprint(connection.queries)
