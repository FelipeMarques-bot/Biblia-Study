import os, django, sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()

from courses.models import Trilha, LicaoBiblica, Exercicio
from gamification.models import Recompensa, DesafioDiario, SerieOuroDesafio, SerieOuroExercicio

def criar_trilha(nome, desc, faixa, nivel, ordem, icone):
    t, _ = Trilha.objects.get_or_create(nome=nome, defaults=dict(descricao=desc, faixa_etaria=faixa, nivel=nivel, ordem=ordem, icone=icone))
    return t

def criar_licao(trilha, titulo, texto, ref, objetivo, resumo, ordem, xp=50):
    l, _ = LicaoBiblica.objects.get_or_create(trilha=trilha, titulo=titulo, defaults=dict(
        descricao=objetivo, texto_base=texto, referencia=ref, objetivo=objetivo, resumo=resumo, ordem=ordem, xp_recompensa=xp))
    return l

def criar_exercicio(licao, tipo, enunciado, dados, ordem=1, peso=1):
    Exercicio.objects.get_or_create(licao=licao, enunciado=enunciado[:200], defaults=dict(tipo=tipo, dados=dados, ordem=ordem, peso_dificuldade=peso))

def criar_desafio(data, titulo, desc, versiculo, pergunta, xp=30):
    DesafioDiario.objects.get_or_create(data=data, defaults=dict(titulo=titulo, descricao=desc, versiculo=versiculo, pergunta=pergunta, xp_recompensa=xp))

def criar_recompensa(tipo, titulo, desc, icone, xp, licoes=0, xp_min=0, streak=0):
    Recompensa.objects.get_or_create(titulo=titulo, defaults=dict(tipo=tipo, descricao=desc, icone=icone, xp_recompensa=xp, criterio_licoes=licoes, criterio_xp=xp_min, criterio_streak=streak))

def criar_serie_ouro(trilha, titulo, desc, faixa, nivel, xp, exercicios):
    so, _ = SerieOuroDesafio.objects.get_or_create(trilha=trilha, titulo=titulo, defaults=dict(descricao=desc, faixa_etaria=faixa, nivel=nivel, xp_recompensa=xp))
    for i, ex in enumerate(exercicios):
        SerieOuroExercicio.objects.get_or_create(desafio_ouro=so, enunciado=ex['e'][:200], defaults=dict(tipo=ex['t'], dados=ex['d'], peso_dificuldade=ex.get('p', 3)))
    return so

# ============================================================
# 1. CRIANÇAS - INICIANTE
# ============================================================
t_crianca1 = criar_trilha('Histórias da Criação', 'As origens segundo Gênesis para crianças', 'crianca', 'iniciante', 1, '🌍')
t_crianca2 = criar_trilha('Histórias de Jesus', 'Milagres e ensinos de Jesus para os pequenos', 'crianca', 'iniciante', 2, '✝️')

