"""Seed production database (idempotent - skips if data exists)."""
import os
import runpy
import sys

from django.core.management.base import BaseCommand
from courses.models import Trilha, LicaoBiblica, Exercicio
from gamification.models import Recompensa, DesafioDiario, SerieOuroDesafio


class Command(BaseCommand):
    help = 'Seed production DB with trilhas, lições, exercícios, etc. Skips if data exists.'

    def handle(self, *args, **options):
        count = Trilha.objects.count()
        if count > 0:
            self.stdout.write(self.style.SUCCESS(f'Database already seeded ({count} trilhas). Skipping.'))
            return

        self.stdout.write('Database is empty. Running seed_v2.py in-process...')

        project_root = os.path.normpath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'
        ))
        seed_path = os.path.normpath(os.path.join(project_root, 'seed_v2.py'))

        if not os.path.exists(seed_path):
            self.stderr.write(self.style.ERROR(f'seed_v2.py not found at {seed_path}'))
            sys.exit(1)

        try:
            runpy.run_path(seed_path, run_name='__main__')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'seed_v2.py FAILED: {e}'))
            sys.exit(1)

        final_count = Trilha.objects.count()
        if final_count == 0:
            self.stderr.write(self.style.ERROR(
                'seed_v2.py ran but created 0 trilhas! '
                'Check Render build logs for errors.'
            ))
            sys.exit(1)

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete! {final_count} trilhas, '
            f'{LicaoBiblica.objects.count()} lições, '
            f'{Exercicio.objects.count()} exercícios, '
            f'{SerieOuroDesafio.objects.count()} séries ouro, '
            f'{Recompensa.objects.count()} recompensas.'
        ))
