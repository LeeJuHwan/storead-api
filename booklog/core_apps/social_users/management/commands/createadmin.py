from django.core.management.base import BaseCommand
from core_apps.social_users.models import Admin
import getpass


class Command(BaseCommand):
    help = 'Creates a new admin superuser'

    def handle(self, *args, **kwargs):
        # 슈퍼유저 생성 로직
        username = input("Username: ")
        email = input("Email: ")
        password = getpass.getpass()
        Admin.objects.create_superuser(username=username, email=email, password=password)

        self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
