"""Inline fallback seed - creates essential trilhas directly (no external script dependency).
Used when seed_v2.py fails during Render build."""
import sys

from django.core.management.base import BaseCommand
from courses.models import Trilha, LicaoBiblica, Exercicio
from gamification.models import Recompensa, SerieOuroDesafio, SerieOuroExercicio


def mk_trilha(nome, desc, faixa, nivel, ordem, icone):
    t, _ = Trilha.objects.get_or_create(
        nome=nome,
        defaults=dict(descricao=desc, faixa_etaria=faixa, nivel=nivel, ordem=ordem, icone=icone),
    )
    return t


def mk_licao(trilha, titulo, texto, ref, obj, resumo, ordem, xp=50):
    l, _ = LicaoBiblica.objects.get_or_create(
        trilha=trilha, titulo=titulo,
        defaults=dict(
            descricao=obj, texto_base=texto, referencia=ref,
            objetivo=obj, resumo=resumo, ordem=ordem, xp_recompensa=xp,
        ),
    )
    return l


def mk_ex(licao, tipo, enun, dados, ordem=1, peso=1):
    Exercicio.objects.get_or_create(
        licao=licao, enunciado=enun[:200],
        defaults=dict(tipo=tipo, dados=dados, ordem=ordem, peso_dificuldade=peso),
    )


def mc(enun, alts, cor, dica='', peso=1):
    return ('MULTIPLA_ESCOLHA', enun, dict(alternativas=alts, indice_correto=cor, dica=dica), peso)


def vf(enun, af, res, dica='', peso=1):
    return ('VF', enun, dict(afirmativa=af, alternativas=['Falso', 'Verdadeiro'], indice_correto=res, dica=dica), peso)


