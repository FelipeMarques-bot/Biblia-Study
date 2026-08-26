import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Cria superuser automaticamente se nao existir'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@admin.com')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" criado com sucesso!'))
        else:
            self.stdout.write(f'Superuser "{username}" ja existe.')
