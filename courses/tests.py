from django.test import TestCase

from courses.models import Trilha, LicaoBiblica, Exercicio
from courses.management.commands.seed_extras import Command


def _contagens():
    return {
        'trilhas': Trilha.objects.count(),
        'licoes': LicaoBiblica.objects.count(),
        'exercicios': Exercicio.objects.count(),
    }


class TrilhaSuperCristaoTest(TestCase):

    def test_label_super_cristao(self):
        t = Trilha.objects.create(
            nome='X', descricao='', faixa_etaria='adulto',
            nivel='super_cristao', ordem=0,
        )
        self.assertEqual(t.get_nivel_display(), 'Super Cristão')

    def test_escolhas_incluem_super_cristao(self):
        niveis = {v for v, _ in Trilha._meta.get_field('nivel').choices}
        self.assertIn('super_cristao', niveis)


class SeedExtrasIdempotenciaTest(TestCase):

    def test_seed_extras_duas_execucoes_nao_duplica(self):
        cmd = Command()
        cmd.handle()
        primeiro = _contagens()
        self.assertGreaterEqual(primeiro['exercicios'], 240)
        self.assertGreaterEqual(primeiro['trilhas'], 6)

        cmd.handle()
        self.assertEqual(primeiro, _contagens())