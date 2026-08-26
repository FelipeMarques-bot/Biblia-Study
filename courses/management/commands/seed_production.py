"""Seed production database (idempotent - skips if data exists)."""
import os
import sys
import importlib.util
import traceback

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

        self.stdout.write('Database is empty. Running seed_v2.py...')

        project_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
        seed_path = os.path.normpath(os.path.join(project_root, 'seed_v2.py'))

        if not os.path.exists(seed_path):
            self.stdout.write(self.style.ERROR(f'seed_v2.py not found at {seed_path}'))
            return

        spec = importlib.util.spec_from_file_location('seed_v2', seed_path)
        mod = importlib.util.module_from_spec(spec)
        mod.__name__ = 'seed_v2'

        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error running seed_v2: {e}'))
            traceback.print_exc()
            return

        final_count = Trilha.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'Seed complete! {final_count} trilhas, '
            f'{LicaoBiblica.objects.count()} lições, '
            f'{Exercicio.objects.count()} exercícios, '
            f'{SerieOuroDesafio.objects.count()} séries ouro, '
            f'{Recompensa.objects.count()} recompensas.'
        ))
