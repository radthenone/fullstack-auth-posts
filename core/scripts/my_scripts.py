from django.contrib.auth import get_user_model
from pprint import pprint


def run():
    user = get_user_model()
    pprint(user.objects.all())
