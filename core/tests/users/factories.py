import json
from enum import Enum
from typing import Optional
from uuid import uuid4
from apps.users.models import ProfileMixin
import factory
from factory import fuzzy
from apps.users.models import User

from faker import Faker
from faker.providers import internet, misc
from django.db.models.signals import post_save
from apps.api.tokens import encode_token
from apps.users.types import UserModelType
import logging

faker = Faker()
faker.add_provider(internet)
faker.add_provider(misc)


def get_email_attribute():
    email = str(faker.unique.email().split(".")[0]) + ".com"
    if User.objects.filter(email=email).exists():
        return get_email_attribute()
    return email


class RolesNames(Enum):
    PREMIUM = "PREMIUM"
    BASIC = "BASIC"

    @classmethod
    def choices(cls):
        return [key.value for key in cls]


class RolesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.Roles"
        django_get_or_create = ("name", "description")

    description = factory.Faker("sentence")

    @factory.lazy_attribute
    def name(self):
        return fuzzy.FuzzyChoice(choices=RolesNames.choices()).fuzz()


class FriendshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.Friendship"
        django_get_or_create = ("from_user", "to_user")

    from_user = factory.SubFactory(
        "tests.users.factories.UserFactory",
    )
    to_user = factory.SubFactory(
        "tests.users.factories.UserFactory",
    )
    is_accepted = factory.Faker("boolean")
    is_blocked = factory.Faker("boolean")

    @factory.post_generation
    def ensure_different_users(self, create, extracted, **kwargs):  # noqa
        while self.to_user == self.from_user:
            self.to_user = factory.SubFactory(UserFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        logging.info("creating friendship")
        from_user: Optional["UserModelType"] = kwargs.pop("from_user", None)
        to_user: Optional["UserModelType"] = kwargs.pop("to_user", None)
        if from_user and to_user:
            from_user.friends.add(to_user)  # noqa
            to_user.friends.add(from_user)  # noqa
            kwargs["from_user"] = from_user
            kwargs["to_user"] = to_user

        return super()._create(model_class, *args, **kwargs)


class JSONFactory(factory.DictFactory):
    @classmethod
    def _generate(cls, create, attrs):
        obj = super()._generate(create, attrs)
        return json.dumps(obj)


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.User"
        django_get_or_create = ("email",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda _: get_email_attribute())
    password = factory.django.Password(faker.password())
    username = factory.LazyAttribute(
        lambda obj: f"{obj.email.split('@')[0]}_{str(uuid4().hex)}"
    )
    friend_requests = factory.Dict(params={}, dict_factory=JSONFactory)

    @factory.post_generation
    def friend_requests(self, create, extracted, **kwargs):
        if not create or extracted is None:
            return

        else:
            if not isinstance(extracted, int):
                raise factory.FactoryError("Friend requests should be an integer")
            users = UserFactory.build_batch(size=extracted)

            params = {}
            for user in users:
                params[user.email] = f"{encode_token()}"
                user.save()
            self.friend_requests.update(params)
            logging.info(f"Friend requests: {self.friend_requests}")

    @factory.post_generation
    def roles(self, create, extracted):
        roles = getattr(extracted, "roles", "BASIC")
        if roles not in RolesNames.choices() and not isinstance(roles, str):
            raise factory.FactoryError("Roles should be one of: BASIC, PREMIUM")
        if not create:
            RolesFactory.build(name=roles)
            UserBasicFactory.build(user=self)

        else:
            if roles == "BASIC":
                role = RolesFactory.create(name="BASIC", description="Basic role")
                UserBasicFactory.create(user=self)
            else:
                role = RolesFactory.create(name="PREMIUM", description="Premium role")
                UserPremiumFactory.create(user=self)
            self.roles.set([role])
            log_value = list(self.roles.all().values_list("name", flat=True))
            logging.info(f"{self.email} -> roles: {log_value}")

    @factory.post_generation
    def friends(self, create, extracted):
        if not create or extracted is None:
            return

        else:
            if not isinstance(extracted, int):
                raise factory.FactoryError("Friends should be an integer")

            users = UserFactory.create_batch(size=extracted)
            for user in users:
                FriendshipFactory.create(from_user=self, to_user=user, is_accepted=True)
            log_value = list(self.friends.all().values_list("email", flat=True))
            logging.info(f"User {self.email} friends: {log_value}")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProfileMixin
        abstract = True

    user = factory.SubFactory("tests.users.factories.UserFactory")
    avatar = factory.django.ImageField()
    is_premium = False
    is_basic = False


class UserPremiumFactory(ProfileFactory):
    class Meta:
        model = "users.UserPremium"

    is_basic = False
    is_premium = True


class UserBasicFactory(ProfileFactory):
    class Meta:
        model = "users.UserBasic"

    is_basic = True
    is_premium = False
