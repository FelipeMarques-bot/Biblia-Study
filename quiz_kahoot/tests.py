from django.test import TestCase, Client
from django.urls import reverse

from courses.models import Trilha, LicaoBiblica, Exercicio
from .models import QuizRoom
from .quiz_utils import selecionar_perguntas


def _trilha(nome, nivel):
    return Trilha.objects.create(
        nome=nome, faixa_etaria='adulto', nivel=nivel, ordem=0
    )


def _licao(trilha, titulo, qtd):
    licao = LicaoBiblica.objects.create(
        trilha=trilha, titulo=titulo, texto_base='Base',
        referencia='Gn 1:1', ordem=0,
    )
    for i in range(qtd):
        Exercicio.objects.create(
            licao=licao, tipo='MULTIPLA_ESCOLHA',
            enunciado=f'{titulo} pergunta {i}',
            dados={'alternativas': ['a', 'b', 'c', 'd'], 'indice_correto': 0},
            ordem=i,
        )
    return licao


class SelecionarPerguntasTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        ini = _trilha('Iniciante', 'iniciante')
        med = _trilha('Intermediario', 'intermediario')
        ava = _trilha('Avancado', 'avancado')
        _licao(ini, 'T1', 10)
        _licao(med, 'T2', 3)
        _licao(ava, 'T3', 8)

    _COUNTER = 1

    def _room(self, nivel, total):
        room = QuizRoom.objects.create(
            pin=f'{self._COUNTER:06d}',
            perguntas_total=total,
            nivel=nivel,
        )
        type(self)._COUNTER += 1
        self.addCleanup(room.questions.all().delete)
        selecionar_perguntas(room)
        return room

    def _niveis(self, room):
        from collections import Counter
        c = Counter()
        for q in room.questions.all():
            c[Exercicio.objects.get(id=q.exercicio_id).licao.trilha.nivel] += 1
        return c

    def test_quantidade_maxima_20(self):
        room = QuizRoom.objects.create(
            pin='maxq20', perguntas_total=99, nivel='todos',
        )
        selecionar_perguntas(room)
        self.assertLessEqual(room.questions.count(), 20)
        self.assertGreaterEqual(room.questions.count(), 5)

    def test_quantidades_permitidas(self):
        for total in (5, 10, 12, 15, 20):
            room = self._room('avancado', total)
            self.assertEqual(room.questions.count(), total)

    def test_filtra_por_nivel(self):
        room = self._room('avancado', 5)
        niveis = self._niveis(room)
        self.assertEqual(room.questions.count(), 5)
        self.assertEqual(set(niveis), {'avancado'})

    def test_complementa_quando_nivel_insuficiente(self):
        room = self._room('intermediario', 5)
        niveis = self._niveis(room)
        self.assertEqual(sum(niveis.values()), 5)
        self.assertGreaterEqual(niveis.get('intermediario', 0), 1)
        self.assertLessEqual(niveis.get('intermediario', 0), 3)

    def test_todos_os_niveis(self):
        room = self._room('todos', 10)
        self.assertEqual(room.questions.count(), 10)


class CriarSalaViewTest(TestCase):

    def test_cria_sala_com_nivel_e_quantidade(self):
        c = Client()
        resp = c.post(reverse('quiz_join'), {
            'action': 'create',
            'nome': 'Host',
            'nivel': 'avancado',
            'perguntas': '12',
        })
        self.assertEqual(resp.status_code, 302)
        room = QuizRoom.objects.latest('created_at')
        self.assertEqual(room.nivel, 'avancado')
        self.assertEqual(room.perguntas_total, 12)
        self.assertTrue(c.session.get(f'quiz_host_{room.pin}'))

    def test_ignora_nivel_invalido(self):
        c = Client()
        c.post(reverse('quiz_join'), {
            'action': 'create',
            'nome': 'Host',
            'nivel': 'hacker',
            'perguntas': '20',
        })
        room = QuizRoom.objects.latest('created_at')
        self.assertEqual(room.nivel, 'todos')
        self.assertEqual(room.perguntas_total, 20)