l = criar_licao(t_crianca1, 'O Primeiro Dia - A Luz', 'Gênesis 1:1-5', 'Gn 1:1-5', 'Saber que Deus criou a luz', 'Deus fez a luz no primeiro dia. Ele viu que a luz era boa.', 1, 40)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Deus criou no primeiro dia?', {"alternativas":["O sol","A luz","Os peixes","As árvores"],"indice_correto":1,"dica":"Gn 1:3 — Disse Deus: Haja luz!"}, 1)
criar_exercicio(l, 'VF', 'Deus viu que a luz era boa.', {"afirmativa":"Deus viu que a luz era boa.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"Gn 1:4 confirma isso."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Quem criou a luz?', {"alternativas":["Moisés","Os anjos","Deus","O homem"],"indice_correto":2,"dica":"Foi Deus quem criou os céus e a terra!"}, 3)

l = criar_licao(t_crianca1, 'Deus Criou os Animais', 'Gênesis 1:20-25', 'Gn 1:20-25', 'Conhecer os animais criados por Deus', 'Deus fez os peixes, pássaros e todos os animais.', 2, 40)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Em que dia Deus criou os peixes?', {"alternativas":["Primeiro dia","Terceiro dia","Quinto dia","Sétimo dia"],"indice_correto":2,"dica":"Gn 1:20-23"}, 1)
criar_exercicio(l, 'VF', 'Deus criou todos os animais de uma só vez.', {"afirmativa":"Deus criou todos os animais de uma só vez.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Deus criou em dias diferentes: peixes no 5º, animais terrestres no 6º."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Deus sentiu ao criar os animais?', {"alternativas":["Raiva","Tristeza","Viu que era bom","Indiferença"],"indice_correto":2,"dica":"Gn 1:25 — Viu Deus que era bom."}, 3)

l = criar_licao(t_crianca2, 'Jesus Ama as Crianças', 'Marcos 10:13-16', 'Mc 10:13-16', 'Saber que Jesus ama e acolhe as crianças', 'Jesus disse: Deixai vir a mim os pequeninos.', 1, 40)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que os discípulos fizeram com as crianças?', {"alternativas":["Chamaram","Abençoaram","Repreenderam","Brincaram"],"indice_correto":2,"dica":"Mc 10:13 — Os discípulos repreendiam as crianças."}, 1)
criar_exercicio(l, 'VF', 'Jesus ficou feliz com as crianças perto Dele.', {"afirmativa":"Jesus ficou feliz com as crianças perto Dele.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"Mc 10:14 — Jesus disse: Deixai vir a mim os pequeninos."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Jesus disse sobre as crianças?', {"alternativas":["Que atrapalhavam","Que delas é o Reino de Deus","Que deveriam ficar em casa","Que não entendiam"],"indice_correto":1,"dica":"Mc 10:14 — ...porque dos tais é o Reino de Deus."}, 3)

l = criar_licao(t_crianca2, 'O Milagre dos Pães e Peixes', 'João 6:1-14', 'Jo 6:1-14', 'Ver o poder de Jesus em multiplicar alimentos', 'Jesus alimentou 5.000 pessoas com cinco pães e dois peixes.', 2, 40)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Quantos pães o menino tinha?', {"alternativas":["Dois","Cinco","Sete","Dez"],"indice_correto":1,"dica":"Jo 6:9 — Há um menino com cinco pães."}, 1)
criar_exercicio(l, 'VF', 'Sobraram pedaços depois de todos comerem.', {"afirmativa":"Sobraram pedaços depois de todos comerem.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"Jo 6:12 — Encheram 12 cestos do que sobrou."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Quantos cestos sobraram?', {"alternativas":["5","7","12","20"],"indice_correto":2,"dica":"Jo 6:13 — Encheram doze cestos."}, 3)

l = criar_licao(t_crianca2, 'Jesus Acalma a Tempestade', 'Marcos 4:35-41', 'Mc 4:35-41', 'Confiar que Jesus tem poder sobre a natureza', 'Jesus mandou o vento e o mar se acalmarem, e eles obedeceram.', 3, 40)
criar_exercicio(l, 'VF', 'Os discípulos ficaram com medo na tempestade.', {"afirmativa":"Os discípulos ficaram com medo na tempestade.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"Mc 4:38 — Eles acordaram Jesus com medo."}, 1)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Jesus disse ao vento e ao mar?', {"alternativas":["Acalmem-se","Vão embora","Fiquem quietos","Silêncio"],"indice_correto":0,"dica":"Mc 4:39 — Disse: Acalma-te, quieta-te!"}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que aprendemos com esse milagre?', {"alternativas":["Jesus tem poder sobre tudo","Devemos ter medo do mar","Tempestades são sempre más","Jesus só ajuda adultos"],"indice_correto":0,"dica":"Jesus mostrou que tem poder sobre toda a criação."}, 3)

# ============================================================
# 2. ADOLESCENTES - INICIANTE
# ============================================================
t_ado1 = criar_trilha('Quem é Jesus?', 'Conhecendo a Pessoa de Cristo', 'adolescente', 'iniciante', 3, '👑')
t_ado2 = criar_trilha('Amizade e Fé', 'Relacionamentos à luz da Bíblia', 'adolescente', 'iniciante', 4, '🤝')

l = criar_licao(t_ado1, 'Jesus: Deus e Homem', 'João 1:1-14', 'Jo 1:1-14', 'Entender a natureza divina e humana de Cristo', 'O Verbo se fez carne e habitou entre nós.', 1, 50)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que João 1:1 diz que o Verbo era?', {"alternativas":["Um anjo","Um profeta","Deus","Um homem sábio"],"indice_correto":2,"dica":"Jo 1:1 — O Verbo era Deus."}, 1)
criar_exercicio(l, 'VF', 'Jesus existia antes de nascer em Belém.', {"afirmativa":"Jesus existia antes de nascer em Belém.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"Jo 1:1 — No princípio era o Verbo."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que significa "O Verbo se fez carne"?', {"alternativas":["Jesus virou um livro","Deus se tornou humano","João escreveu um livro","A Bíblia foi escrita"],"indice_correto":1,"dica":"Jo 1:14 — O Verbo se fez carne e habitou entre nós."}, 3)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'De onde veio Jesus segundo João 1?', {"alternativas":["De Nazaré","De junto de Deus","De Roma","De Jerusalém"],"indice_correto":1,"dica":"Jo 1:1-2 — Ele estava com Deus desde o princípio."}, 4)

l = criar_licao(t_ado1, 'Jesus Veio para Salvar', 'Lucas 19:1-10', 'Lc 19:1-10', 'Ver que Jesus busca os perdidos', 'Zaqueu foi salvo porque Jesus veio buscar e salvar o perdido.', 2, 50)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Zaqueu fazia?', {"alternativas":["Pescador","Cobrador de impostos","Médico","Sacerdote"],"indice_correto":1,"dica":"Lc 19:2 — Zaqueu era chefe dos publicanos."}, 1)
criar_exercicio(l, 'VF', 'Zaqueu subiu em uma árvore para ver Jesus.', {"afirmativa":"Zaqueu subiu em uma árvore para ver Jesus.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"Lc 19:4 — Subiu num sicômoro para vê-lo."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Jesus disse a Zaqueu?', {"alternativas":["Saia da árvore","Hoje preciso ficar em sua casa","Você é pecador","Vá e não peques mais"],"indice_correto":1,"dica":"Lc 19:5 — Hoje me convém ficar em tua casa."}, 3)

l = criar_licao(t_ado2, 'O Amigo Verdadeiro', 'Provérbios 18:24; João 15:13-15', 'Pv 18:24; Jo 15:13-15', 'Saber o que faz um amigo verdadeiro', 'O amigo verdadeiro ama em todos os momentos.', 1, 50)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Segundo Provérbios, o que faz um amigo verdadeiro?', {"alternativas":["Só aparece na alegria","Ama em todos os momentos","Dá presentes caros","Nunca discorda"],"indice_correto":1,"dica":"Pv 18:24 — Há amigo mais chegado que um irmão."}, 1)
criar_exercicio(l, 'VF', 'Jesus chamou os discípulos de servos, não de amigos.', {"afirmativa":"Jesus chamou os discípulos de servos, não de amigos.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Jo 15:15 — Já vos chamo amigos."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Qual o maior amor que alguém pode ter por um amigo?', {"alternativas":["Dar conselhos","Dar a própria vida","Dar dinheiro","Defender em toda briga"],"indice_correto":1,"dica":"Jo 15:13 — Ninguém tem maior amor do que este."}, 3)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Como Jesus nos mostrou esse amor?', {"alternativas":["Ensinando com parábolas","Morrendo na cruz","Fazendo milagres","Escolhendo 12 discípulos"],"indice_correto":1,"dica":"Jo 15:13 — Dar a vida pelos amigos."}, 4)

l = criar_licao(t_ado2, 'Fé em Meio às Dúvidas', 'Marcos 9:14-29', 'Mc 9:14-29', 'Aprender que fé e dúvida podem coexistir', 'O pai do menino disse: Creio, ajuda a minha incredulidade.', 2, 50)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que o pai do menino disse a Jesus?', {"alternativas":["Meu filho está bem","Creio, ajuda minha incredulidade","Cura meu filho","Tenho fé"],"indice_correto":1,"dica":"Mc 9:24 — Disse com lágrimas."}, 1)
criar_exercicio(l, 'VF', 'Os discípulos conseguiram expulsar o espírito sozinhos.', {"afirmativa":"Os discípulos conseguiram expulsar o espírito sozinhos.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Mc 9:18 — Não puderam expulsar."}, 2)
criar_exercicio(l, 'ORDENACAO', 'Ordene os eventos da história:', {"itens":["O pai pede ajuda a Jesus","Jesus pergunta sobre o menino","O pai diz: Creio!","Jesus expulsa o espírito","O menino é curado"]}, 3, 2)

# ============================================================
# 3. ADULTOS - INICIANTE
# ============================================================
t_adulto1 = criar_trilha('Fundamentos da Bíblia', 'As doutrinas elementares da fé cristã para adultos', 'adulto', 'iniciante', 11, '📖')
t_adulto2 = criar_trilha('Evangelhos em Foco', 'Estudo dos quatro evangelhos e a vida de Cristo', 'adulto', 'iniciante', 12, '✝️')

l = criar_licao(t_adulto1, 'A Promessa a Abraão', 'Gênesis 12:1-9; 15:1-6', 'Gn 12:1-9; 15:1-6', 'Entender a fé de Abraão como modelo', 'Abraão creu em Deus e isso lhe foi imputado como justiça.', 3, 50)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Deus pediu que Abraão fizesse?', {"alternativas":["Construísse um altar","Saisse da sua terra","Fosse ao Egito","Esperasse 100 anos"],"indice_correto":1,"dica":"Gn 12:1 — Sai da tua terra."}, 1)
criar_exercicio(l, 'VF', 'Abraão obedeceu imediatamente à chamada de Deus.', {"afirmativa":"Abraão obedeceu imediatamente à chamada de Deus.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"Gn 12:4 — Partiu Abrão como o Senhor lhe dissera."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Gênesis 15:6 diz sobre a fé de Abraão?', {"alternativas":["Foi recompensada com riquezas","Foi imputada como justiça","Foi considerada loucura","Foi testada e aprovada"],"indice_correto":1,"dica":"Gn 15:6 — Creu no Senhor, e foi-lhe imputado por justiça."}, 3)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Qual lição principal da vida de Abraão?', {"alternativas":["A fé é recompensa por boas obras","Deus cumpre Suas promessas","Precisamos viajar para ser abençoados","A justiça vem pelo esforço"],"indice_correto":1,"dica":"A fé de Abraão nos ensina a confiar nas promessas de Deus."}, 4)

l = criar_licao(t_adulto2, 'O Sermão do Monte - As Bem-Aventuranças', 'Mateus 5:1-12', 'Mt 5:1-12', 'Compreender o caráter do Reino de Deus', 'Bem-aventurados os pobres de espírito, porque deles é o Reino dos Céus.', 2, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Quem Jesus declara bem-aventurado primeiro?', {"alternativas":["Os mansos","Os pobres de espírito","Os que choram","Os pacificadores"],"indice_correto":1,"dica":"Mt 5:3 — Bem-aventurados os pobres de espírito."}, 1)
criar_exercicio(l, 'VF', 'As Bem-aventuranças prometem vida fácil aos crentes.', {"afirmativa":"As Bem-aventuranças prometem vida fácil aos crentes.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Jesus fala de perseguição e aflição, mas com promessa de consolo."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que significa ser pobre de espírito?', {"alternativas":["Ser pobre financeiramente","Reconhecer necessidade espiritual de Deus","Ter pouco conhecimento","Ser humilde financeiramente"],"indice_correto":1,"dica":"É reconhecer que dependemos totalmente de Deus."}, 3)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Qual promessa é feita aos misericordiosos?', {"alternativas":["Herdeiros da terra","Cheios de justiça","Alcançarão misericórdia","Verão a Deus"],"indice_correto":2,"dica":"Mt 5:7 — Bem-aventurados os misericordiosos."}, 4)
criar_exercicio(l, 'ORDENACAO', 'Coloque as Bem-aventuranças na ordem de Mateus 5:', {"itens":["Pobres de espírito","Os que choram","Mansos","Fome e sede de justiça","Misericordiosos","Limpos de coração","Pacificadores","Perseguidos"]}, 5, 3)

l = criar_licao(t_adulto2, 'A Parábola do Semeador', 'Mateus 13:1-23', 'Mt 13:1-23', 'Discernir os diferentes corações que recebem a Palavra', 'A semente é a Palavra; o coração fértil produz fruto.', 3, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que representa a semente na parábola?', {"alternativas":["O dinheiro","A Palavra de Deus","O pecado","A fé"],"indice_correto":1,"dica":"Mt 13:19 — A semente é a Palavra do Reino."}, 1)
criar_exercicio(l, 'ASSOCIACAO', 'Associe cada tipo de solo ao seu significado:', {"pares":[{"esquerda":"Beira do caminho","direita_correta":"Não entende a Palavra"},{"esquerda":"Solo rochoso","direita_correta":"Recebe com alegria, mas não persiste"},{"esquerda":"Espinhos","direita_correta":"Preocupações sufocam a Palavra"},{"esquerda":"Boa terra","direita_correta":"Ouve, entende e frutifica"}]}, 2, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Qual solo produz fruto?', {"alternativas":["Beira do caminho","Solo rochoso","Entre espinhos","Boa terra"],"indice_correto":3,"dica":"Mt 13:23 — O que foi semeado em boa terra."}, 3)

# ============================================================
# 4. CRIANÇAS INTERMEDIÁRIO - C3: Heróis da Fé
# ============================================================
t_c3 = criar_trilha('Heróis da Fé', 'Personagens bíblicos que confiaram em Deus', 'crianca', 'intermediario', 5, '🛡️')

l = criar_licao(t_c3, 'Noé Confiou em Deus', 'Gênesis 6-9 (recorte)', 'Gn 6-9', 'Mostrar obediência de Noé em meio à incredulidade', 'Noé construiu a arca pela fé e Deus o salvou.', 1, 50)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Por que Noé construiu a arca?', {"alternativas":["Para viajar","Porque Deus mandou","Para pescar","Para se esconder"],"indice_correto":1,"dica":"Gn 6:22 — Assim fez Noé, conforme Deus lhe ordenou."}, 1)
criar_exercicio(l, 'VF', 'Deus se esquece das Suas promessas.', {"afirmativa":"Deus se esquece das Suas promessas.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"O arco-íris lembra a aliança de Deus."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que o arco-íris representa?', {"alternativas":["O fim da chuva","A aliança de Deus","Uma ilusão","A volta de Noé"],"indice_correto":1,"dica":"Gn 9:13 — Meu arco nas nuvens como sinal da aliança."}, 3)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Como podemos obedecer a Deus hoje?', {"alternativas":["Construindo uma arca","Confiar na Palavra mesmo quando outros zombam","Escondendo nossa fé","Só obedecendo quando é fácil"],"indice_correto":1,"dica":"A fé verdadeira obedece mesmo quando os outros não entendem."}, 4)

l = criar_licao(t_c3, 'Abraão Confiou na Promessa', 'Gênesis 12; 15', 'Gn 12; 15', 'Falar de fé e promessa sem barganha', 'Abraão creu em Deus e foi chamado amigo de Deus.', 2, 50)
criar_exercicio(l, 'VF', 'Abraão era velho quando Deus prometeu um filho.', {"afirmativa":"Abraão era velho quando Deus prometeu um filho.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"Gn 12:4 — Abrão tinha 75 anos quando partiu."}, 1)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Abraão fez quando Deus chamou?', {"alternativas":["Pediu mais sinais","Fez perguntas","Obedeceu e partiu","Esperou 10 anos"],"indice_correto":2,"dica":"Gn 12:4 — Partiu como o Senhor lhe dissera."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que aprendemos com Abraão?', {"alternativas":["Precisamos ver para crer","A fé confia no caráter de Deus","Só obedecemos se for conveniente","Deus só abençoa perfeitos"],"indice_correto":1,"dica":"Abraão confiou que Deus é fiel."}, 3)

l = criar_licao(t_c3, 'Davi: Um Rei Que Apontava para Cristo', '1 Samuel 16; 2 Samuel 7', '1Sm 16; 2Sm 7', 'Mostrar Davi como servo imperfeito que aponta para o Rei perfeito', 'Davi era segundo o coração de Deus, mas também pecava e se arrependia.', 3, 50)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Quem escolheu Davi para ser rei?', {"alternativas":["Samuel","O povo","Deus","Saul"],"indice_correto":2,"dica":"1Sm 16:7 — Deus vê o coração."}, 1)
criar_exercicio(l, 'VF', 'Davi nunca pecou.', {"afirmativa":"Davi nunca pecou.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Davi pecou gravemente, mas se arrependeu."}, 2)
criar_exercicio(l, 'ASSOCIACAO', 'Associe cada personagem ao que representa:', {"pares":[{"esquerda":"Davi","direita_correta":"Rei imperfeito que aponta para Cristo"},{"esquerda":"Golias","direita_correta":"Inimigo vencido por Deus"},{"esquerda":"Jesus","direita_correta":"Rei perfeito prometido"}]}, 3)

l = criar_licao(t_c3, 'José: Perdão e Propósito', 'Gênesis 37; 45; 50', 'Gn 37;45;50', 'Ver como Deus usa até o sofrimento para o bem', 'Deus transformou o mal em bem na vida de José.', 4, 50)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que os irmãos de José fizeram com ele?', {"alternativas":["Abraçaram","Venderam como escravo","Pedir desculpas","Deram presentes"],"indice_correto":1,"dica":"Gn 37:28 — Venderam José por 20 moedas."}, 1)
criar_exercicio(l, 'VF', 'Josém se vingou de seus irmãos.', {"afirmativa":"José se vingou de seus irmãos.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Gn 50:20 — Vós planejastes o mal, Deus o tornou em bem."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que José disse sobre o que seus irmãos fizeram?', {"alternativas":["Vou me vingar","Deus transformou em bem","Nunca mais quero vê-los","Foram maus"],"indice_correto":1,"dica":"Gn 50:20 — Deus tornou em bem."}, 3)

# ============================================================
# 5. ADOLESCENTES INTERMEDIÁRIO - A3: Vivendo a Fé
# ============================================================
t_a3 = criar_trilha('Vivendo a Fé na Escola e em Casa', 'Aplicar a fé no dia a dia', 'adolescente', 'intermediario', 6, '🏠')

l = criar_licao(t_a3, 'Identidade em Cristo', 'Efésios 1:3-7; 1Pe 2:9', 'Ef 1:3-7; 1Pe 2:9', 'Saber que nossa identidade está em Cristo, não na opinião alheia', 'Em Cristo fomos escolhidos, amados e perdoados.', 1, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Efésios 1 diz que recebemos em Cristo?', {"alternativas":["Riquezas","Toda bênção espiritual","Fama","Poder terreno"],"indice_correto":1,"dica":"Ef 1:3 — Abençoado com toda bênção espiritual."}, 1)
criar_exercicio(l, 'VF', 'Meu valor vem do meu desempenho e notas.', {"afirmativa":"Meu valor vem do meu desempenho e notas.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Nosso valor vem de sermos amados e escolhidos por Deus."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Como 1 Pedro 2:9 descreve os crentes?', {"alternativas":["Povo qualquer","Nação santa, povo exclusivo de Deus","Grupo religioso","Comunidade perfeita"],"indice_correto":1,"dica":"1Pe 2:9 — Vocês são geração eleita, sacerdócio real."}, 3)

l = criar_licao(t_a3, 'Luta Contra o Pecado', 'Romanos 7:14-25; 1Jo 1:8-9', 'Rm 7:14-25; 1Jo 1:8-9', 'Entender que a vida cristã inclui luta com o pecado e graça', 'Não faço o bem que quero, mas o mal que não quero.', 2, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Paulo descreve em Romanos 7?', {"alternativas":["Vida perfeita","Luta interna contra o pecado","Como ser salvo por obras","Vida sem problemas"],"indice_correto":1,"dica":"Rm 7:19 — Não faço o bem que quero."}, 1)
criar_exercicio(l, 'VF', 'Quando pecamos, devemos esconder e fingir que nada aconteceu.', {"afirmativa":"Quando pecamos, devemos esconder e fingir que nada aconteceu.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"1Jo 1:9 — Se confessarmos, Ele é fiel para perdoar."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que significa arrependimento verdadeiro?', {"alternativas":["Sentir remorso","Mudar de direção e confiar em Cristo","Pedir desculpa","Tentar ser melhor"],"indice_correto":1,"dica":"Arrependimento é mudança de mente que leva a mudança de vida."}, 3)

l = criar_licao(t_a3, 'Graça que Educa', 'Tito 2:11-14', 'Tt 2:11-14', 'Saber que a graça nos ensina a viver de forma santa', 'A graça de Deus nos educa a renunciar à impiedade.', 3, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que a graça de Deus faz segundo Tito 2?', {"alternativas":["Nos dá liberdade para pecar","Nos educa a viver de forma santa","Só perdoa","Ignora o pecado"],"indice_correto":1,"dica":"Tt 2:12 — Educa-nos a renunciar à impiedade."}, 1)
criar_exercicio(l, 'VF', 'Graça significa que não precisamos nos preocupar com o pecado.', {"afirmativa":"Graça significa que não precisamos nos preocupar com o pecado.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"A graça nos educa a dizer não ao pecado."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Como aplicar a graça no uso da internet?', {"alternativas":["Tudo é permitido","Usar com sabedoria para glória de Deus","Só conteúdo religioso","Evitar totalmente"],"indice_correto":1,"dica":"Graça nos ensina a viver com sabedoria em todas as áreas."}, 3)

l = criar_licao(t_a3, 'Fé Viva em Meio à Pressão', 'Daniel 3', 'Dn 3', 'Ser fiel a Deus acima da aprovação humana', 'Deus pode livrar, mas mesmo que não, Ele continua sendo Deus.', 4, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Nabucodonosor ordenou?', {"alternativas":["Que todos orassem","Que todos adorassem a estátua","Que lessem a Bíblia","Que jejuassem"],"indice_correto":1,"dica":"Dn 3:5 — Ao som dos instrumentos, todos se prostrariam."}, 1)
criar_exercicio(l, 'VF', 'Os três jovens se curvaram à estátua por medo.', {"afirmativa":"Os três jovens se curvaram à estátua por medo.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Dn 3:18 — Não serviremos a teus deuses."}, 2)
criar_exercicio(l, 'ASSOCIACAO', 'Associe cada elemento à história:', {"pares":[{"esquerda":"Fornalha","direita_correta":"Lugar de provação"},{"esquerda":"Anjo","direita_correta":"Proteção de Deus"},{"esquerda":"Quarto homem","direita_correta":"Presença divina"}]}, 3)

l = criar_licao(t_a3, 'Perdão Entre Amigos', 'Mateus 18:21-35', 'Mt 18:21-35', 'Entender que o perdão que recebemos deve fluir para outros', 'Perdoai para que sejais perdoados.', 5, 50)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Quantas vezes Pedro perguntou se devia perdoar?', {"alternativas":["3","7","70x7","150"],"indice_correto":2,"dica":"Mt 18:22 — Não até sete, mas até setenta vezes sete."}, 1)
criar_exercicio(l, 'VF', 'Devemos perdoar porque já fomos perdoados por Deus.', {"afirmativa":"Devemos perdoar porque já fomos perdoados por Deus.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"A parábola mostra que quem muito foi perdoado, muito deve perdoar."}, 2)
criar_exercicio(l, 'ORDENACAO', 'Ordene a parábola do credor incompassivo:', {"itens":["Servo deve 10 mil talentos","Rei perdoa a dívida","Servo cobra 100 denários do outro","Servo é cobrado pelo rei","Rei o entrega aos torturadores"]}, 3, 2)

# ============================================================
# 6. ADULTOS INTERMEDIÁRIO - D3: Vida Cristã no Dia a Dia
# ============================================================
t_d3 = criar_trilha('Vida Cristã no Dia a Dia', 'Aplicando a fé no trabalho, família e sofrimento', 'adulto', 'intermediario', 7, '🏡')

l = criar_licao(t_d3, 'Trabalhando para a Glória de Deus', 'Colossenses 3:23-24', 'Cl 3:23-24', 'Ver o trabalho como serviço a Deus', 'Tudo quanto fizerdes, fazei de coração como ao Senhor.', 1, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Como devemos trabalhar segundo Colossenses?', {"alternativas":["Apenas pelo salário","De coração como para o Senhor","Com pressa","Buscando promoção"],"indice_correto":1,"dica":"Cl 3:23 — De coração, como ao Senhor."}, 1)
criar_exercicio(l, 'VF', 'Só o trabalho religioso tem valor eterno.', {"afirmativa":"Só o trabalho religioso tem valor eterno.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Todo trabalho feito para a glória de Deus tem valor."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que receberemos como recompensa?', {"alternativas":["Salário dobrado","Promoção","Herança do Senhor","Reconhecimento humano"],"indice_correto":2,"dica":"Cl 3:24 — Recebereis a recompensa da herança."}, 3)

l = criar_licao(t_d3, 'Família e Graça', 'Efésios 5:21-6:4', 'Ef 5:21-6:4', 'Viver a graça nos relacionamentos familiares', 'Sujeitai-vos uns aos outros no temor de Cristo.', 2, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Qual o fundamento dos relacionamentos em Efésios?', {"alternativas":["Autoridade","Sujeição mútua","Independência","Igualdade"],"indice_correto":1,"dica":"Ef 5:21 — Sujeitai-vos uns aos outros no temor de Cristo."}, 1)
criar_exercicio(l, 'VF', 'Pais devem provocar seus filhos à ira.', {"afirmativa":"Pais devem provocar seus filhos à ira.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Ef 6:4 — Pais, não provoqueis vossos filhos à ira."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que a graça traz para a família?', {"alternativas":["Regras rígidas","Amor sacrificial, perdão e cuidado","Competição","Perfeição"],"indice_correto":1,"dica":"A graça nos ensina a amar como Cristo amou."}, 3)

l = criar_licao(t_d3, 'Lidando com Ansiedade e Sofrimento', 'Filipenses 4:6-7; Romanos 8:28-39', 'Fp 4:6-7; Rm 8:28-39', 'Confiar na soberania de Deus em meio às lutas', 'Não estejais ansiosos; em tudo pela oração apresentai a Deus vossos pedidos.', 3, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que devemos fazer em vez de ficar ansiosos?', {"alternativas":["Parar de pensar","Orar e apresentar pedidos a Deus","Ignorar o problema","Trabalhar mais"],"indice_correto":1,"dica":"Fp 4:6 — Em tudo pela oração."}, 1)
criar_exercicio(l, 'VF', 'Romanos 8:28 diz que todas as coisas cooperam para o bem.', {"afirmativa":"Romanos 8:28 diz que todas as coisas cooperam para o bem.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"Rm 8:28 — Para os que amam a Deus, todas as coisas cooperam para o bem."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que pode nos separar do amor de Deus?', {"alternativas":["Tribulação","Angústia","Nada","Pecado"],"indice_correto":2,"dica":"Rm 8:38-39 — Nem morte, nem vida... nada pode nos separar."}, 3)

l = criar_licao(t_d3, 'Comunhão e Igreja Local', 'Hebreus 10:24-25; Atos 2:42-47', 'Hb 10:24-25; At 2:42-47', 'Entender a importância da vida em comunidade', 'Não deixando a congregação, como é costume de alguns.', 4, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Hebreus nos exorta a não deixar?', {"alternativas":["O trabalho","A congregação","A família","O estudo"],"indice_correto":1,"dica":"Hb 10:25 — Não deixando a nossa congregação."}, 1)
criar_exercicio(l, 'VF', 'A igreja primitiva vivia em comunhão e partilha.', {"afirmativa":"A igreja primitiva vivia em comunhão e partilha.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"At 2:44 — Todos os que criam estavam juntos e tinham tudo em comum."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Quais são os meios de graça na igreja?', {"alternativas":["Dinheiro e poder","Palavra, oração e sacramentos","Música e arte","Programas sociais"],"indice_correto":1,"dica":"Deus usa Sua Palavra, oração e os sacramentos para nos fortalecer."}, 3)

# ============================================================
# 7. ADULTOS AVANÇADO - D4: Doutrinas Centrais
# ============================================================
t_d4 = criar_trilha('Doutrinas Centrais', 'Fundamentos da fé cristã reformada', 'adulto', 'avancado', 8, '📚')

l = criar_licao(t_d4, 'Quem é Deus?', 'Êxodo 34:6-7; Salmo 103', 'Ex 34:6-7; Sl 103', 'Conhecer os atributos e o caráter de Deus', 'O Senhor é misericordioso, benigno, tardio em irar-se e grande em beneficência.', 1, 70)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Como Deus se descreve em Êxodo 34?', {"alternativas":["Deus irado","Misericordioso e benigno","Distante","Indiferente"],"indice_correto":1,"dica":"Ex 34:6 — Deus misericordioso e benigno."}, 1)
criar_exercicio(l, 'VF', 'Deus muda de ideia como os humanos.', {"afirmativa":"Deus muda de ideia como os humanos.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Deus é imutável em Seu caráter e propósitos."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que o Salmo 103 destaca sobre Deus?', {"alternativas":["Sua ira constante","Seu amor e compaixão","Suas exigências","Seu silêncio"],"indice_correto":1,"dica":"Sl 103:8 — Misericordioso e benigno, tardio em irar-se."}, 3)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que significa Deus ser santo?', {"alternativas":["Ser muito poderoso","Ser separado do pecado e perfeitamente puro","Ser distante","Ser misterioso"],"indice_correto":1,"dica":"Santidade é a perfeição moral de Deus."}, 4)

l = criar_licao(t_d4, 'Pecado e Depravação Humana', 'Romanos 3:9-26', 'Rm 3:9-26', 'Compreender a extensão do pecado e a necessidade da graça', 'Todos pecaram e estão destituídos da glória de Deus.', 2, 70)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Romanos 3 diz sobre a humanidade?', {"alternativas":["Todos são justos","Todos pecaram","Alguns são bons","Só os maus pecam"],"indice_correto":1,"dica":"Rm 3:23 — Todos pecaram."}, 1)
criar_exercicio(l, 'VF', 'O ser humano é essencialmente bom.', {"afirmativa":"O ser humano é essencialmente bom.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Rm 3:10 — Não há um justo, nem um sequer."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Qual a solução para o pecado?', {"alternativas":["Esforço humano","Boas obras","Justificação pela fé em Cristo","Religião"],"indice_correto":2,"dica":"Rm 3:24 — Justificados gratuitamente por Sua graça."}, 3)
criar_exercicio(l, 'ORDENACAO', 'Ordene a progressão do plano da redenção:', {"itens":["Criação","Queda","Promessa","Encarnação","Morte de Cristo","Ressurreição","Nova Criação"]}, 4, 3)

l = criar_licao(t_d4, 'Justificação pela Fé', 'Romanos 5:1-2; Gálatas 2:16', 'Rm 5:1-2; Gl 2:16', 'Saber que somos declarados justos somente pela fé em Cristo', 'Justificados pela fé, temos paz com Deus.', 3, 70)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Como somos justificados?', {"alternativas":["Pelos nossos méritos","Pela fé em Cristo","Pelos sacramentos","Pelos mandamentos"],"indice_correto":1,"dica":"Gl 2:16 — Não por obras da lei, mas pela fé em Cristo."}, 1)
criar_exercicio(l, 'VF', 'Justificação significa que Deus nos torna interiormente santos.', {"afirmativa":"Justificação significa que Deus nos torna interiormente santos.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Justificação é sermos declarados justos; santificação é sermos tornados santos."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Qual a diferença entre justificação e santificação?', {"alternativas":["São a mesma coisa","Justificação é declaração; santificação é processo","Não há diferença","Santificação é automática"],"indice_correto":1,"dica":"Justificação é instantânea; santificação é progressiva."}, 3)

l = criar_licao(t_d4, 'Santificação: Graça que Transforma', '1 Tessalonicenses 4:3; 1 Coríntios 6:11', '1Ts 4:3; 1Co 6:11', 'Entender a obra do Espírito que nos transforma', 'A vontade de Deus é a vossa santificação.', 4, 70)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Qual a vontade de Deus para nós?', {"alternativas":["Sucesso financeiro","Santificação","Saúde perfeita","Fama"],"indice_correto":1,"dica":"1Ts 4:3 — A vontade de Deus é a vossa santificação."}, 1)
criar_exercicio(l, 'VF', 'A santificação é obra exclusivamente humana.', {"afirmativa":"A santificação é obra exclusivamente humana.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Santificação é obra do Espírito Santo, com nossa cooperação."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que nos motiva à santificação?', {"alternativas":["Medo do castigo","Gratidão pela graça","Ganhar recompensas","Competição"],"indice_correto":1,"dica":"Respondemos à graça com gratidão e obediência."}, 3)

l = criar_licao(t_d4, 'Perseverança dos Santos', 'João 10:27-29; Filipenses 1:6', 'Jo 10:27-29; Fp 1:6', 'Descansar na segurança que Deus nos preserva até o fim', 'Aquele que começou a boa obra a aperfeiçoará até o dia de Cristo.', 5, 70)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Jesus promete sobre Suas ovelhas?', {"alternativas":["Podem se perder","Ninguém as arranca da Sua mão","São todas iguais","Precisam se salvar sozinhas"],"indice_correto":1,"dica":"Jo 10:28 — Nunca hão de perecer."}, 1)
criar_exercicio(l, 'VF', 'Podemos perder a salvação se pecarmos muito.', {"afirmativa":"Podemos perder a salvação se pecarmos muito.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Deus nos preserva até o fim por Seu poder."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Em Filipenses 1:6, quem aperfeiçoa a obra?', {"alternativas":["Nós mesmos","A igreja","Deus","Os líderes"],"indice_correto":2,"dica":"Fp 1:6 — Aquele que começou a boa obra a aperfeiçoará."}, 3)

l = criar_licao(t_d4, 'Esperança Futura: Nova Criação', 'Apocalipse 21:1-5; 1 Coríntios 15', 'Ap 21:1-5; 1Co 15', 'Ter esperança bíblica na consumação do Reino', 'Eis que faço novas todas as coisas.', 6, 70)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que João viu no novo céu e nova terra?', {"alternativas":["Destruição total","Deus habitando com os homens","Anjos governando","Somente espíritos"],"indice_correto":1,"dica":"Ap 21:3 — Eis o tabernáculo de Deus com os homens."}, 1)
criar_exercicio(l, 'VF', 'Na nova criação não haverá mais morte nem dor.', {"afirmativa":"Na nova criação não haverá mais morte nem dor.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"Ap 21:4 — Não haverá mais morte, nem pranto, nem dor."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Como essa esperança deve nos impactar hoje?', {"alternativas":["Fugir do mundo","Viver com propósito e esperança","Ignorar o presente","Só pensar no futuro"],"indice_correto":1,"dica":"A esperança futura nos sustenta e nos motiva a viver para Deus hoje."}, 3)

# ============================================================
# 8. CRIANÇAS AVANÇADO - C4: Parábolas de Jesus
# ============================================================
t_c4 = criar_trilha('Parábolas de Jesus', 'Ensinos de Jesus em histórias', 'crianca', 'avancado', 9, '📖')

l = criar_licao(t_c4, 'A Ovelha Perdida', 'Lucas 15:1-7', 'Lc 15:1-7', 'Saber que Jesus busca a ovelha perdida', 'Jesus veio buscar e salvar o perdido.', 1, 50)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Quantas ovelhas o pastor tinha?', {"alternativas":["50","100","200","10"],"indice_correto":1,"dica":"Lc 15:4 — Quem de vós tendo 100 ovelhas."}, 1)
criar_exercicio(l, 'VF', 'O pastor deixou as 99 para buscar a perdida.', {"afirmativa":"O pastor deixou as 99 para buscar a perdida.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"Lc 15:4 — Deixa as 99 no deserto e vai atrás da perdida."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Jesus quis ensinar?', {"alternativas":["Cuidar de animais","O amor de Deus que busca pecadores","Ser pastor é fácil","Ovelhas são teimosas"],"indice_correto":1,"dica":"Deus se alegra com um pecador que se arrepende."}, 3)

l = criar_licao(t_c4, 'O Filho Pródigo - Parte 1', 'Lucas 15:11-24', 'Lc 15:11-24', 'Ver o amor do Pai que recebe o filho arrependido', 'O filho voltou e o Pai correu para abraçá-lo.', 2, 50)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que o filho mais novo pediu?', {"alternativas":["Um cavalo","Sua herança","Bênção","Trabalho"],"indice_correto":1,"dica":"Lc 15:12 — Dá-me a parte dos bens."}, 1)
criar_exercicio(l, 'VF', 'O pai ficou com raiva quando o filho voltou.', {"afirmativa":"O pai ficou com raiva quando o filho voltou.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Lc 15:20 — Correu e lançou-se ao pescoço."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que o pai fez quando viu o filho voltando?', {"alternativas":["Fechou a porta","Correu e o abraçou","Ignorou","Mandou embora"],"indice_correto":1,"dica":"Lc 15:20 — Correu, abraçou e beijou."}, 3)

l = criar_licao(t_c4, 'O Filho Pródigo - Parte 2', 'Lucas 15:25-32', 'Lc 15:25-32', 'Ver o perigo da autojustiça', 'O filho mais velho também precisava de graça.', 3, 50)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Como o filho mais velho reagiu?', {"alternativas":["Ficou feliz","Ficou irado e não quis entrar","Abraçou o irmão","Dançou de alegria"],"indice_correto":1,"dica":"Lc 15:28 — Indignou-se e não queria entrar."}, 1)
criar_exercicio(l, 'VF', 'O filho mais velho também precisava de arrependimento.', {"afirmativa":"O filho mais velho também precisava de arrependimento.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"Ele confiava em seu próprio mérito, não na graça."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que a parábola nos ensina?', {"alternativas":["Devemos ser bonzinhos","Todos precisam da graça de Deus","Só pecadores graves precisam de Deus","Os justos não precisam de arrependimento"],"indice_correto":1,"dica":"Tanto o filho perdido quanto o que ficou precisam da graça do Pai."}, 3)

l = criar_licao(t_c4, 'A Casa na Rocha', 'Mateus 7:24-27', 'Mt 7:24-27', 'Obedecer a Palavra é construir sobre a rocha', 'O prudente constrói sobre a rocha que é Cristo.', 4, 50)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que o homem prudente construiu?', {"alternativas":["Sobre a areia","Sobre a rocha","Perto do rio","Na montanha"],"indice_correto":1,"dica":"Mt 7:24 — Edificou sobre a rocha."}, 1)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que fez a casa na rocha não cair?', {"alternativas":["Era muito bonita","Tinha bons materiais","Estava firmada na rocha","Era grande"],"indice_correto":2,"dica":"Mt 7:25 — Não caiu porque estava fundada sobre a rocha."}, 2)
criar_exercicio(l, 'VF', 'O insensato ouviu e obedeceu a Palavra.', {"afirmativa":"O insensato ouviu e obedeceu a Palavra.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Mt 7:26 — Ouviu e não praticou."}, 3)

# ============================================================
# 9. ADOLESCENTES AVANÇADO - A4: Discipulado e Chamado
# ============================================================
t_a4 = criar_trilha('Discipulado e Chamado', 'Seguir Cristo em todas as áreas', 'adolescente', 'avancado', 10, '🔥')

l = criar_licao(t_a4, 'Ser Discípulo de Cristo', 'Lucas 9:23-25', 'Lc 9:23-25', 'Entender o custo e a alegria do discipulado', 'Se alguém quer vir após mim, negue-se a si mesmo, tome a cruz e siga-me.', 1, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Jesus diz que devemos fazer para segui-lo?', {"alternativas":["Ser rico","Estudar muito","Negar a si mesmo e tomar a cruz","Ser religioso"],"indice_correto":2,"dica":"Lc 9:23 — Negue-se a si mesmo, tome a cruz."}, 1)
criar_exercicio(l, 'VF', 'Seguir Jesus é sempre confortável e fácil.', {"afirmativa":"Seguir Jesus é sempre confortável e fácil.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Lc 9:23 — Tomar a cruz envolve sacrifício."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que significa negar a si mesmo?', {"alternativas":["Deixar de existir","Recusar prazeres","Colocar Cristo acima dos próprios desejos","Ser pobre"],"indice_correto":2,"dica":"É dizer não ao ego e sim ao senhorio de Cristo."}, 3)

l = criar_licao(t_a4, 'Chamado para Toda a Vida', 'Colossenses 3:23-24; 1Co 10:31', 'Cl 3:23-24; 1Co 10:31', 'Ver que toda a vida é serviço a Deus', 'Fazei tudo para a glória de Deus.', 2, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que 1 Coríntios 10:31 nos ensina?', {"alternativas":["Só o culto importa","Fazei tudo para glória de Deus","Religião é privada","Só o trabalho na igreja conta"],"indice_correto":1,"dica":"1Co 10:31 — Fazei tudo para a glória de Deus."}, 1)
criar_exercicio(l, 'VF', 'Só pastores e missionários têm chamado de Deus.', {"afirmativa":"Só pastores e missionários têm chamado de Deus.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"Todo cristão é chamado a servir a Deus em sua vocação."}, 2)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Como estudantes podem viver para a glória de Deus?', {"alternativas":["Só estudando Bíblia","Estudando com dedicação e honestidade","Abandonando os estudos","Só frequentando a igreja"],"indice_correto":1,"dica":"Tudo que fazemos pode ser para a glória de Deus."}, 3)

l = criar_licao(t_a4, 'Igreja: Corpo de Cristo', 'Efésios 4:11-16', 'Ef 4:11-16', 'Entender a importância da comunidade de fé', 'Somos membros uns dos outros, crescendo em amor.', 3, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'Para que Cristo deu dons à igreja?', {"alternativas":["Para competir","Para edificação dos santos","Para ganhar dinheiro","Para fama pessoal"],"indice_correto":1,"dica":"Ef 4:12 — Com vistas ao aperfeiçoamento dos santos."}, 1)
criar_exercicio(l, 'ASSOCIACAO', 'Associe cada dom ao seu propósito:', {"pares":[{"esquerda":"Apostolado","direita_correta":"Fundar a igreja"},{"esquerda":"Ensino","direita_correta":"Instruir na Palavra"},{"esquerda":"Serviço","direita_correta":"Ajudar necessitados"}]}, 2)
criar_exercicio(l, 'VF', 'Podemos viver a fé cristã isoladamente.', {"afirmativa":"Podemos viver a fé cristã isoladamente.","alternativas":["Falso","Verdadeiro"],"indice_correto":0,"dica":"A igreja é o corpo de Cristo; precisamos uns dos outros."}, 3)

l = criar_licao(t_a4, 'Esperança que Sustenta', 'Apocalipse 21:1-5', 'Ap 21:1-5', 'Ter esperança bíblica em meio ao sofrimento', 'Eis que faço novas todas as coisas.', 4, 60)
criar_exercicio(l, 'MULTIPLA_ESCOLHA', 'O que Deus fará na nova criação?', {"alternativas":["Destruirá tudo","Fará novas todas as coisas","Só salvará alguns","Ignorará o pecado"],"indice_correto":1,"dica":"Ap 21:5 — Eis que faço novas todas as coisas."}, 1)
criar_exercicio(l, 'VF', 'A esperança futura nos ajuda a perseverar hoje.', {"afirmativa":"A esperança futura nos ajuda a perseverar hoje.","alternativas":["Falso","Verdadeiro"],"indice_correto":1,"dica":"Saber que Cristo vencerá nos sustenta nas lutas presentes."}, 2)
criar_exercicio(l, 'ORDENACAO', 'Ordene a história da redenção:', {"itens":["Deus cria o mundo perfeito","O pecado entra no mundo","Deus promete um Salvador","Jesus nasce e vive","Jesus morre e ressuscita","O Espírito é derramado","Cristo volta e faz novas todas as coisas"]}, 3, 3)

# ============================================================
# 10. DESAFIOS DIÁRIOS (7 dias completos)
# ============================================================
from datetime import date, timedelta
base = date.today()
semana = [
    ("Versículo do Dia", "Leia João 3:16 e reflita sobre o amor de Deus que enviou Seu Filho para salvar pecadores.", "João 3:16", "O que significa Deus ter dado Seu Filho único?"),
    ("Oração e Gratidão", "Separe 5 minutos para agradecer a Deus por três bênçãos específicas desta semana.", "1 Tessalonicenses 5:18", "Como a gratidão muda sua perspectiva?"),
    ("Perdão na Prática", "Pense em alguém que você precisa perdoar. Ore por essa pessoa hoje.", "Colossenses 3:13", "O que impede você de perdoar?"),
    ("Amor ao Próximo", "Faça uma boa ação anônima para alguém hoje.", "1 João 4:19", "Como você pode demonstrar amor de forma prática?"),
    ("Fé em Ação", "Leia Hebreus 11:1 e identifique uma área onde precisa confiar mais em Deus.", "Hebreus 11:1", "O que significa ter fé no dia a dia?"),
    ("Descanso em Deus", "Leia Salmo 23 e medite sobre o cuidado do Bom Pastor.", "Salmos 23:1-6", "O que significa para você o Senhor ser seu pastor?"),
    ("Palavra no Coração", "Escolha um versículo para memorizar esta semana.", "Salmos 119:11", "Como guardar a Palavra no coração ajuda contra o pecado?"),
]
for i, (tit, desc, ver, perg) in enumerate(semana):
    criar_desafio(base + timedelta(days=i), tit, desc, ver, perg, 30)

# ============================================================
# 11. SÉRIE OURO
# ============================================================
so_ex = lambda t, e, d, p=3: {'t': t, 'e': e, 'd': d, 'p': p}

criar_serie_ouro(t_d4, 'Desafio Ouro: Doutrinas Centrais', 'Questões avançadas sobre teologia reformada', 'adulto', 'avancado', 300, [
    so_ex('MULTIPLA_ESCOLHA', 'Qual a diferença entre graça comum e graça salvadora?', {"alternativas":["Não há diferença","Graça comum sustenta a criação; graça salvadora regenera","Graça comum é para crentes","Graça salvadora é para todos"],"indice_correto":1}),
    so_ex('VF', 'A expiação de Cristo foi limitada em seu propósito, não em seu poder.', {"afirmativa":"A expiação de Cristo foi limitada em seu propósito, não em seu poder.","alternativas":["Falso","Verdadeiro"],"indice_correto":1}),
    so_ex('MULTIPLA_ESCOLHA', 'O que significa a perseverança dos santos?', {"alternativas":["Que podemos perder a salvação","Que Deus preserva os Seus até o fim","Que todos serão salvos","Que só os fortes perseveram"],"indice_correto":1}),
    so_ex('ORDENACAO', 'Ordene os decretos de Deus na teologia reformada:', {"itens":["Eleição","Criação","Queda","Redenção","Chamado Eficaz","Justificação","Glorificação"]}),
    so_ex('ASSOCIACAO', 'Associe cada doutrina ao seu ensino:', {"pares":[{"esquerda":"Justificação","direita_correta":"Declarado justo em Cristo"},{"esquerda":"Santificação","direita_correta":"Tornado santo pelo Espírito"},{"esquerda":"Glorificação","direita_correta":"Perfeito na nova criação"}]}),
])

criar_serie_ouro(t_c3, 'Desafio Ouro: Heróis da Fé', 'Conhecimento aprofundado sobre os heróis bíblicos', 'crianca', 'intermediario', 200, [
    so_ex('MULTIPLA_ESCOLHA', 'O que a arca de Noé simboliza?', {"alternativas":["Apenas um barco","Cristo como lugar de salvação","A habilidade de Noé","Uma história infantil"],"indice_correto":1}),
    so_ex('VF', 'Abraão foi justificado por suas obras.', {"afirmativa":"Abraão foi justificado por suas obras.","alternativas":["Falso","Verdadeiro"],"indice_correto":0}),
    so_ex('ORDENACAO', 'Ordene a história de José:', {"itens":["José é vendido","José no Egito","José na prisão","José interpreta sonhos","José governa o Egito","José perdoa seus irmãos"]}),
])

criar_serie_ouro(t_a3, 'Desafio Ouro: Vivendo a Fé', 'Aplicação avançada da fé no cotidiano adolescente', 'adolescente', 'intermediario', 200, [
    so_ex('MULTIPLA_ESCOLHA', 'Como responder quando sua fé é desafiada na escola?', {"alternativas":["Discutir com todos","Com mansidão e razão, prontos a responder","Esconder a fé","Sair da escola"],"indice_correto":1}),
    so_ex('VF', 'A graça de Deus nos dá liberdade para viver como quisermos.', {"afirmativa":"A graça de Deus nos dá liberdade para viver como quisermos.","alternativas":["Falso","Verdadeiro"],"indice_correto":0}),
    so_ex('MULTIPLA_ESCOLHA', 'Qual versículo melhor resume a identidade do crente?', {"alternativas":["Vós sois o sal da terra","Deus é amor","Não julgueis","Tudo posso naquele que me fortalece"],"indice_correto":0}),
])

# ============================================================
# 12. RECOMPENSAS EXTRAS
# ============================================================
criar_recompensa('medalha', 'Herói da Fé', 'Complete a trilha Heróis da Fé', '🛡️', 300, licoes=4)
criar_recompensa('medalha', 'Doutrinador', 'Complete a trilha Doutrinas Centrais', '📚', 500, licoes=6)
criar_recompensa('medalha', 'Discípulo', 'Complete a trilha Discipulado e Chamado', '🔥', 300, licoes=4)
criar_recompensa('versiculo', 'João 3:16', 'O amor de Deus em um versículo', '📜', 50, xp_min=200)
criar_recompensa('medalha', 'Colecionador de Estreak', 'Complete 30 dias de streak', '⭐', 1000, streak=30)
criar_recompensa('xp_bonus', 'Bônus de 10 Lições', 'Complete 10 lições', '🎯', 400, licoes=10)

print("Seed concluído com sucesso!")
print(f"  Trilhas: {Trilha.objects.count()}")
print(f"  Lições: {LicaoBiblica.objects.count()}")
print(f"  Exercícios: {Exercicio.objects.count()}")
print(f"  Desafios Diários: {DesafioDiario.objects.count()}")
print(f"  Recompensas: {Recompensa.objects.count()}")
print(f"  Série Ouro: {SerieOuroDesafio.objects.count()}")
