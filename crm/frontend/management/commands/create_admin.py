from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates admin user'

    def handle(self, *args, **options):
        email = 'icu0755@gmail.com'
        password = 'qwe123qwe'
        user = User.objects.create_superuser(email, email, password)
        self.stdout.write('Successfully created user "%s"' % user.id)