"""Seed production database (idempotent - skips if data exists)."""
import os
import subprocess
import sys

from django.core.management.base import BaseCommand
from courses.models import Trilha


class Command(BaseCommand):
    help = 'Seed production DB with trilhas, lições, exercícios, etc. Skips if data exists.'

    def handle(self, *args, **options):
        count = Trilha.objects.count()
        if count > 0:
            self.stdout.write(self.style.SUCCESS(f'Database already seeded ({count} trilhas). Skipping.'))
            return

        self.stdout.write('Database is empty. Running seed_v2.py...')

        project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
        project_root = os.path.normpath(project_root)
        seed_path = os.path.join(project_root, 'seed_v2.py')

        if not os.path.exists(seed_path):
            self.stdout.write(self.style.ERROR(f'seed_v2.py not found at {seed_path}'))
            return

        result = subprocess.run(
            [sys.executable, seed_path],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=300,
        )

        self.stdout.write(result.stdout)
        if result.returncode != 0:
            self.stdout.write(self.style.ERROR(f'Seed failed:\n{result.stderr}'))
            return

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete! {Trilha.objects.count()} trilhas loaded.'
        ))