class Command(BaseCommand):
    help = 'Inline fallback seed - creates essential trilhas if seed_v2.py fails.'

    def handle(self, *args, **options):
        if Trilha.objects.count() > 0:
            self.stdout.write(self.style.SUCCESS('Database already has trilhas. Skipping inline seed.'))
            return

        self.stdout.write('Running inline fallback seed...')

        # ── TRILHA 1: Criação e Patriarcas ──
        t1 = mk_trilha(
            'Criação e Patriarcas', 'Gênesis: de Adão a José - as origens da humanidade e do povo de Israel',
            'adulto', 'iniciante', 1, 'open_in_new',
        )
        l1 = mk_licao(t1, 'A Obra da Criação',
            'No princípio Deus criou os céus e a terra. Em seis dias criou tudo: luz, firmamento, mares, vegetação, luminares, animais e o ser humano à Sua imagem. No sétimo dia descansou.',
            'Gênesis 1:1-2:3', 'Compreender a ordem e propósito da criação divina',
            'Deus criou o universo em seis dias por Sua palavra, culminando com a humanidade.', 1)
        mk_ex(l1, *mc('Quem criou os céus e a terra?', ['Adão', 'Noé', 'Deus', 'Abraão'], 2, 'Gênesis 1:1'))
        mk_ex(l1, *mc('Em quantos dias Deus criou tudo?', ['5', '6', '7', '3'], 1, 'Gênesis 1:31'))
        mk_ex(l1, *vf('Deus criou o homem à Sua imagem.', 'Deus criou o homem à Sua imagem.', 1, 'Gênesis 1:27'))

        l2 = mk_licao(t1, 'A Queda e Suas Consequências',
            'Deus colocou Adão e Eva no Éden com liberdade para comer de todas as árvores, exceto a árvore do conhecimento do bem e do mal. A serpente enganou Eva, que comeu e deu a Adão.',
            'Gênesis 3:1-24', 'Entender o pecado original e suas consequências',
            'A desobediência trouxe a morte espiritual e a separação de Deus.', 2)
        mk_ex(l2, *mc('Qual árvore Deus proibiu?', ['Da vida', 'Do conhecimento do bem e do mal', 'Da ciência', 'Da sabedoria'], 1, 'Gênesis 2:17'))
        mk_ex(l2, *vf('Eva comeu primeiro da fruta proibida.', 'Eva comeu primeiro da fruta proibida.', 1, 'Gênesis 3:6'))

        l3 = mk_licao(t1, 'A Arca de Noé',
            'Deus viu a maldade humana e decidiu destruir a terra com dilúvio, mas achou graça em Noé. Noé construiu a arca conforme as instruções, levando sua família e pares de animais.',
            'Gênesis 6:1-9:17', 'Reconhecer o juízo divino e a fidelidade de Deus',
            'Noé obedeceu em tudo. Depois do dilúvio, Deus fez aliança com um arco-íris.', 3)
        mk_ex(l3, *mc('Por quantos dias choveu?', ['20', '30', '40', '50'], 2, 'Gênesis 7:12'))

        # ── TRILHA 2: Êxodo e a Lei ──
        t2 = mk_trilha(
            'Êxodo e a Lei', 'Do cativeiro no Egito à entrega da Lei no Sinai',
            'adulto', 'iniciante', 2, 'exit_to_app',
        )
        l4 = mk_licao(t2, 'O Êxodo do Egito',
            'Deus livrou Israel do cativeiro egípcio com 10 pragas poderosas. O Cordeiro Pascal salvou os primogênitos israelitas. O mar Vermelho se abriu para o povo atravessar.',
            'Êxodo 12-15', 'Compreender a redenção tipológica do Êxodo',
            'O êxodo é o maior ato redentor do Antigo Testamento, prefigurando Cristo.', 1)
        mk_ex(l4, *mc('Quantas pragas Deus enviou ao Egito?', ['7', '10', '12', '5'], 1, 'Êxodo 7-12'))
        mk_ex(l4, *vf('O mar Vermelho se abriu para Israel.', 'O mar Vermelho se abriu para Israel.', 1, 'Êxodo 14:21-22'))

        l5 = mk_licao(t2, 'A Entrega da Lei',
            'Deus deu os Dez Mandamentos e a Lei no Monte Sinai. A Lei revela a justiça de Deus e a incapacidade humana de cumpri-la perfeitamente.',
            'Êxodo 20-24', 'Entender o propósito da Lei na economia da salvação',
            'A Lei é espelho que mostra nosso pecado e guia que aponta para Cristo.', 2)
        mk_ex(l5, *mc('Onde Deus deu os Dez Mandamentos?', ['Jerusalém', 'Sinai', 'Canaã', 'Betel'], 1, 'Êxodo 19:20'))

        # ── TRILHA 3: Salmos e Adoração ──
        t3 = mk_trilha(
            'Salmos e Adoração', 'O livro de orações e louvores de Israel',
            'adulto', 'iniciante', 3, 'menu_book',
        )
        l6 = mk_licao(t3, 'O Salmo 23 - O Senhor é meu Pastor',
            'O Salmo mais conhecido da Bíblia. Davi descreve Deus como um pastor cuidadoso que guia, provê e protege seu rebanho.',
            'Salmo 23', 'Experimentar o cuidado pastoral de Deus',
            'Deus cuida de cada detalhe da vida do crente, como um pastor de suas ovelhas.', 1)
        mk_ex(l6, *mc('Quem escreveu o Salmo 23?', ['Moisés', 'Davi', 'Salomão', 'Paulo'], 1, 'Salmo 23 (título)'))
        mk_ex(l6, *vf('O Senhor é meu pastor, nada me faltará.', 'O Senhor é meu pastor, nada me faltará.', 1, 'Salmo 23:1'))

        l7 = mk_licao(t3, 'Salmos de Arrependimento',
            'Davi arrependeu-se profundamente de seu pecado com Bate-Seba. O Salmo 51 é a expressão máxima de arrependimento bíblico.',
            'Salmo 51', 'Entender o arrependimento sincero diante de Deus',
            'O arrependimento verdadeiro reconhece a gravidade do pecado e clama pela misericórdia de Deus.', 2)
        mk_ex(l7, *vf('Davi pecou contra Deus com Bate-Seba.', 'Davi pecou contra Deus com Bate-Seba.', 1, '2 Samuel 11'))

        # ── TRILHA 4: Profecias Messiânicas ──
        t4 = mk_trilha(
            'Profecias Messiânicas', 'As promessas do Antigo Testamento sobre o Messias',
            'adulto', 'intermediario', 4, 'auto_stories',
        )
        l8 = mk_licao(t4, 'A Promessa em Gênesis 3:15',
            'Logo após a queda, Deus prometeu que a semente da mulher esmagaria a cabeça da serpente. Esta é a primeira profecia messiânica (Protevangelium).',
            'Gênesis 3:15', 'Reconhecer que Cristo é prometido desde o início',
            'Todo o Antigo Testamento aponta para a vinda de Cristo, o Redentor prometido.', 1)
        mk_ex(l8, *mc('O que a semente da mulher fará à serpente?', ['Fugirá', 'Esmagará a cabeça', 'Servirá', 'Morrerá'], 1, 'Gênesis 3:15'))

        l9 = mk_licao(t4, 'Isaías 53 - O Servo Sofredor',
            'A profecia mais clara sobre a crucificação de Jesus no Antigo Testamento. O Servo sofrerá pelos pecados do povo.',
            'Isaías 53:1-12', 'Entender a substituição vicária de Cristo',
            'Cristo foi ferido pelas nossas transgressões e moído pelas nossas iniquidades.', 2)
        mk_ex(l9, *mc('Pelos pecados de quem o Servo sofreu?', ['Dele mesmo', 'Do povo', 'Dos gentios', 'Dos anjos'], 1, 'Isaías 53:5'))

        # ── TRILHA 5: Jesus e o Evangelho ──
        t5 = mk_trilha(
            'Jesus e o Evangelho', 'A vida, morte e ressurreição de Jesus Cristo',
            'adulto', 'iniciante', 5, 'church',
        )
        l10 = mk_licao(t5, 'O Nascimento de Jesus',
            'Jesus nasceu em Belém de uma virgem, cumprindo as profecias messiânicas. Anunciado por anjos aos pastores.',
            'Lucas 2:1-20', 'Reconhecer a encarnação como ato de humildade divina',
            'Deus se fez homem para habitar entre os homens e salvá-los.', 1)
        mk_ex(l10, *mc('Onde Jesus nasceu?', ['Jerusalém', 'Belém', 'Nazaré', 'Egito'], 1, 'Lucas 2:4'))
        mk_ex(l10, *vf('Jesus nasceu de uma virgem.', 'Jesus nasceu de uma virgem.', 1, 'Lucas 1:26-35'))

        l11 = mk_licao(t5, 'A Cruz e a Ressurreição',
            'Jesus foi crucificado em Jerusalém, morrendo como cordeiro pascal pelos nossos pecados. No terceiro dia, ressuscitou vencendo a morte.',
            'Mateus 26-28', 'Entender o alcance redentor da morte e ressurreição de Cristo',
            'Na cruz, Deus julgou o pecado em Cristo. Na ressurreição, venceu a morte.', 2)
        mk_ex(l11, *mc('Em que dia Jesus ressuscitou?', ['Quinto', 'Sexto', 'Sétimo', 'Terceiro'], 1, 'Mateus 28:1'))
        mk_ex(l11, *vf('Jesus foi crucificado e ressuscitou.', 'Jesus foi crucificado e ressuscitou.', 1, '1 Coríntios 15:3-4'))

        # ── TRILHA 6: Atos e a Igreja Primitiva ──
        t6 = mk_trilha(
            'Atos e a Igreja', 'O nascimento da igreja e a expansão do evangelho',
            'adulto', 'iniciante', 6, 'groups',
        )
        l12 = mk_licao(t6, 'O Pentecostes',
            'O Espírito Santo desceu sobre os discípulos em Pentecostes, capacitando-os para pregar o evangelho em línguas estranhas.',
            'Atos 2:1-41', 'Entender a obra do Espírito Santo na igreja',
            'O Pentecostes marca o início da era da igreja, cumprindo a promessa de Jesus.', 1)
        mk_ex(l12, *mc('Quando o Espírito Santo desceu?', ['Páscoa', 'Pentecostes', 'Tabernáculos', 'Chanuca'], 1, 'Atos 2:1'))

        # ── TRILHA 7: Romanos e a Doutrina da Graça ──
        t7 = mk_trilha(
            'Romanos e a Graça', 'A epístola que fundamenta a teologia reformada',
            'adulto', 'intermediario', 7, 'balance',
        )
        l13 = mk_licao(t7, 'Justificação pela Fé',
            'Paulo ensina que somos justificados não por obras, mas pela fé em Jesus Cristo. A justiça de Deus se revela no evangelho.',
            'Romanos 1:17; 3:21-26', 'Compreender a justificação solo fide, solo gratia',
            'A justificação é um veredicto judicial onde Deus declara o pecador justo pela fé.', 1)
        mk_ex(l13, *mc('Somos justificados por:', ['Obras', 'Fé', 'Batismo', 'Lei'], 1, 'Romanos 3:28'))
        mk_ex(l13, *vf('A justiça de Deus se revela pela fé.', 'A justiça de Deus se revela pela fé.', 1, 'Romanos 1:17'))

        l14 = mk_licao(t7, 'A Soberania de Deus',
            'Deus é soberano sobre todas as coisas, incluindo a salvação. Ele escolhe, chama e guarda os Seus.',
            'Romanos 8:28-39', 'Entender e descansar na soberania de Deus',
            'Nada nos separará do amor de Deus em Cristo Jesus.', 2)
        mk_ex(l14, *vf('Deus trabalha todas as coisas para o bem dos que o amam.', 'Deus trabalha todas as coisas para o bem dos que o amam.', 1, 'Romanos 8:28'))

        # ── TRILHA 8: Efésios e a Vida Cristã ──
        t8 = mk_trilha(
            'Efésios e a Vida Cristã', 'Andando dignamente na vocação do evangelho',
            'adulto', 'iniciante', 8, 'directions_walk',
        )
        l15 = mk_licao(t8, 'Abençoes Espirituais',
            'Em Cristo, somos abençoados com toda bênção espiritual: eleitos, predestinados, redimidos, selados pelo Espírito.',
            'Efésios 1:3-14', 'Reconhecer as bênçãos espirituais em Cristo',
            'Tudo o que precisamos para a vida e piedade já nos foi dado em Cristo.', 1)
        mk_ex(l15, *mc('Como Paulo descreve as bênçãos espirituais em Cristo?', ['Duas', 'Sete', 'Toda', 'Nenhuma'], 2, 'Efésios 1:3'))

        # ── TRILHA 9: Hebreus e a Superioridade de Cristo ──
        t9 = mk_trilha(
            'Hebreus e Cristo', 'A epístola que demonstra a superioridade de Jesus sobre tudo',
            'adulto', 'avancado', 9, 'emoji_events',
        )
        l16 = mk_licao(t9, 'A Fé e os Heróis da Fé',
            'Hebreus 11 lista os heróis da fé que viveram e morreram crendon nas promessas de Deus.',
            'Hebreus 11', 'Crescer na fé observando os exemplos bíblicos',
            'A fé é a certeza do que esperamos e a prova do que não vemos.', 1)
        mk_ex(l16, *mc('O que é a fé segundo Hebreus?', ['Sentimento', 'Certeza e prova', 'Obras', 'Batismo'], 1, 'Hebreus 11:1'))

        # ── Recompensas ──
        Recompensa.objects.get_or_create(
            titulo='Estrela da Fé',
            defaults=dict(
                descricao='Complete a trilha de Fé',
                tipo='medalha',
                xp_recompensa=100,
                icone='Globe',
            ),
        )
        Recompensa.objects.get_or_create(
            titulo='Espada da Palavra',
            defaults=dict(
                descricao='Complete 10 lições',
                tipo='medalha',
                xp_recompensa=200,
                icone='Book',
            ),
        )
        Recompensa.objects.get_or_create(
            titulo='Coroa da Vida',
            defaults=dict(
                descricao='Complete todas as trilhas',
                tipo='medalha',
                xp_recompensa=500,
                icone='Cross',
            ),
        )

        final = Trilha.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'Inline seed complete! {final} trilhas, '
            f'{LicaoBiblica.objects.count()} lições, '
            f'{Exercicio.objects.count()} exercícios, '
            f'{Recompensa.objects.count()} recompensas.'
        ))
        if final == 0:
            self.stderr.write(self.style.ERROR('Inline seed created 0 trilhas!'))
            sys.exit(1)
