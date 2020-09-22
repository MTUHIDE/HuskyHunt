from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Makes existing user a superuser'

    def handle(self, *args, **options):
        email = input("Please enter an existing email: ")

        users = User.objects.filter(email=email)

        if len(users) == 0:
            self.stderr.write(self.style.ERROR("User couldn't be found."))
            return
        elif len(users) > 1:
            self.stderr.write(self.style.ERROR("There are more than one users with that email."))
            return

        user = users[0]

        user.is_superuser = True
        user.is_staff = True

        user.save()

        self.stdout.write(self.style.SUCCESS('✓ user was updated.'))
