"""Seed production database (idempotent - skips if data exists)."""
import os
import importlib.util

from django.core.management.base import BaseCommand
from courses.models import Trilha, LicaoBiblica, Exercicio


class Command(BaseCommand):
    help = 'Seed production DB with trilhas, lições, exercícios, etc. Skips if data exists.'

    def handle(self, *args, **options):
        count = Trilha.objects.count()
        if count > 0:
            self.stdout.write(self.style.SUCCESS(f'Database already seeded ({count} trilhas). Skipping.'))
            return

        self.stdout.write('Database is empty. Running seed_v2.py in-process...')

        project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
        project_root = os.path.normpath(project_root)
        seed_path = os.path.normpath(os.path.join(project_root, 'seed_v2.py'))

        if not os.path.exists(seed_path):
            self.stdout.write(self.style.ERROR(f'seed_v2.py not found at {seed_path}'))
            return

        with open(seed_path, 'r', encoding='utf-8') as f:
            source = f.read()

        # Remove the Django setup block at the top (we're already in Django)
        lines = source.split('\n')
        clean_lines = []
        skip = False
        for line in lines:
            if 'django.setup()' in line:
                skip = False
                continue
            if line.startswith('import os, django, sys'):
                skip = True
                continue
            if skip and (line.startswith('sys.path') or line.startswith("os.environ['DJANGO")):
                continue
            if skip and line.strip() == '':
                skip = False
                continue
            skip = False
            clean_lines.append(line)

        clean_source = '\n'.join(clean_lines)

        # Execute seed in current process
        exec(compile(clean_source, seed_path, 'exec'), {'__name__': '__exec__', '__file__': seed_path})

        final_count = Trilha.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'Seed complete! {final_count} trilhas, '
            f'{LicaoBiblica.objects.count()} lições, '
            f'{Exercicio.objects.count()} exercícios.'
        ))
