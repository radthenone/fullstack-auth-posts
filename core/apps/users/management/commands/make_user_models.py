from django.core.management.base import BaseCommand
import logging
from tests.users.factories import UserFactory

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    python manage.py make_user_models -> make 10 test users
    python manage.py make_user_models --amount 3 -> make 3 test users
    """

    help = "Create test users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--amount",
            type=int,
            default=10,
            help="Amount of test users to create",
            dest="amount",
        )

    @staticmethod
    def generate_users(amount: int):
        users = UserFactory.build_batch(size=amount)
        for user in users:
            print(user.objects.values())

    def handle(self, *args, **options):
        logger.info("Creating test users")
        amount = options["amount"] or 10
        self.generate_users(amount=amount)
