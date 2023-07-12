from uuid import uuid4

import factory
from apps.users.models import Profile, UserBasic, UserPremium
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from factory import fuzzy
from faker import Faker
from faker.providers import internet, misc

faker = Faker()
faker.add_provider(internet)
faker.add_provider(misc)
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    roles = fuzzy.FuzzyChoice(choices=["BA", "PM"])
    password = factory.LazyFunction(lambda: make_password(faker.password()))
    username = factory.LazyAttribute(
        lambda obj: f"{obj.email.split('@')[0]}_{str(uuid4().hex)}"
    )

    @classmethod
    def create(cls, **kwargs):
        kwargs["roles"] = "BA"
        return super().create(**kwargs)


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        abstract = True

    user = factory.SubFactory("tests.users.factories.UserFactory")
    avatar = factory.django.ImageField()
    is_premium = False
    is_basic = False


class UserPremiumFactory(ProfileFactory):
    class Meta:
        model = UserPremium

    is_basic = False
    is_premium = True


class UserBasicFactory(ProfileFactory):
    class Meta:
        model = UserBasic

    is_basic = True
    is_premium = False
