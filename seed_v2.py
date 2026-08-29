"""Seed v2 - Plataforma Biblica (~365 licoes + Serie Ouro)"""
import os, django, sys
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()

from courses.models import Trilha, LicaoBiblica, Exercicio
from gamification.models import Recompensa, DesafioDiario, SerieOuroDesafio, SerieOuroExercicio

def mk_trilha(nome, desc, faixa, nivel, ordem, icone):
    t, _ = Trilha.objects.get_or_create(nome=nome, defaults=dict(descricao=desc, faixa_etaria=faixa, nivel=nivel, ordem=ordem, icone=icone))
    return t

def mk_licao(trilha, titulo, texto, ref, obj, resumo, ordem, xp=50):
    l, _ = LicaoBiblica.objects.get_or_create(trilha=trilha, titulo=titulo, defaults=dict(descricao=obj, texto_base=texto, referencia=ref, objetivo=obj, resumo=resumo, ordem=ordem, xp_recompensa=xp))
    return l

def mk_ex(licao, tipo, enun, dados, ordem=1, peso=1):
    Exercicio.objects.get_or_create(licao=licao, enunciado=enun[:200], defaults=dict(tipo=tipo, dados=dados, ordem=ordem, peso_dificuldade=peso))

def add_licoes(trilha, data, xp=50):
    """data = list of (titulo, texto, ref, obj, resumo, [exercicios])"""
    for i, item in enumerate(data, 1):
        t, txt, ref, obj, res, exs = item
        l = mk_licao(trilha, t, txt, ref, obj, res, i, xp)
        for j, e in enumerate(exs, 1):
            mk_ex(l, e[0], e[1], e[2], j, e[3] if len(e)>3 else 1)

def mc(enun, alts, cor, dica='', peso=1):
    return ('MULTIPLA_ESCOLHA', enun, dict(alternativas=alts, indice_correto=cor, dica=dica), peso)

def vf(enun, af, res, dica='', peso=1):
    return ('VF', enun, dict(afirmativa=af, alternativas=['Falso','Verdadeiro'], indice_correto=res, dica=dica), peso)

print("Seed v2 - Iniciando...")

# ═══════════════════════════════════════════════
# TRILHA 1 - Criacao e Patriarcas (Gn 1-50)
# ═══════════════════════════════════════════════
t1 = mk_trilha('Criacao e Patriarcas', 'Genesis: de Adao a Jose - as origens da humanidade e do povo de Israel', 'adulto', 'iniciante', 1, 'open_in_new')
add_licoes(t1, [
    ('A Obra da Criação', 'No início Deus criou os céus e a terra. Em seis dias criou tudo: luz, firmamento, mares, vegetação, luminares, animais e o ser humano à Sua imagem. No sétimo dia descansou.', 'Genesis 1:1-2:3', 'Compreender a ordem e propósito da criação divina', 'Deus criou o universo em seis dias por Sua palavra, culminando com a humanidade. O sétimo dia estabelece o padrão de descanso.', [
        mc('Quem criou os ceus e a terra?', ['Adao','Noe','Deus','Abraao'], 2, 'Genesis 1:1'),
        mc('Em quantos dias Deus criou tudo?', ['5','6','7','3'], 1, 'Genesis 1:31 - no sexto dia completou'),
        vf('Deus criou o homem a Sua imagem.', 'Deus criou o homem a Sua imagem.', 1, 'Genesis 1:27'),
    ]),
    ('A Queda e Suas Consequências', 'Deus colocou Adão e Eva no Éden com liberdade para comer de todas as árvores, exceto a árvore do conhecimento do bem e do mal. A serpente enganou Eva, que comeu e deu a Adão.', 'Genesis 3:1-24', 'Entender o pecado original e suas consequências', 'A desobediência trouxe a morte espiritual, a separação de Deus e a expulsão do Éden. Deus prometeu uma semente que esmagaria a cabeça da serpente.', [
        mc('Qual arvore Deus proibiu?', ['Da vida','Do conhecimento do bem e do mal','Da ciencia','Da sabedoria'], 1, 'Genesis 2:17'),
        vf('Eva comeu primeiro da fruta proibida.', 'Eva comeu primeiro da fruta proibida.', 1, 'Genesis 3:6'),
        mc('Qual foi a consequencia da desobediencia?', ['Riqueza','Expulsao do Eden','Morte imediata','Multiplicacao'], 1, 'Genesis 3:23-24'),
    ]),
    ('Caim e Abel', 'Abel ofereceu ao Senhor as primícias do seu rebanho, mas Caim dos frutos da terra. O Senhor aceitou Abel, mas não a Caim. Caim, dominado pela inveja, matou seu irmão.', 'Genesis 4:1-16', 'Compreender a primícia do sacrifício e o perigo do pecado', 'O primeiro assassinato da Bíblia demonstra como o pecado se perpetua. Deus marcou Caim, mostrando misericórdia mesmo na desobediência.', [
        mc('Quem ofereceu sacrificio aceito por Deus?', ['Caim','Abel','Noe','Adao'], 1, 'Genesis 4:4'),
        vf('Caim matou seu irmao Abel por inveja.', 'Caim matou seu irmao Abel por inveja.', 1, 'Genesis 4:8'),
        mc('O que Deus fez com Caim?', ['Matou-o','Marcou-o','Perdoou-o sem nada','Expulsou-o da terra'], 1, 'Genesis 4:15 - marcou para protege-lo'),
    ]),
    ('A Arca de Noé', 'Deus viu a maldade humana e decidiu destruir a terra com dilúvio, mas achou graça em Noé. Noé construiu a arca conforme as instruções, levando sua família e pares de animais.', 'Genesis 6:1-9:17', 'Reconhecer o juízo divino e a fidelidade de Deus', 'Noé obedeceu em tudo. Depois do dilúvio, Deus fez aliança com um arco-íris como sinal.', [
        mc('Por quantos dias choveu?', ['20','30','40','50'], 2, 'Genesis 7:12'),
        vf('Noe levou apenas animais limpos na arca.', 'Noe levou apenas animais limpos na arca.', 0, 'Levou pares de todos, limpos e nao limpos'),
        mc('Qual sinal Deus deu pos-diluvio?', ['Estrela','Arco-iris','Lua cheia','Nuvem'], 1, 'Genesis 9:13'),
    ]),
    ('A Chamada de Abraão', 'Deus disse a Abraão: "Vai-te da tua terra e vai para a terra que eu te mostrarei." Prometeu fazer dele grande nação e que nele seriam abençoadas todas as famílias da terra.', 'Genesis 12:1-9', 'Entender a aliança de Deus com Abraão', 'A chamada de Abraão inicia a história da redenção. Sua obediência, apesar da incerteza, é modelo de fé.', [
        mc('De que terra Abrao saiu?', ['Mesopotamia','Canaa','Egito','Edom'], 0, 'Genesis 12:1 - de Ur dos caldeus'),
        vf('Abraao creu em Deus e lhe foi imputado justica.', 'Abraao creu em Deus e lhe foi imputado justica.', 1, 'Genesis 15:6'),
        mc('Quantos filhos teve Abraao com Sara?', ['1 - Isaac','2 - Ismael e Isaac','3 - Zorobael e outros','Nenhum'], 0, 'Genesis 21:2'),
    ]),
    ('A Prova de Isaque', 'Deus ordenou a Abraão que oferecesse Isaac em sacrifício no monte Moriá. No momento final um anjo deteve sua mão e um cordeiro foi oferecido em substituição.', 'Genesis 22:1-19', 'Reconhecer o exemplo de obediência e fé de Abraão', 'A prova do Moriá e tipologia do sacrifício de Cristo. Deus proveu o cordeiro como substituto.', [
        mc('Onde Deus pediu o sacrificio?', ['Monte Sinai','Monte Moria','Monte das Oliveiras','Monte Nebo'], 1, 'Genesis 22:2 - montanha de Moria'),
        vf('Deus permitiu que Isaque fosse morto.', 'Deus permitiu que Isaque fosse morto.', 0, 'Genesis 22:12 - um anjo o deteve'),
        mc('O que foi oferecido em vez de Isaque?', ['Touro','Cordeiro','Carneiro preso num carrapicho','Pomba'], 2, 'Genesis 22:13'),
    ]),
    ('Jacó e Esaú', 'Isaac teve gêmeos: Esaú, o primogênito, e Jacó. Esaú vendeu o direito de primogenitura por um prato de lentilhas. Depois Jacó recebeu a bênção do primogênito.', 'Genesis 25:19-34; 27:1-40', 'Compreender as consequências do engano e busca por vantagem', 'A rivalidade entre Jacó e Esaú demonstra as consequências da preferência humana e do engano.', [
        mc('O que Esaú vendeu por lentilhas?', ['A vida','O direito de primogenito','A esposa','A terra'], 1, 'Genesis 25:33'),
        vf('Jacó era o primogenito.', 'Jacó era o primogenito.', 0, 'Era o segundo gemeo'),
        mc('Quem ajudou Jacó a receber a bencao?', ['Isaac','Deus','Rebeca','Lia'], 2, 'Genesis 27:5-17'),
    ]),
    ('O Escaldo de Jacó em Peniel', 'Jacó lutou toda a noite com um anjo no vale do Jaboque e foi vitorioso, embora tivesse o quadril deslocado. Recebeu o nome de Israel.', 'Genesis 32:22-32', 'Entender a transformação de Jacó', 'Jacó partiu como enganador e voltou como Israel, aquele que foi tocado por Deus e mudado.', [
        mc('Que nome Jacó recebeu apos lutar com Deus?', ['Abraao','Israel','Isaque','Jacó mesmo'], 1, 'Genesis 32:28'),
        vf('Jacó ganhou a luta sem nenhum ferimento.', 'Jacó ganhou a luta sem nenhum ferimento.', 0, 'Teve o quadril deslocado'),
        mc('Onde a luta aconteceu?', ['Monte Sinai','Vau do Jaboque','Rio Jordao','Deserto'], 1, 'Genesis 32:22'),
    ]),
    ('José e os Sonhos', 'José, filho favorito de Jacó, recebeu sonhos de grandeza que provocaram inveja dos irmãos. Eles o venderam como escravo. No Egito, José foi preso mas interpretou sonhos do faraó.', 'Genesis 37:1-41:41', 'Compreender o propósito de Deus nas adversidades', 'A história de José demonstra como Deus transforma o mal em bem para salvar muitas vidas.', [
        mc('O que os irmaos fizeram com Jose?', ['Abraçaram-no','Venderam-no','Mataram-no','Perdoaram-no'], 1, 'Genesis 37:28'),
        vf('Jose interpretou sonhos do farao no Egito.', 'Jose interpretou sonhos do farao no Egito.', 1, 'Genesis 41'),
        mc('O que Jose disse aos irmaos?', ['Vingarei-me','Deus o encaminhou para bem','Odeio-los','Nao me lembro'], 1, 'Genesis 50:20'),
    ]),
    ('José Perdoa seus Irmãos', 'José revelou sua identidade: "Vós pensastes mal contra mim, mas Deus o encaminhou para o bem." José chorou e abraçou seus irmãos.', 'Genesis 42:1-45:15', 'Reconhecer o poder do perdão e a soberania de Deus', 'O perdão de José é um dos mais belos exemplos na Bíblia. Ele reconheceu a mão de Deus em tudo.', [
        mc('Como Jose reagiu ao ver os irmaos?', ['Rejeitou-os','Perdoou-os','Expulsou-os','Cobrou-lhes'], 1, 'Genesis 45:14-15'),
        vf('Jose nunca chorou quando reencontrou os irmaos.', 'Jose nunca chorou quando reencontrou os irmaos.', 0, 'Chorou muito'),
        mc('Quantos irmãos de Jose vieram ao Egito?', ['10','11','12','7'], 0, 'Genesis 42:3 - sem Benjamim e Jose'),
    ]),
    ('A Descida ao Egito', 'Jacó e toda a sua família desceram ao Egito, reunindo-se a José. Foram 70 pessoas. Israel estabeleceu-se na terra de Gosen.', 'Genesis 46:1-47:12', 'Entender como a descendência de Abraão se multiplicou', 'A descida ao Egito cumpriu a profecia de que sua descendência seria estrangeira por 400 anos.', [
        mc('Quantas pessoas desceram ao Egito?', ['50','70','100','200'], 1, 'Genesis 46:27'),
        vf('Jacó morreu no Egito.', 'Jacó morreu no Egito.', 1, 'Genesis 49:33'),
        mc('Onde Israel se estabeleceu no Egito?', ['Memfis','Gosen','Tebas','Delta'], 1, 'Genesis 47:10-11'),
    ]),
    ('José interpreta sonhos do faraó', 'O faraó sonhou com sete vacas gordas devoradas por sete magras, e sete espigas cheias devoradas por sete magras. José interpretou: sete anos de abundância seguidos de sete anos de fome.', 'Genesis 41:1-36', 'Entender como Deus usa sonhos para revelar seus planos', 'José revelou que apenas a sapiência divina pode interpretar sonhos e preparar o povo para o futuro.', [
        mc('O que as sete vacas magras representavam?', ['Anos de guerra','Anos de fome','Anos de paz','Anos de praga'], 1, 'Genesis 41:27'),
        vf('Jose pediu ao farao que o libertasse antes de interpretar.', 'Jose pediu ao farao que o libertasse antes de interpretar.', 0, 'Interpretou primeiro, depois foi libertado'),
        mc('Que cargo Jose recebeu no Egito?', ['Sacerdote','Governador','General','Escriba'], 1, 'Genesis 41:41-43'),
    ]),
], 50)
print("  Trilha 1 completa - 12 licoes")

# ═══════════════════════════════════════════════
# TRILHA 2 - Exodo e a Lei (Ex-Lev)
# ═══════════════════════════════════════════════
t2 = mk_trilha('Exodo e a Lei', 'A libertacao do Egito e a aliança no Sinai: Moises, as pragas, o tabernaculo e a santidade de Deus', 'adulto', 'iniciante', 2, 'exit_to_app')
add_licoes(t2, [
    ('O Nascimento de Moisés', 'Moisés nasceu em tempos em que o faraó matava bebês hebreus. Sua mãe o colocou num cesto no Nilo. A filha do faraó o encontrou e criou-o no palácio.', 'Exodo 2:1-10', 'Entender como Deus prepara seus libertadores', 'Deus protegeu Moisés desde o nascimento, preparando-o para liderar Israel. O Nilo, fonte de morte, tornou-se caminho de vida.', [
        mc('Quem encontrou Moises no rio?', ['Uma pastora','A filha do farao','Uma escrava','A mae de Moises'], 1, 'Exodo 2:5'),
        vf('Moises foi criado no palacio do farao.', 'Moises foi criado no palacio do farao.', 1, 'Exodo 2:10'),
        mc('O que Moises fez ao matar um egipcio?', ['Foi preso','Fugiu para Madian','Morreu','Pediu perdao'], 1, 'Exodo 2:15'),
    ]),
    ('As Dez Pragas do Egito', 'Deus enviou dez pragas sobre o Egito para libertar Israel: água em sangue, rãs, mosquitos, moscas, peste, furúnculos, granizo, gafanhotos, trevas e morte dos primogênitos.', 'Exodo 7:1-12:32', 'Reconhecer o poder de Deus sobre os deuses do Egito', 'Cada praga atingiu um deus egípcio, demonstrando a supremacia do Deus de Israel.', [
        mc('Quantas pragas Deus enviou ao Egito?', ['7','8','10','12'], 2, 'Exodo 7-12'),
        mc('Qual foi a ultima praga?', ['Trevas','Granizo','Morte dos primogenitos','Gafanhotos'], 2, 'Exodo 12:29'),
        vf('As pragas afetaram apenas os egipcios.', 'As pragas afetaram apenas os egipcios.', 1, 'Deus poupou os israelitas em Gosen das pragas - Exodo 8:22-23'),
    ]),
    ('A Passagem do Mar Vermelho', 'Israel cruzou o Mar Vermelho em seco, com as águas erguidas como muralhas. Os egípcios que os perseguiram foram engolidos pelas águas. Moisés e Miriam cantam de louvor.', 'Exodo 14:1-15:21', 'Entender a salvação de Deus e o louvor que se segue', 'O Mar Vermelho é o maior ato de salvação do AT, tipo do batismo e da libertação do pecado.', [
        mc('Como Israel cruzou o mar?', ['Nadando','Em barcos','Em seco','Por ponte'], 2, 'Exodo 14:22'),
        vf('Todos os egipcios morreram no mar.', 'Todos os egipcios morreram no mar.', 1, 'Exodo 14:28'),
        mc('Quem liderou o canto de louvor pos-milagre?', ['Aaron','Moises','Miriam','Josue'], 2, 'Exodo 15:20-21'),
    ]),
    ('Os Dez Mandamentos', 'No monte Sinai, Deus deu a Lei a Moisés: não ter outros deuses, não fazer imagens, não usar o nome em vão, lembrar o sábado, honrar pais, não matar, não adulterar, não furtar, não mentir, não cobiçar.', 'Exodo 20:1-17', 'Conhecer os mandamentos como base da aliança', 'Os Dez Mandamentos são o núcleo da Lei, revelando a vontade de Deus para a vida humana.', [
        mc('Qual e o primeiro mandamento?', ['Nao matar','Nao ter outros deuses','Honrar pais','Nao furtar'], 1, 'Exodo 20:3'),
        vf('O sabado e o quarto mandamento.', 'O sabado e o quarto mandamento.', 1, 'Exodo 20:8-11'),
        mc('Quantos mandamentos Deus deu?', ['5','7','10','12'], 2, 'Exodo 20:1-17'),
    ]),
    ('O Bezerro de Ouro', 'Enquanto Moisés estava no Sinai, o povo fez um bezerro de ouro para adorar. Moisés, ao descer, quebrou as tábuas da Lei e julgou os idólatras. Depois subiu de novo e recebeu novas tábuas.', 'Exodo 32:1-35', 'Reconhecer o perigo da idolatria e a paciência de Deus', 'O bezerro demonstra a tendência humana de buscar substitutos tangíveis para o Deus invisível.', [
        mc('O que o povo fez enquanto Moises estava ausente?', ['Oraram','Fizeram bezerro de ouro','Dormiram',' fugiram'], 1, 'Exodo 32:1-4'),
        vf('Moises quebrou as tábuas da Lei ao ver o bezerro.', 'Moises quebrou as tábuas da Lei ao ver o bezerro.', 1, 'Exodo 32:19'),
        mc('Quantos morreram naquele dia?', ['3 mil','5 mil','10 mil','Nenhum'], 0, 'Exodo 32:28 - cerca de 3 mil'),
    ]),
    ('O Tabernáculo', 'Deus instruiu Moisés a construir o tabernáculo, lugar onde Sua presença habitaria entre o povo. Tinha o pátio, o santuário e o Santo dos Santos, onde ficava a Arca da Aliança.', 'Exodo 25-27; 40', 'Entender a importância da presença de Deus no meio do povo', 'O tabernáculo revela o desejo de Deus de habitar com Sua criatura e antecipa o templo e a encarnação.', [
        mc('Onde ficava a Arca da Aliança?', ['No patio','No santuario','No Santo dos Santos','Na entrada'], 2, 'Exodo 26:33'),
        vf('O tabernaculo era permanente e fixo.', 'O tabernaculo era permanente e fixo.', 0, 'Era transportavel'),
        mc('Quem construiu o tabernaculo?', ['Moises','Aron','Bezalel e Ooliabe','O povo todo'], 2, 'Exodo 31:1-6'),
    ]),
    ('O Sangue da Aliança', 'Moisés aspergiu o povo com sangue de animais, dizendo: "Este é o sangue da aliança." O sangue era sinal de compromisso entre Deus e Israel.', 'Exodo 24:1-8', 'Entender o significado do sangue na aliança', 'O sangue da aliança é tipo do sangue de Cristo que estabelece a nova aliança.', [
        mc('O que Moises aspergiu sobre o povo?', ['Agua','Oleo','Sangue','Incenso'], 2, 'Exodo 24:8'),
        vf('A alianca era apenas de Israel.', 'A alianca era apenas de Israel.', 0, 'Era bidirecional: Deus e Israel'),
        mc('O que o sangue representava?', ['Vida','Pecado','Morte','Poder'], 0, 'Vida esta no sangue - Levitico 17:11'),
    ]),
    ('Levítico: Santidade de Deus', 'Levítico revela a santidade de Deus e as instruções para sacrifícios, pureza e festivais. "Sede santos, porque eu sou santo."', 'Levitico 11:44-45; 19:2', 'Compreender o chamado a santidade', 'Levítico ensina que a aproximação a Deus exige pureza e obediência, apontando para a santidade necessária na nova aliança.', [
        mc('Quantas vezes Deus diz "sede santos" em Levitico?', ['1 vez','3 vezes','7 vezes','Nenhuma'], 1, 'Levitico 11:44, 19:2, 20:7'),
        vf('Levitico fala apenas de sacrificios.', 'Levitico fala apenas de sacrificios.', 0, 'Tambem fala de pureza, festivais e santidade'),
        mc('Qual e o principal sacrificio expiatório?', ['Holocausto','Pecado','Comunhao','Obrigacao'], 1, 'Levitico 4-5'),
    ]),
    ('O Dia da Expiação', 'Uma vez por ano, o sumo sacerdote entrava no Santo dos Santos com sangue de um bode, para expiar os pecados de Israel. Dois bodes: um morto, outro vivo (scapegoat).', 'Levitico 16', 'Entender o simbolismo do Dia da Expiação', 'O Dia da Expiação antecipa a obra expiatória de Cristo, o nosso sumo sacerdote que entrou no céu.', [
        mc('Quem entrava no Santo dos Santos?', ['Qualquer sacerdote','O sumo sacerdote','O rei','Qualquer israelita'], 1, 'Levitico 16:2-3'),
        vf('O Dia da Expiação era celebrado todo mes.', 'O Dia da Expiação era celebrado todo mes.', 0, 'Era uma vez por ano'),
        mc('O que representava o bode vivo?', ['O pecado','A libertacao do pecado','A morte','A vida eterna'], 1, 'Levitico 16:20-22 - scapegoat'),
    ]),
], 50)
print("  Trilha 2 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 3 - Davi: O Rei segundo o Coracao de Deus
# ═══════════════════════════════════════════════
t3 = mk_trilha('Davi: O Rei segundo o Coracao de Deus', 'De pastor a rei: a uncao, Golia, o pecado, o arrependimento e os salmos de Davi', 'adulto', 'iniciante', 3, 'crown')
add_licoes(t3, [
    ('A Unção de Davi', 'Samuel ungiu Davi, o menor dos filhos de Jessé, como futuro rei de Israel. Enquanto Saul era rei, Deus já havia escolhido um homem segundo o Seu coração.', '1 Samuel 16:1-13', 'Entender que Deus olha o coração, não a aparência', 'Deus rejeitou os irmãos mais velhos de Davi e escolheu o menor, revelando que Sua escolha não depende de aparência.', [
        mc('Quem ungiu Davi?', ['Saul','Samuel','Aron','Natan'], 1, '1 Samuel 16:13'),
        vf('Davi era o filho mais velho de Jesse.', 'Davi era o filho mais velho de Jesse.', 0, 'Era o menor'),
        mc('Por que Deus escolheu Davi?', ['Por ser forte','Por ser bonito','Por ter bom coracao','Por ser rico'], 2, '1 Samuel 16:7'),
    ]),
    ('Davi e Golias', 'O filisteu Golias, um gigante de quase 3 metros, desafiou Israel por 40 dias. Davi, um pastor jovem, aceitou o desafio com uma funda e cinco pedras, derrubando o gigante.', '1 Samuel 17:1-54', 'Entender que a fé vence o impossível', 'Davi venceu não pelo armamento, mas pela confiança em Deus. A funda e pedras simbolizam a simplicidade da fé.', [
        mc('Quem derrotou Golia?', ['Saul','Samuel','Davi','Jonatas'], 2, '1 Samuel 17:49-50'),
        vf('Davi usou uma espada para matar Golia.', 'Davi usou uma espada para matar Golia.', 0, 'Usou funda e pedras'),
        mc('Quantas pedras Davi levou?', ['3','4','5','6'], 2, '1 Samuel 17:40'),
    ]),
    ('A Amizade de Davi e Jônatas', 'Jônatas, filho do rei Saul, amou Davi como a si mesmo e fez aliança com ele. Quando Saul quis matar Davi, Jônatas o alertou e o protegeu.', '1 Samuel 18:1-4; 20:1-42', 'Reconhecer o valor da amizade fiel', 'A amizade Davi-Jônatas é um dos mais belos exemplos de lealdade na Bíblia, prefigurando o amor fraternal.', [
        mc('Quem era Jonatas?', ['Irmao de Davi','Filho do rei Saul','Sacerdote','Profeta'], 1, '1 Samuel 18:1'),
        vf('Saul aprovou a amizade entre Davi e Jonatas.', 'Saul aprovou a amizade entre Davi e Jonatas.', 0, 'Saul ficou com inveja e queria matar Davi'),
        mc('O que Jonatas fez por Davi?', ['Deu-lhe roupas','Deu-lhe armas','Alertou-o sobre Saul','Todos anteriores'], 3, '1 Samuel 18:4; 20:1-42'),
    ]),
    ('O Pecado de Davi e Bate-Seba', 'Davi viu Bate-Seba tomando banho, chamou-a e cometeu adultério. Para encobrir, mandou matar Urias, o marido. O profeta Natã o confrontou.', '2 Samuel 11:1-27', 'Reconhecer que mesmo os mais fiéis podem cair', 'O pecado de Davi demonstra que ninguém está acima da tentação. A consequência foi severa, mas a misericórdia de Deus prevaleceu.', [
        mc('Com quem Davi cometeu adultério?', ['Mical','Abigail','Bate-Seba','Rute'], 2, '2 Samuel 11:2-4'),
        vf('Davi arrependeu-se imediatamente.', 'Davi arrependeu-se imediatamente.', 0, 'Tentou esconder o pecado primeiro'),
        mc('Quem confrontou Davi?', ['Samuel','Jonatas','Natan','Gad'], 2, '2 Samuel 12'),
    ]),
    ('O Salmo 51: Arrependimento', 'Davi orou: "Tem misericórdia de mim, ó Deus, segundo a Tua benignidade... Cria em mim, ó Deus, um coração puro." Este salmo é o maior texto de arrependimento da Bíblia.', 'Salmo 51:1-19', 'Aprender a orar de arrependimento', 'O Salmo 51 é o modelo bíblico de confissão, arrependimento e busca por restauração com Deus.', [
        mc('O que Davi pediu a Deus?', ['Riqueza','Um coracao puro','Vinganca','Poder'], 1, 'Salmo 51:10'),
        vf('Davi minimizou seu pecado.', 'Davi minimizou seu pecado.', 0, 'Reconheceu que o pecado era contra Deus'),
        mc('Contra quem Davi disse que pecou principalmente?', ['Contra Bate-Seba','Contra Urias','Contra Natan','Contra Deus'], 3, 'Salmo 51:4 - contra Ti somente pequei'),
    ]),
    ('Salmo 23: O Pastor', '"O Senhor é meu pastor, nada me faltará." Davi, que era pastor antes de ser rei, usou a imagem do pastor para descrever o cuidado de Deus.', 'Salmo 23', 'Entender o cuidado pessoal de Deus', 'Salmo 23 e o mais conhecido salmo, revelando que Deus guia, provê, protege e restaura Seu povo.', [
        mc('O que Deus faz com Seu rebanho?', ['Gui','Prove','Protege','Todos anteriores'], 3, 'Salmo 23'),
        vf('Salmo 23 foi escrito por Salomao.', 'Salmo 23 foi escrito por Salomao.', 0, 'Foi escrito por Davi'),
        mc('Mesmo na vala da morte, Davi diz:', ['Tenho medo','Nada temo','Vou fugir','Morro'], 1, 'Salmo 23:4 - nao temerei mal algum'),
    ]),
    ('Salmo 119: Amor à Palavra', 'O maior salmo (176 versículos) e um acróstico sobre o amor à Lei de Deus. Cada versículo começa com uma letra do alfabeto hebraico.', 'Salmo 119:1-176', 'Cultivar o amor pela Palavra de Deus', 'Salmo 119 demonstra que a Palavra de Deus é luz, vida, alegria e esperança para o caminho.', [
        mc('Salmo 119 e famoso por ser:', ['O mais curto','O mais longo','O mais antigo','O mais triste'], 1, '176 versiculos'),
        vf('Cada versiculo de Salmo 119 comeca com a mesma letra.', 'Cada versiculo comeca com a mesma letra.', 0, 'E um acrostico - cada verso comeca com letra diferente do alfabeto'),
        mc('O que a Palavra de Deus e para Davi?', ['Cadeia','Fardo','Luz e vida','Nada'], 2, 'Salmo 119:105 - lanterna para os pes'),
    ]),
    ('Salmo 22: Profecia da Cruz', '"Meu Deus, meu Deus, por que me abandonaste?" Davi profetizou o sofrimento do Messias, palavras que Jesus citou na cruz.', 'Salmo 22:1-31', 'Reconhecer as profecias messiânicas nos salmos', 'Salmo 22 descreve com precisão a crucificação de Jesus, escrito milênios antes do evento.', [
        mc('O que Jesus disse na cruz citando este salmo?', ['Perdoa-os','Em Tuas maos entrego Meu espirito','Meu Deus, por que me abandonaste','Esta consumado'], 2, 'Mateus 27:46'),
        vf('Salmo 22 foi escrito depois da crucificacao.', 'Salmo 22 foi escrito depois da crucificacao.', 0, 'Foi escrito por Davi seculos antes'),
        mc('Que partes do corpo sao mencionadas como feridas?', ['Pes e maos','Ossos e coracao','Cabeca e costas','Todos anteriores'], 3, 'Salmo 22 - maos e pes furados, ossos contados'),
    ]),
    ('Salmo 139: Omnipresença de Deus', '"Para onde fugirei do Teu espírito? Para onde irei da Tua presença?" Davi reconhece que Deus o conhece completamente e está em todo lugar.', 'Salmo 139:1-24', 'Entender que Deus nos conhece e nos acompanha', 'Deus sabe tudo sobre nós, antes mesmo de nascermos, e nunca nos deixa sozinhos.', [
        mc('Deus pode estar em algum lugar sem ser visto?', ['Sim','Nao','As vezes','Nunca'], 0, 'Para onde fugirei? - em todo lugar'),
        vf('Deus nos conheceu quando ja eramos adultos.', 'Deus nos conheceu quando ja eramos adultos.', 0, 'Antes de nascermos - Salmo 139:13-16'),
        mc('O que Davi reconhece no Salmo 139?', ['Que Deus o conhece e o sustenta em todo lugar','Que Deus esta longe e distante','Que Deus se esquece dele','Que Deus nao se importa'], 0, 'Salmo 139:1-10 - a Tua mao direita me sustenta'),
    ]),
], 50)
print("  Trilha 3 completa - 9 licoes")

# ═══════════════════════════════════════════════
# TRILHA 4 - Salmos: Oracao e Adoracao
# ═══════════════════════════════════════════════
t4 = mk_trilha('Salmos: Oracao e Adoracao', 'O livro dos Salmos: oracao, adoracao, lamento e esperanca no Deus que cuida do Seu povo', 'adulto', 'iniciante', 4, 'music_note')
add_licoes(t4, [
    ('Salmo 91 - Proteção Divina', 'Aquele que habita no esconderijo do Altíssimo, descansará à sombra do Todo-Poderoso. Direi do Senhor: Ele é o meu refúgio e a minha fortaleza, o meu Deus, em quem confio.', 'Salmo 91:1-16', 'Confiar na proteção absoluta de Deus', 'Salmo 91 e a declaração bíblica de proteção divina. Quem se refugia em Deus está guardado de pragas, armas e perigos.', [
        mc('Quem habita no esconderijo do Altissimo?', ['O pecador','O que confia em Deus','O rei','O sacerdote'], 1, 'Salmo 91:1'),
        vf('Salmo 91 promete que nada mau acontecera ao justo.', 'Salmo 91 promete que nada mau acontecera ao justo.', 0, 'Deus protege, mas nao livra de toda dificuldade'),
        mc('O que Salmo 91:11 diz sobre os anjos?', ['Deus dara ordem aos Seus anjos para guardarem o justo','Cada justo recebera exatamente dois anjos','Nao ha anjos guardando ninguem','Os anjos guardam apenas os sacerdotes'], 0, 'Salmo 91:11 - aos Seus anjos dara ordem a teu respeito'),
    ]),
    ('Salmo 46 - Refúgio Inabalável', 'Deus é o nosso refúgio e fortaleza, socorro sempre presente nas angústias. Por isso não temerei, ainda que a terra se mude e os montes se abalem no mar.', 'Salmo 46:1-11', 'Encontrar paz no meio do caos', 'Salmo 46 ensina que, mesmo quando o mundo desmorona, Deus é nossa rocha imóvel. Basta parar e reconhecer que Ele é Deus.', [
        mc('O que e Deus para quem O busca?', ['Um projeto','Refugio e fortaleza','Um castigo','Uma ideia'], 1, 'Salmo 46:1'),
        vf('O salmo diz para fugir quando ha perigo.', 'O salmo diz para fugir quando ha perigo.', 0, 'Diz: "Ainda que a terra se mude, nao temerei"'),
        mc('O que Deus diz as nacoes?', ['Aventurem-se','Acalmem-se e saibam que Eu sou Deus', 'Vinguem-se', 'Desistam'], 1, 'Salmo 46:10'),
    ]),
    ('Salmo 103 - Bondade de Deus', 'Bendize, ó minha alma, ao Senhor, e não esqueças de nenhum dos seus benefícios. Ele perdoa todas as tuas enfermidades e coroa de benignidade.', 'Salmo 103:1-22', 'Cultivar a gratidão por tudo que Deus faz', 'Salmo 103 enumera os benefícios de Deus: perdão, cura, resgate, amor, misericórdia e satisfação. É um hino de gratidão.', [
        mc('O que o salmista pede a sua alma?', ['Chorar','Esquecer','Bendizer ao Senhor','Dormir'], 2, 'Salmo 103:1'),
        vf('Deus sara todas as tuas enfermidades.', 'Deus sara todas as tuas enfermidades.', 1, 'Salmo 103:3 - perdoa as iniquidades e sara as enfermidades'),
        mc('Quantos beneficios Deus da?', ['Muitos','Sete','Doze','Apenas perdao'], 0, 'Nao esquecas de nenhum dos seus beneficios'),
    ]),
    ('Salmo 27 - O Senhor é a Minha Luz', 'O Senhor é a minha luz e a minha salvação; a quem temerei? O Senhor é a fortaleza da minha vida; de quem me assustarei?', 'Salmo 27:1-14', 'Buscar a presença de Deus acima de tudo', 'Davi declara que, mesmo cercado de inimigos, sua única busca é habitar na casa do Senhor e contemplar a Sua beleza.', [
        mc('O que e o Senhor para Davi?', ['Luz e salvacao','Forte e implacavel','Um juiz severo','Um espectador'], 0, 'Salmo 27:1'),
        vf('Davi preferia estar na guerra do que na casa de Deus.', 'Davi preferia estar na guerra do que na casa de Deus.', 0, 'Uma coisa peço... habitar na casa do Senhor'),
        mc('O que Davi busca acima de tudo?', ['Vinganca','Riqueza','Ver a bondade do Senhor','Fama'], 2, 'Salmo 27:4 - ver a bondade do Senhor'),
    ]),
    ('Salmo 121 - Guarda do Senhor', 'Ergo os meus olhos para os montes; de onde me vem o socorro? O meu socorro vem do Senhor, que fez os céus e a terra. O Senhor te guardará de todo mal.', 'Salmo 121:1-8', 'Confiança na guarda permanente de Deus', 'Salmo 121 é um dos gritos de peregrino: Deus não dorme, não cochila, e guarda a entrada e a saída do Seu povo.', [
        mc('De onde vem o socorro?', ['Dos montes','Do exercito','Do Senhor','Dos homens'], 2, 'Salmo 121:1-2'),
        vf('O Senhor dorme para descansar.', 'O Senhor dorme para descansar.', 0, 'O que guarda Israel nao dorme nem cochila'),
        mc('O que Deus guarda?', ['A entrada e a saida','Apenas a entrada','Apenas a saida','Nada'], 0, 'O Senhor guarda a tua entrada e a tua saida'),
    ]),
    ('Salmo 34 - Louvor Contínuo', 'Bendirei ao Senhor em todo tempo; o seu louvor estará sempre na minha boca. Provei e vi que o Senhor é bom; bem-aventurado o homem que nele confia.', 'Salmo 34:1-22', 'Cultivar um estilo de vida de louvor', 'Davi escreveu este salmo após fingir loucura diante de Abimeleque. Mostra que, mesmo em dificuldades, podemos louvar.', [
        mc('Quando Davi louva ao Senhor?', ['Apenas no sabado','Em todo tempo','So quando esta feliz','So na guerra'], 1, 'Salmo 34:1'),
        vf('Davi louvou mesmo fingindo ser louco.', 'Davi louvou mesmo fingindo ser louco.', 1, 'Escreveu este salmo depois desse episodio'),
        mc('O que o salmo diz do homem que confia em Deus?', ['E fraco','E forte','E mau','E abencoadado'], 3, 'Salmo 34:8 - bem-aventurado'),
    ]),
    ('Salmo 150 - A Grande Adoração', 'Louvai ao Senhor no seu santuário; louvai-o no firmamento do seu poder. Louvai-o com sons de trombeta, harpa, tamborim e dança.', 'Salmo 150:1-6', 'Expressar adoração com tudo que temos', 'Salmo 150 e o grande encerramento do livro dos Salmos: tudo o que tem fôlego louve ao Senhor!', [
        mc('O que deve louvar ao Senhor?', ['Apenas os sacerdotes','Tudo o que tem folego','So os homens','As pedras'], 1, 'Salmo 150:6'),
        vf('O louvor deve ser apenas com vozes.', 'O louvor deve ser apenas com vozes.', 0, 'Ha instrumentos: trombeta, harpa, tamborim, danca'),
        mc('Onde devemos louvar ao Senhor?', ['Em casa','No santuario','Na rua','No comercio'], 1, 'Salmo 150:1'),
    ]),
    ('Salmo 8 - Grandeza do Ser Humano', 'Senhor, o Teu nome é em toda a terra! Como é glorioso o Teu nome sobre os céus! Pôs os Teus abismos abaixo do homem.', 'Salmo 8:1-9', 'Reconhecer a dignidade que Deus deu ao ser humano', 'O salmo contempla a grandeza da criação e a honra que Deus deu ao homem, colocando tudo sob seus pés.', [
        mc('Como e o nome do Senhor?', ['Fraco','Glorioso em toda a terra','Secreto','Irrelevante'], 1, 'Salmo 8:1'),
        vf('O homem e menor que os anjos segundo o salmo.', 'O homem e menor que os anjos segundo o salmo.', 1, 'Salmo 8:5 - um pouco menor que os anjos, coroado de gloria e honra'),
        mc('O que Deus pos sob os pes do homem?', ['Os anjos','Os animais e a terra','Os pecados','As nuvens'], 1, 'Salmo 8:6-8'),
    ]),
    ('Salmo 16 - Alegria na Presença', 'Conserva-me, ó Deus, porque em Ti confio. Ao Senhor disse: tu és o meu Senhor, o meu bem não está em outro. Alegria há na Tua presença.', 'Salmo 16:1-11', 'Encontrar verdadeira alegria somente em Deus', 'Davi declara que o seu bem está em Deus, e que na Sua presença há plenitude de alegria e gozo eterno.', [
        mc('Onde esta o bem de Davi?', ['No mundo','Em si mesmo','Em Deus','Nenhum lugar'], 2, 'Salmo 16:2'),
        vf('Salmo 16 fala de tristeza permanente.', 'Salmo 16 fala de tristeza permanente.', 0, 'Ha plenitude de alegria na Tua presenca'),
        mc('O que Deus revela no salmo?', ['Caminhos de morte','Caminhos de vida','Silencio','Escuridao'], 1, 'Salmo 16:11 - mostrar-me-ás o caminho da vida'),
    ]),
    ('Salmo 42 - Anseio por Deus', 'Como anseia a corça por águas correntes, assim a minha alma anseia por Ti, ó Deus. A minha alma tem sede de Deus.', 'Salmo 42:1-11', 'Cultivar sede e fome de Deus', 'O salmista compara sua sede espiritual com a sede de uma corça. Mesmo em tempos difíceis, sua alma busca a Deus.', [
        mc('O que a corça busca?', ['Sombra','Aguas correntes','Comida','Fugir'], 1, 'Salmo 42:1'),
        vf('O salmista nunca sentiu tristeza.', 'O salmista nunca sentiu tristeza.', 0, 'Por que estás abatida, ó minha alma?'),
        mc('O que a alma do salmista busca?', ['Dinheiro','Poder','Deus','Fama'], 2, 'Salmo 42:2 - tem sede de Deus'),
    ]),
], 50)
print("  Trilha 4 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 5 - Profetas: Alertas e Esperanca
# ═══════════════════════════════════════════════
t5 = mk_trilha('Profetas: Alertas e Esperanca', 'Isaias, Jeremias, Daniel, Oseias, Amos e Joel: os mensageiros de Deus que alertaram e trouxeram esperanca', 'adulto', 'iniciante', 5, 'warning')
add_licoes(t5, [
    ('Isaías 53 - O Servo Sofredor', 'Ele foi desprezado e rejeitado pelos homens, homem de doenças e habituado ao sofrimento. Foi traspassado pelas nossas transgressões, moído pelas nossas iniquidades. Pela sua chaga fomos sarados.', 'Isaias 53:1-12', 'Reconhecer Jesus como o Servo Sofredor profetizado', 'Isaías 53 e a profecia mais clara sobre a morte expiatória de Jesus, escrita 700 anos antes da cruz.', [
        mc('O que o Servo Sofredor carregou?', ['O mundo','As nossas doencas','As nossas transgressoes','As nuvens'], 2, 'Isaias 53:4-5'),
        vf('O servo foi aceito pelos homens.', 'O servo foi aceito pelos homens.', 0, 'Foi desprezado e rejeitado'),
        mc('Pela chaga de quem fomos sarados?', ['De Moises','De Abraao','De Jesus','De Paulo'], 2, 'Isaias 53:5 - pela sua chaga fomos sarados'),
    ]),
    ('Isaías 9 - O Príncipe da Paz', 'Para nos nasceu uma criança, para nos foi dado um filho; e o principado estará sobre os seus ombros. Conselheiro maravilhoso, Deus fortíssimo, Pai eterno, Príncipe da Paz.', 'Isaias 9:1-7', 'Reconhecer Jesus como o Príncipe da Paz prometido', 'Isaías profetizou a vinda de um governante perfeito cujo reinado seria de paz, justiça eterna.', [
        mc('Como e chamado o filho que nascerá?', ['Principe da Guerra','Principe da Paz','Principe da Treva','Principe do Medo'], 1, 'Isaias 9:6'),
        vf('Isaias 9 fala de um rei temporario.', 'Isaias 9 fala de um rei temporario.', 0, 'O Seu governo e eterno'),
        mc('Quantos nomes o filho receba?', ['2','3','4','5'], 2, 'Isaias 9:6 - Conselheiro, Deus, Pai, Principe da Paz'),
    ]),
    ('Jeremias 29 - Planos de Bem', 'Porque eu bem sei os pensamentos que tenho a vosso respeito, pensamentos de paz e não de mal, para vos dar o fim que esperais.', 'Jeremias 29:11', 'Confiança nos planos de Deus mesmo na dificuldade', 'Deus falou ao povo exilado na Babilônia: mesmo longe de casa, Ele tinha planos de bem para restaurá-los.', [
        mc('O que Deus pensa para o Seu povo?', ['Mal','Paz e bem','Castigo eterno','Esquecimento'], 1, 'Jeremias 29:11'),
        vf('Deus planejava destruir o povo para sempre.', 'Deus planejava destruir o povo para sempre.', 0, 'Pensamentos de paz para dar fim esperado'),
        mc('Onde Deus falou isso ao povo?', ['Em Israel','Na Babilonia','No deserto','No Egito'], 1, 'Exilio na Babilonia'),
    ]),
    ('Jeremias 31 - A Nova Aliança', 'Farei uma aliança nova com Israel. Porei a minha Lei no seu interior e a escreverei nos seus corações. Serei o seu Deus e eles serão o meu povo.', 'Jeremias 31:31-34', 'Entender o fundamento da nova aliança em Cristo', 'A profecia da nova aliança revela que Deus colocaria Sua Lei no coração, não em tábuas de pedra.', [
        mc('Onde Deus escreveria Sua Lei?', ['Em pedras','No papel','No coracao','No chao'], 2, 'Jeremias 31:33'),
        vf('A nova alianca seria apenas para Israel.', 'A nova alianca seria apenas para Israel.', 0, 'Estende-se a todos que creem'),
        mc('O que Deus prometeu fazer?', ['Destruir tudo','Perdoar os pecados','Enviar um exercito','Mudar o clima'], 1, 'Jeremias 31:34 - perdoarei a sua iniquidade'),
    ]),
    ('Daniel 3 - Os Amigos no Forno', 'Sadraque, Mesaque e Abed-nego se recusaram a adorar a estátua de ouro de Nabucodonosor. Foram jogados no forno quente, mas Deus os livrou: nem o cheiro de fogo ficou neles.', 'Daniel 3:1-30', 'Coragem para se manter fiel mesmo sob ameaça', 'Os três jovens preferiram morrer a trair sua fé. Deus os livrou do forno, provando que Ele é soberano.', [
        mc('Por que foram jogados no forno?', ['Roubaram','Recusaram adorar a estatua','Oderam o rei','Nao trabalharam'], 1, 'Daniel 3:12'),
        vf('Os tres amigos morreram no forno.', 'Os tres amigos morreram no forno.', 0, 'Deus os livrou ilesos'),
        mc('Quantos amigos entraram no forno?', ['1','2','3','4'], 2, 'Sadraque, Mesaque e Abed-nego'),
    ]),
    ('Daniel 6 - Na Cova dos Leões', 'Daniel continuava orando a Deus três vezes por dia, mesmo com proibição. Denunciado, foi jogado na cova dos leões, mas Deus enviou um anjo e fechou as bocas dos leões.', 'Daniel 6:1-28', 'Fidelidade na oração como prioridade', 'Daniel não parou de orar mesmo sob ameaça de morte. Sua fé era tão firme que nem leões puderam contra ele.', [
        mc('Quantas vezes Daniel orava por dia?', ['Uma','Duas','Tres','Sete'], 2, 'Daniel 6:10'),
        vf('Daniel parou de orar quando foi proibido.', 'Daniel parou de orar quando foi proibido.', 0, 'Continuou orando normalmente'),
        mc('O que Deus fez na cova dos leoes?', ['Deixou Daniel morrer','Enviou anjo e fechou as bocas dos leoes','Abriu uma saída','Mudou os leoes em cordeiros'], 1, 'Daniel 6:22'),
    ]),
    ('Oseias 2 - Amor Infeliz restaurado', 'Deus comparou Oseias com uma mulher infiel, Gomer, para ilustrar como Israel era infiel a Deus. Mesmo assim, Deus prometeu restaurar e amar novamente.', 'Oseias 2:1-23', 'Entender o amor incondicional de Deus', 'A história de Oseias e Gomer é um retrato vivo do amor de Deus: fiel mesmo quando o povo trai.', [
        mc('Quem era Gomer?', ['A esposa de Oseias','A mae de Daniel','Uma rainha','Uma profetisa'], 0, 'Oseias 1:3'),
        vf('Deus abandonou Israel por ser infiel.', 'Deus abandonou Israel por ser infiel.', 0, 'Deus prometeu restaurar e amar novamente'),
        mc('O que Deus prometeu a Israel?', ['Castigo eterno','Restauracao e amor','Silencio','Esquecimento'], 1, 'Oseias 2:19-20 - te desposarei para sempre'),
    ]),
    ('Amos 5 - Justiça e Equidade', 'Buscai ao Senhor e viverei; buscai justiça e ponham a equidade. Odeio e desprezo os vossos festivais; não aceitarei as vossas ofertas.', 'Amos 5:4-24', 'Compreender que Deus prioriza justiça sobre ritual', 'Amos denunciou a religiosidade vazia: Deus quer justiça e equidade, não sacrifícios sem amor.', [
        mc('O que Deus odeia em Amos 5?', ['Os festivais e ofertas dos que praticam injustica','A busca da justica','O povo de Israel','A adoracao no templo'], 0, 'Amos 5:21-24 - odeio as vossas festas; buscai justica, nao rituais vazios'),
        vf('Deus aceita sacrificios de quem pratica injustica.', 'Deus aceita sacrificios de quem pratica injustica.', 0, 'Rejeitou as ofertas dos opressores'),
        mc('O que Amos diz que devemos buscar?', ['Riqueza','Fama','Justica e equidade','Vinganca'], 2, 'Amos 5:24 - corra a justica como agua'),
    ]),
    ('Mateus 6 - O Messias Pobre', 'Jesus nasceu em manjedoura e cresceu em Nazaré, cidade humilde. Disse: "A raposa tem tocas, e as aves do céu têm ninhos, mas o Filho do Homem não tem onde repousar a cabeça."', 'Mateus 8:19-20; Lucas 2:7', 'Reconhecer a humildade do Deus que veio ao mundo', 'Jesus escolheu a pobreza para redimir os pobres. O Messias prometido veio sem ostentação, em humildade.', [
        mc('Onde Jesus nasceu?', ['Num palacio','Numa manjedoura','Num templo','Numa cidade grande'], 1, 'Lucas 2:7'),
        vf('Jesus viveu em luxo durante seu ministerio.', 'Jesus viveu em luxo durante seu ministerio.', 0, 'Mateus 8:20 - nao tinha onde repousar a cabeca'),
        mc('Que cidade Jesus cresceu?', ['Jerusalem','Nazare','Betlem','Capernaum'], 1, 'Mateus 2:23 - Nazare da Galileia'),
    ]),
    ('Joel 2 - O Dia do Senhor', 'O dia do Senhor vem, dia de trevas e não de luz. Mas depois diz: "Derramarei do Meu Espírito sobre toda carne; vossos filhos e vossas filhas profetizarão."', 'Joel 2:1-32', 'Preparar-se para o Dia do Senhor e receber o Espírito', 'Joel profetizou o juízo e a restauração, e a promessa do derramamento do Espírito, cumprida em Atos 2.', [
        mc('O que sera o dia do Senhor?', ['Alegria total','Trevas e nao luz','Um festival','Um descanso'], 1, 'Joel 2:2'),
        vf('Deus derramaria Seu Espirito apenas sobre homens velhos.', 'Deus derramaria Seu Espirito apenas sobre homens velhos.', 0, 'Sobre toda carne, filhos e filhas'),
        mc('Sobre quem o Espirito seria derramado?', ['Apenas sacerdotes','Sobre toda carne','Apenas reis','Apenas mulheres'], 1, 'Joel 2:28'),
    ]),
], 50)
print("  Trilha 5 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 6 - Jesus: Vida e Ministerio
# ═══════════════════════════════════════════════
t6 = mk_trilha('Jesus: Vida e Ministerio', 'Do nascimento a ascensao: os milagres, ensinamentos, paixao e ressurreição de Jesus Cristo', 'adulto', 'iniciante', 6, 'auto_awesome')
add_licoes(t6, [
    ('Mateus 1 - O Nascimento de Jesus', 'A genealogia de Jesus, filho de Davi, filho de Abraão. Maria, noiva de José, concebeu pelo Espírito Santo. José, homem justo, a recebeu sem dúvidas.', 'Mateus 1:1-25', 'Compreender a origem divina e humana de Jesus', 'Jesus veio da linhagem de Davi, cumprindo as profecias. Sua concepção foi miraculosa, pelo poder do Espírito Santo.', [
        mc('De quem Jesus descende?', ['Adao','Abraao e Davi','Moises','Noe'], 1, 'Mateus 1:1'),
        vf('Jose era duvidoso sobre a gravidez de Maria.', 'Jose era duvidoso sobre a gravidez de Maria.', 0, 'Jose era justo e a recebeu sem duvidas'),
        mc('Como Maria concebeu?', ['Naturalmente','Pelo Espirito Santo','Por um anjo','Por um milagre no templo'], 1, 'Mateus 1:18'),
    ]),
    ('Mateus 3 - O Batismo de Jesus', 'João Batista batizou Jesus no Rio Jordão. Ao subir das águas, os céus se abriram e o Espírito desceu como pomba. Uma voz disse: "Este é o Meu Filho amado."', 'Mateus 3:13-17', 'Entender o significado do batismo e da aprovação divina', 'Jesus, sendo sem pecado, foi batizado para cumprir toda justiça e iniciar Seu ministério público.', [
        mc('Quem baptizou Jesus?', ['Pedro','Joao Batista','Paulo','Tiago'], 1, 'Mateus 3:13'),
        vf('Jesus precisava de batismo para perdoar pecados.', 'Jesus precisava de batismo para perdoar pecados.', 0, 'Foi para cumprir toda a justica'),
        mc('O que desceu sobre Jesus?', ['Uma estrela','Uma pomba','Um anjo','Nuvem escura'], 1, 'Mateus 3:16 - o Espirito desceu como pomba'),
    ]),
    ('Mateus 4 - A Tentação no Deserto', 'Jesus foi conduzido ao deserto pelo Espírito e foi tentado por Satanás por 40 dias. Resistiu a cada tentação com a Palavra de Deus: "Está escrito."', 'Mateus 4:1-11', 'Aprender a resistir à tentação com a Palavra', 'Jesus usou a Escritura para vencer cada tentação. O exemplo é modelo para todos os crentes.', [
        mc('Quem tentou Jesus no deserto?', ['Um fariseu','Satanás','Um romano','Joao Batista'], 1, 'Mateus 4:1'),
        vf('Jesus cedeu a primeira tentacao.', 'Jesus cedeu a primeira tentacao.', 0, 'Resistiu dizendo "Esta escrito"'),
        mc('O que Jesus respondeu a cada tentacao?', ['Eu sou Deus','Esta escrito','Vai embora','Nao quero'], 1, 'Mateus 4:4, 7, 10'),
    ]),
    ('Mateus 5 - O Sermão do Monte', 'Jesus sentou e ensinou: Bem-aventurados os pobres de espírito, os mansos, os que choram, os que têm fome e sede de justiça. Vós sois a luz do mundo.', 'Mateus 5:1-48', 'Assimilar os ensinamentos fundamentais de Jesus', 'O Sermão do Monte e a constituição do Reino de Deus: valores inversos ao mundo, amor aos inimigos, perfeição.', [
        mc('Quem sao bem-aventurados segundo Jesus?', ['Os ricos','Os poderosos','Os pobres de espirito','Os sábios'], 2, 'Mateus 5:3'),
        vf('Jesus disse para odiar os inimigos.', 'Jesus disse para odiar os inimigos.', 0, 'Amai os vossos inimigos'),
        mc('Vós sois a luz do mundo. Uma cidade:', ['Escondida','Aclamada','Assentada sobre um monte','Nas trevas'], 2, 'Mateus 5:14'),
    ]),
    ('Mateus 9 - O Coração de Jesus', 'Jesus viu as multidões e teve compaixão, porque estavam cansadas e dispersas como ovelhas sem pastor. Começou a curar doentes e perdoar pecados.', 'Mateus 9:1-38', 'Reconhecer a compaixão infinita de Jesus', 'Jesus sentiu profunda compaixão e agiu: curou paralíticos, perdoou pecados e chamou pecadores.', [
        mc('O que Jesus sentiu ao ver as multidoes?', ['Raiva','Indiferenca','Compaixao','Medo'], 2, 'Mateus 9:36'),
        vf('Jesus rejeitou pecadores.', 'Jesus rejeitou pecadores.', 0, 'Comia com publicanos e pecadores'),
        mc('O que Jesus disse aos discipulos?', ['Fujam','Orem mais','A ceifa e muita, mas os operarios sao poucos','Deixem as multidoes'], 2, 'Mateus 9:37'),
    ]),
    ('Mateus 13 - As Parábolas', 'Jesus ensinou em parábolas: o Semeador, o Joio e o Trigo, o Grão de Mostarda, o Tesouro Escondido, a Pérola de grande valor e a Rede.', 'Mateus 13:1-58', 'Entender os ensinamentos de Jesus através de histórias', 'As parábolas revelam mistérios do Reino de Deus: como a Palavra é semeada, cresce e traz frutos.', [
        mc('O que representa a semente no parabola do Semeador?', ['Dinheiro','A Palavra de Deus','O povo','Os pecados'], 1, 'Mateus 13:18-23'),
        vf('Todas as parabolas sao iguais.', 'Todas as parabolas sao iguais.', 0, 'Cada uma ensina algo diferente'),
        mc('O que e o Reino dos Ceus?', ['Um lugar fisico','O valor mais importante','Um imperio romano','Uma ilusao'], 1, 'Grao de mostarda, tesouro, perola - valioso'),
    ]),
    ('Mateus 14 - Pão e Peixes', 'Jesus alimentou 5 mil homens com cinco pães e dois peixes, multiplicando-os. Também caminhou sobre as águas e acalmou a tempestade.', 'Mateus 14:13-33', 'Confiar no poder de Jesus para suprir necessidades', 'Jesus transformou o pouco em abundância, demonstrando ser Senhor da criação e provedor do povo.', [
        mc('Quantas pessoas foram alimentadas?', ['3 mil','4 mil','5 mil','10 mil'], 2, 'Mateus 14:21'),
        vf('Jesus usou 12 pães para alimentar a multidao.', 'Jesus usou 12 pães para alimentar a multidao.', 0, 'Cinco pães e dois peixes'),
        mc('O que Jesus fez sobre as aguas?', ['Nadou','Caminhou','Afundou','Desceu num barco'], 1, 'Mateus 14:25 - caminhou sobre o mar'),
    ]),
    ('João 1 - O Verbo se Fez Carne', 'No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus. Tudo foi feito por Ele. E o Verbo se fez carne e habitou entre nós.', 'João 1:1-18', 'Entender a natureza divina e eterna de Jesus', 'João apresenta Jesus como o Verbo eterno, pré-existente, criador de todas as coisas que veio habitar entre os homens.', [
        mc('Quem e o Verbo?', ['Joao Batista','Jesus','Pedro','Abraao'], 1, 'João 1:1, 14'),
        vf('O Verbo comecou a existir quando Jesus nasceu.', 'O Verbo comecou a existir quando Jesus nasceu.', 0, 'No principio era o Verbo - eterno'),
        mc('O que Jesus trouxe?', ['Lei nova','Graça e verdade','Castigo','Riquezas'], 1, 'João 1:17 - graça e verdade'),
    ]),
    ('João 3 - Nascer de Novo', 'Jesus disse a Nicodemos: "É necessário nascer de novo para ver o Reino de Deus. Quem crê no Filho unigênito não perece, mas tem a vida eterna."', 'João 3:1-36', 'Compreender a necessidade do novo nascimento espiritual', 'Jesus revelou que a salvação vem pelo nascimento espiritual e pela fé no Filho de Deus.', [
        mc('Com quem Jesus conversou?', ['Pedro','Nicodemos','Paulo','Um fariseu anônimo'], 1, 'João 3:1'),
        vf('Jesus disse que precisamos nascer apenas uma vez.', 'Jesus disse que precisamos nascer apenas uma vez.', 0, 'Nascer de novo - segundo nascimento'),
        mc('Qual o versiculo mais famoso?', ['Mateus 6:33','João 3:16','Romanos 8:28','Salmo 23:1'], 1, 'João 3:16 - assim amou Deus ao mundo'),
    ]),
    ('João 4 - A Samaritana', 'Jesus falou com uma mulher samaritana no poço de Jacó. Revelou que Ele é o Messias e que Deus busca adoradores em espírito e em verdade.', 'João 4:1-42', 'Entender que Jesus transcende barreiras sociais', 'Jesus quebrou barreiras de gênero, religião e cultura ao falar com a samaritana, revelando que todos são bem-vindos.', [
        mc('Quem Jesus encontrou no poço?', ['Uma judia','Uma samaritana','Uma romana','Uma egipcia'], 1, 'João 4:7'),
        vf('Jesus se recusou a falar com a samaritana.', 'Jesus se recusou a falar com a samaritana.', 0, 'Falou e revelou que era o Messias'),
        mc('Onde Deus quer que O adoremos?', ['No monte','Em Jerusalems','Em espirito e em verdade','Apenas no templo'], 2, 'João 4:23-24'),
    ]),
    ('João 15 - A Videira e os Ramos', 'Eu sou a videira verdadeira, e o meu Pai é o lavrador. Permanecei em mim, e eu em vós. Sem mim nada podeis fazer.', 'João 15:1-27', 'Compreender a necessidade de permanecer em Cristo', 'Jesus é a videira; nós somos os ramos. Só frutificamos quando estamos ligados a Ele.', [
        mc('O que Jesus e?', ['O pastor','A videira','A pedra','O rei'], 1, 'João 15:1'),
        vf('Podemos frutificar sem Jesus.', 'Podemos frutificar sem Jesus.', 0, 'Sem mim nada podeis fazer'),
        mc('O que acontece com o ramo que nao permanece?', ['Fica no chao','E cortado e seco','Floresce','Cresce'], 1, 'João 15:6 - cortado e seco'),
    ]),
    ('Marcos 8 - A Cura dos Cegos', 'Jesus aplicou lama nos olhos de um cego de Betsaida e ele passou a ver. Depois, Jesus perguntou: "Que vês?" E o homem via tudo claramente.', 'Marcos 8:22-26', 'Reconhecer Jesus como o curador completo', 'Jesus curou em etapas, mostrando que o milagre é gradual e que Ele cuida de cada detalhe da cura.', [
        mc('O que Jesus aplicou nos olhos do cego?', ['Agua','Oleo','Lama','Sangue'], 2, 'Marcos 8:23'),
        vf('O cego enxergou perfeitamente de primeira.', 'O cego enxergou perfeitamente de primeira.', 0, 'Jesus aplicou duas vezes'),
        mc('Jesus perguntou ao cego:', ['Quem és?', 'Que vêes?', 'Onde vais?', 'O que fazes?'], 1, 'Marcos 8:23'),
    ]),
], 50)
print("  Trilha 6 completa - 12 licoes")

# ═══════════════════════════════════════════════
# TRILHA 7 - Atos: A Igreja em Expansao
# ═══════════════════════════════════════════════
t7 = mk_trilha('Atos: A Igreja em Expansao', 'O livro de Atos: da ascensao de Jesus a chegada do evangelho em Roma, pelo poder do Espirito Santo', 'adulto', 'iniciante', 7, 'local_fire_department')
add_licoes(t7, [
    ('Atos 1 - A Ascensão de Jesus', 'Jesus ressuscitado apareceu aos discípulos por 40 dias, falando do Reino de Deus. Depois, diante deles, foi elevado ao céu. Dois anjos disseram: "Esse Jesus, que foi elevado, voltará."', 'Atos 1:1-11', 'Entender a ascensão e a promessa do retorno', 'A ascensão marca a conclusão da obra terrena de Jesus e a espera ativa pela volta d\'Ele.', [
        mc('Por quantos dias Jesus apareceu apos ressuscitar?', ['10','20','40','50'], 2, 'Atos 1:3'),
        vf('Jesus ascendeu ao ceu de barco.', 'Jesus ascendeu ao ceu de barco.', 0, 'Foi elevado aos ceus'),
        mc('O que os anjos disseram?', ['Ele morreu','Ele voltara como foi elevado','Ele esqueceu','Ele dormiu'], 1, 'Atos 1:11'),
    ]),
    ('Atos 2 - O Pentecostes', 'No dia de Pentecostes, um som como vento forte encheu a casa. Línguas de fogo pousaram sobre cada um. Começaram a falar em outras línguas. Pedro pregou e 3 mil foram salvos.', 'Atos 2:1-47', 'Receber o poder do Espírito Santo', 'O Pentecostes e o cumprimento da promessa de Jesus: o Espírito Santo habita nos crentes e dá poder para testemunhar.', [
        mc('O que os discipulos receberam no Pentecostes?', ['Riquezas','Línguas de fogo e poder','Armazens','Novas leis'], 1, 'Atos 2:3-4'),
        vf('Apenas 100 pessoas foram salvas no Pentecostes.', 'Apenas 100 pessoas foram salvas no Pentecostes.', 0, 'Foram 3 mil homens'),
        mc('Quem pregou no Pentecostes?', ['Paulo','Pedro','Tiago','João'], 1, 'Atos 2:14'),
    ]),
    ('Atos 4 - Coragem na Perseguição', 'Pedro e João foram presos por pregar a ressurreição. Mas não pararam. A igreja orou e o Espírito Santo os encheu de ousadia.', 'Atos 4:1-31', 'Ter coragem para testemunhar mesmo sob perseguição', 'Os líderes da igreja enfrentaram ameaças e prisões, mas oraram por mais coragem e não por livramento.', [
        mc('Quem foi preso por pregar?', ['Paulo e Barnabé','Pedro e João','Tiago e Filipe','Estevão'], 1, 'Atos 4:1-3'),
        vf('Os apóstolos pararam de pregar quando presos.', 'Os apóstolos pararam de pregar quando presos.', 0, 'Nao pararam, pregavam com coragem'),
        mc('O que a igreja pediu em oracao?', ['Dinheiro','Fama','Mais coragem e ousadia','Vinganca'], 2, 'Atos 4:29 - conceda que os Teus servos falem com toda ousadia'),
    ]),
    ('Atos 7 - O Martírio de Estêvão', 'Estêvão, cheio do Espírito Santo, enfrentou o Sinédrio com um discurso ousado. Apedrejado, pediu: "Senhor, não lhes imputes este pecado." Foi o primeiro mártir cristão.', 'Atos 7:1-60', 'Reconhecer o custo e a honra do testemunho fiel', 'Estêvão viu os céus abertos e perdoou seus assassinos, imitando a Jesus. Sua morte espalhou o evangelho.', [
        mc('Quem foi o primeiro martir cristão?', ['Pedro','Paulo','Estevão','Tiago'], 2, 'Atos 7:60'),
        vf('Estevão morreu xingando seus assassinos.', 'Estevão morreu xingando seus assassinos.', 0, 'Perdoou e pediu que nao lhes imputassem pecado'),
        mc('O que Estevão viu antes de morrer?', ['Um anjo','Os ceus abertos e Jesus de pe','Uma estrela','Nada'], 1, 'Atos 7:55-56'),
    ]),
    ('Atos 9 - A Conversão de Saulo', 'Saulo ia perseguindo cristãos quando uma luz do céu o derrubou. Jesus disse: "Saulo, Saulo, por que me persegues?" Saulo se converteu e se tornou o apóstolo Paulo.', 'Atos 9:1-31', 'Entender que Jesus transforma vidas radicalmente', 'O maior perseguidor da igreja se tornou o maior missioneiro da história. Ninguém está longe da graça de Deus.', [
        mc('O que derrubou Saulo no caminho?', ['Um terremoto','Uma luz do ceu','Um cavalo','Um rio'], 1, 'Atos 9:3'),
        vf('Saulo continuou perseguindo cristãos depois do encontro.', 'Saulo continuou perseguindo cristãos depois do encontro.', 0, 'Tornou-se apóstolo Paulo'),
        mc('Como Jesus chamou Saulo?', ['Saulo, Saulo','Paulo, Paulo','Servo, servo','Amigo, amigo'], 0, 'Atos 9:4 - Saulo, Saulo, por que me persegues?'),
    ]),
    ('Atos 10 - Cornélio e Pedro', 'Deus mandou um anjo a Cornélio, romano piedoso. Em sonho, Pedro viu um pano com animais e Deus disse: "O que Deus purificou, não chames de impuro." Pedro entendeu que o evangelho é para todos.', 'Atos 10:1-48', 'Compreender que o evangelho é para todas as nações', 'A visão do pano ensinou a Pedro que a graça de Deus não faz diferença entre judeus e gentios.', [
        mc('Quem era Cornelio?', ['Judeu','Romano piedoso','Publicano','Fariseu'], 1, 'Atos 10:1'),
        vf('Pedro sempre soube que o evangelho era para os gentios.', 'Pedro sempre soube que o evangelho era para os gentios.', 0, 'Precisou de uma visão de Deus'),
        mc('O que Deus disse a Pedro sobre os animais?', ['São impuros', 'O que Deus purificou, nao chames de impuro','Deves comer todos','Nao deves tocar'], 1, 'Atos 10:15'),
    ]),
    ('Atos 16 - A Conversão em Filipos', 'Paulo e Silas foram presos em Filipos, mas cantavam hinos na prisão. Um terremoto abriu as portas. O carcereiro perguntou: "Que devo fazer para ser salvo?" Resposta: "Crê no Senhor Jesus."', 'Atos 16:16-34', 'Experimentar a liberdade que vem da fé em Jesus', 'Mesmo na prisão, Paulo e Silas louvavam. Deus abriu as portas e salvou o carcereiro e toda a sua família.', [
        mc('O que Paulo e Silas faziam na prisão?', ['Dormiam','Cantavam hinos','Choravam','Gritavam'], 1, 'Atos 16:25'),
        vf('O carcereiro se tornou cristão antes de ouvir sobre Jesus.', 'O carcereiro se tornou cristão antes de ouvir sobre Jesus.', 0, 'Ouviu a pregação e creu'),
        mc('O que aconteceu quando Paulo e Silas cantavam?', ['Nada','Um terremoto abriu as portas','O carcereiro dormiu','Choveu'], 1, 'Atos 16:26'),
    ]),
    ('Atos 17 - O Areópago', 'Paulo pregou em Atenas, no Areópago, citando poetas gregos. Falou do "Deus desconhecido" que deu vida a todos. Alguns zombaram, outros creram.', 'Atos 17:16-34', 'Usar a cultura para comunicar o evangelho', 'Paulo usou a cultura local para apresentar o Deus verdadeiro, adaptando sua mensagem sem comprometer a verdade.', [
        mc('Onde Paulo preguou em Atenas?', ['No teatro','No Areópago','No circo','No palacio'], 1, 'Atos 17:19'),
        vf('Paulo citou apenas a Bíblia hebraica.', 'Paulo citou apenas a Bíblia hebraica.', 0, 'Tambem citou poetas gregos'),
        mc('O que Paulo disse sobre o "Deus desconhecido"?', ['Não existe','E o Deus verdadeiro','E um falso deus','E irrelevante'], 1, 'Atos 17:23 - esse Deus vos declaro'),
    ]),
    ('Atos 21 - A Prisão em Jerusalém', 'Paulo voltou a Jerusalém sabendo que seria preso. Multidões o atacaram, romanos o prenderam para protegê-lo. Paulo usou cada oportunidade para pregar.', 'Atos 21:1-40', 'Perseguir o chamado mesmo com custos', 'Paulo sabia do perigo, mas cumpriu o chamado. Na prisão, sempre encontrava forma de testemunhar.', [
        mc('Paulo sabia que seria preso?', ['Nao sabia','Sim, sabia','Duvidava','Nao se importava'], 1, 'Atos 20:22-23; 21:13'),
        vf('Paulo fugiu quando a multidão o atacou.', 'Paulo fugiu quando a multidão o atacou.', 0, 'Ficou e enfrentou a situacao'),
        mc('Quem prendeu Paulo?', ['Fariseus','Sadduceus','Romanos','Samaritanos'], 2, 'Romano para protege-lo da multidão'),
    ]),
    ('Atos 28 - O Evangelho em Roma', 'Paulo chegou a Roma como prisioneiro, mas alugou uma casa e recebeu os líderes judeus. Pregou o Reino de Deus com franqueza. O livro termina com Paulo livre.', 'Atos 28:16-31', 'Reconhecer que o evangelho não pode ser detido', 'Mesmo preso em Roma, Paulo continuou pregando. O livro de Atos termina aberto: o evangelho continua se espalhando.', [
        mc('Onde Paulo ficou em Roma?', ['Na cruz','Alugou uma casa','Na prisão','No palacio'], 1, 'Atos 28:30'),
        vf('Paulo parou de pregar quando preso em Roma.', 'Paulo parou de pregar quando preso em Roma.', 0, 'Continuou pregando com franqueza'),
        mc('Como o livro de Atos termina?', ['Com a morte de Paulo','Com o evangelho se espalhando livremente','Com Paulo solto','Com um ponto final fechado'], 1, 'O evangelho continuou sem impedimento'),
    ]),
], 50)
print("  Trilha 7 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 8 - Romanos: O Evangelho da Graça
# ═══════════════════════════════════════════════
t8 = mk_trilha('Romanos: O Evangelho da Graça', 'A epistola mais sistematica do apostolo Paulo sobre justificacao, santificacao e vida cristã', 'adulto', 'intermediario', 8, 'balance')
add_licoes(t8, [
    ('Romanos 1-2: O Pecado Geral', 'Paulo argumenta que tanto os gentios quanto os judeus estão sob o julgamento de Deus. Todos pecaram e faltam da glória de Deus. Nenhum sistema religioso ou moral pode livrar o ser humano da culpa.', 'Romanos 1:18-3:20', 'Compreender que todos os seres humanos são pecadores diante de Deus', 'Toda humanidade, sem exceção, é culpada diante de Deus. Nem conhecimento da Lei nem a criação deixam desculpa.', [
        mc('Segundo Paulo, quem esta sob o julgamento de Deus?', ['Apenas os gentios','Apenas os judeus','Todos os seres humanos','Apenas os pecadores'], 2, 'Romanos 3:23 - todos pecaram'),
        vf('Os judeus estavam livres do julgamento por terem a Lei.', 'Os judeus estavam livres do julgamento por terem a Lei.', 0, 'Romanos 2:12 - todos serao julgados pela Lei'),
        mc('Qual e a expressao-chave de Romanos 3:23?', ['Deus e amor','Todos pecaram','Jesus salvou','Leia a Biblia'], 1, 'Todos pecaram e faltam da gloria de Deus'),
    ]),
    ('Romanos 3: Justificação pela Fé', 'A justificação é pela graça, mediante a redenção que há em Cristo Jesus. Deus propôs o propiciatório pelo sangue de fé, para demonstrar a Sua justiça. A justificação é um dom, não por obras.', 'Romanos 3:21-31', 'Entender o que significa ser justificado pela fé em Jesus', 'A justificação é um ato gratuito de Deus que nos declara justos com base na obra de Cristo, não nas nossas obras.', [
        mc('O que significa ser justificado?', ['Ser perfeito','Ser declarado justo por Deus','Nunca mais pecar','Entrar na igreja'], 1, 'Justificacao e declaracao de justica diante de Deus'),
        vf('A justificacao depende de nossas boas obras.', 'A justificacao depende de nossas boas obras.', 0, 'Romanos 3:24 - gratuitamente, pela graça'),
        mc('Pela fe de quem somos justificados?', ['De Abraao','De Jesus Cristo','De Paulo','De nos mesmos'], 1, 'Romanos 3:22 - pela fe em Jesus Cristo'),
        mc('Justificacao pela fe anula a Lei?', ['Sim, completamente','Nao, ela e estabelecida','Apenas para judeus','Depende'], 1, 'Romanos 3:31 - estabelecemos a Lei pela fe'),
    ]),
    ('Romanos 4: Abraão Pela Fé', 'Abraão acreditou em Deus e lhe foi imputada justiça. Ele recebeu a promessa não pelas obras, mas pela imputação da fé. A justificação pela fé é o modelo de Abraão para todos os crentes.', 'Romanos 4:1-25', 'Reconhecer que Abraão é o exemplo máximo da justificação pela fé', 'Assim como Abraão creu em Deus e lhe foi contado como justiça, nós também somos justificados pela fé, não pelas obras.', [
        mc('O que foi imputado a Abraao por sua fe?', ['Riqueza','Justica','Poder','Familia'], 1, 'Romanos 4:3 - creu em Deus e lhe foi imputada justica'),
        vf('Abraao foi justificado por sua obediencia a Lei de Moises.', 'Abraao foi justificado por sua obediencia a Lei de Moises.', 0, 'Abraao viveu antes de Moises'),
        mc('A fe de Abraao foi dirigida a:', ['Si mesmo','A Lei','Deus que ressuscita mortos','Os profetas'], 2, 'Romanos 4:17 - diante dAquele em quem creu'),
        mc('A promessa a Abraao veio:', ['Pela Lei','Pela fe','Pela circumcision','Pela obediencia'], 1, 'Pela fe, antes da Lei'),
    ]),
    ('Romanos 5: Paz com Deus', 'Sendo justificados pela fé, temos paz com Deus através de nosso Senhor Jesus Cristo. A graça de Deus abunda onde o pecado aumentou. O amor de Deus foi derramado em nossos corações.', 'Romanos 5:1-11', 'Experimentar a paz que vem da justificação pela fé', 'A justificação traz paz com Deus, acesso à graça e esperança da glória de Deus. O amor de Cristo nos salva.', [
        mc('O que temos sendo justificados pela fe?', ['Medo','Paz com Deus','Perfeicao','Sabedoria'], 1, 'Romanos 5:1 - temos paz com Deus'),
        vf('A graça de Deus diminui onde o pecado aumenta.', 'A graça de Deus diminui onde o pecado aumenta.', 0, 'A graça abunda ainda mais - Romanos 5:20'),
        mc('Onde o amor de Deus foi derramado?', ['Na terra','Nos coracoes dos crentes','No templo','No ceu'], 1, 'Romanos 5:5 - o amor de Deus foi derramado'),
    ]),
    ('Romanos 6: Libertação do Pecado', 'Devemos viver como mortos para o pecado e vivos para Deus. Fomos batizados com Cristo na morte e ressurreição. O pecado não terá domínio sobre nós, pois estamos debaixo da graça.', 'Romanos 6:1-23', 'Entender que a graça não é licença para pecar', 'A graça liberta do pecado, não autoriza a viver nele. Somos novas criaturas em Cristo.', [
        mc('Devemos continuar pecando para que a graça abunda?', ['Sim','Nao','Talvez','Depende'], 1, 'Romanos 6:1-2 - de forma alguma!'),
        vf('Somos batizados na morte e ressurreição de Cristo.', 'Somos batizados na morte e ressurreição de Cristo.', 1, 'Romanos 6:3-4'),
        mc('O que governa o crente?', ['O pecado','A graça de Deus','O mundo','A carne'], 1, 'Debaixo da graça, nao debaixo da Lei'),
    ]),
    ('Romanos 7: A Luta Interior', 'Paulo descreve a luta entre a carne e o espírito. "O bem que quero não faço, e o mal que não quero, isso pratico." A lei é santa, mas a carne é fraca.', 'Romanos 7:15-25', 'Reconhecer a luta interior de todo cristão maduro', 'A luta contra o pecado é real, mas Cristo é a vitória. A lei mostra o pecado, mas não liberta dele.', [
        mc('O que Paulo diz sobre o pecado?', ['Nunca pequei','O bem que quero, nao faço','O pecado e bom','Nao existe pecado'], 1, 'Romanos 7:19'),
        vf('Paulo conclui que somos salvos pelas obras da Lei.', 'Paulo conclui que somos salvos pelas obras da Lei.', 0, 'Conclui que Jesus Cristo e a libertacao'),
        mc('A Lei e:', ['Má','Boa e santa','Irrelevante','Necessaria para salvar'], 1, 'Romanos 7:12 - a Lei e santa, e o mandamento justo'),
    ]),
    ('Romanos 8: Sem Condenação', 'Não há condenação para os que estão em Cristo Jesus. O Espírito Santo liberta da lei do pecado e da morte. Nada pode nos separar do amor de Deus em Cristo.', 'Romanos 8:1-39', 'Viver na certeza de não haver condenação para quem está em Cristo', 'A vida no Espírito traz liberdade, adoção como filhos e segurança eterna no amor de Deus.', [
        mc('Ha condenacao para quem esta em Cristo?', ['Sim sempre','Nunca','Apenas em pecados graves','Apenas na terra'], 1, 'Romanos 8:1 - nenhuma'),
        vf('O Espirito Santo nos liberta da lei do pecado.', 'O Espirito Santo nos liberta da lei do pecado.', 1, 'Romanos 8:2 - a lei do Espirito de vida'),
        mc('O que pode nos separar do amor de Deus?', ['Pecado','Morte','Anjos','Nada'], 3, 'Romanos 8:38-39 - nada podera nos separar'),
        mc('Em Romanos 8, somos chamados de:', ['Escravos','Hospedes','Filhos de Deus','Estrangeiros'], 2, 'Romanos 8:16 - filhos de Deus'),
    ]),
    ('Romanos 9: A Eleição Divina', 'Paulo discute a soberania de Deus na escolha de Israel e na eleição dos crentes. Deus tem misericórdia de quem quer e endurece quem quer. O barro não pode questionar o oleiro.', 'Romanos 9:1-24', 'Entender a soberania de Deus na eleição', 'Deus é soberano na Sua escolha, mas isso não anula a responsabilidade humana de crer.', [
        mc('Quem tem misericordia de quem?', ['O homem escolhe','Deus escolhe','A sorte decide','Ninguem'], 1, 'Romanos 9:15 - terei misericordia de quem tiver misericordia'),
        vf('O barro pode questionar o oleiro sobre por que foi feito assim.', 'O barro pode questionar o oleiro.', 0, 'Romanos 9:20 - quem es tu, o homem?'),
        mc('Para que Deus endurece?', ['Por maldade','Para demonstrar poder','Sem motivo','Para punir todos'], 1, 'Romanos 9:17 - para demonstrar o Meu poder'),
    ]),
    ('Romanos 12: Viva em Sacrifício', 'Paulo pede que ofereçamos nossos corpos como sacrifício vivo e santo a Deus. Não nos conformemos com este mundo, mas transformemo-nos pela renovação do entendimento.', 'Romanos 12:1-21', 'Renovar a vida como sacrifício vivo a Deus', 'A vida cristã prática envolve consagração, serviço, amor genuíno e não retaliação.', [
        mc('O que Paulo pede que oferecamos?', ['Dinheiro','Tempo','Nossos corpos como sacrificio','Animais'], 2, 'Romanos 12:1'),
        vf('Devemos nos conformar com os padroes deste mundo.', 'Devemos nos conformar com os padroes deste mundo.', 0, 'Romanos 12:2 - nao vos conformeis'),
        mc('Como somos transformados?', ['Pelo dinheiro','Pela renovacao do entendimento','Pela politica','Pela forca'], 1, 'Renovacao do entendimento para experimentar a boa vontade de Deus'),
        mc('Paulo diz para:', ['Vingar-se dos inimigos','Amar e perdoar','Odiar o pecador','Fugir do mundo'], 1, 'Romanos 12:21 - vence o mal com o bem'),
    ]),
    ('Romanos 13: Submissão às Autoridades', 'Todo poder vem de Deus. Devemos estar sujeitos às autoridades, pagar impostos, honrar todos e amar ao próximo como a nós mesmos. O amor cumpre a Lei.', 'Romanos 13:1-14', 'Entender a relação entre fé cristã e autoridade civil', 'Deus estabeleceu autoridades para ordem. O crente deve submeter-se, mas o amor é a Lei suprema.', [
        mc('De onde vem todo poder?', ['Do povo','Do diabo','Deus','Do governo'], 2, 'Romanos 13:1 - toda autoridade vem de Deus'),
        vf('O crente deve sempre desobedecer ao governo.', 'O crente deve sempre desobedecer ao governo.', 0, 'Romanos 13:1 - esteja sujeito'),
        mc('Qual mandamento resume toda a Lei no contexto de Romanos 13?', ['Nao mataras','Amaras ao proximo','Guarda o sabado','Nao teras outros deuses'], 1, 'Romanos 13:9 - amaras ao proximo como a ti mesmo'),
    ]),
], 50)
print("  Trilha 8 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 9 - Corintios e Galatas
# ═══════════════════════════════════════════════
t9 = mk_trilha('Corintios e Galatas', 'Paulo corrige a igreja em Corinto sobre divisoes, imoralidade e espiritualidade, e defende a justificacao pela fe aos galatas', 'adulto', 'intermediario', 9, 'forum')
add_licoes(t9, [
    ('1 Coríntios 1: Sabedoria da Cruz', 'Paulo repreende as divisões na igreja de Corinto. A sabedoria de Deus é loucura para o mundo. Cristo crucificado é o poder e sabedoria de Deus, não a retórica humana.', '1 Corintios 1:18-31', 'Reconhecer que a sabedoria de Deus está na cruz', 'O mundo busca sabedoria eloquente, mas Deus usa o que é fraco e louco aos olhos do mundo para confundir os sábios.', [
        mc('O que e loucura para os que perecem?', ['A cruz','A oracao','O batismo','A ceia'], 0, '1 Corintios 1:18 - a palavra da cruz e loucura'),
        vf('Paulo prega com sabedoria de palavras para convencer os sabios.', 'Paulo prega com sabedoria de palavras.', 0, '1 Corintios 2:1 - nao com sabedoria de palavras'),
        mc('Em que se tornou Cristo para nos pela sabedoria de Deus?', ['Sacerdote','Profeta','Justica, santificacao e redencao','Rei'], 2, '1 Corintios 1:30'),
    ]),
    ('1 Coríntios 6: O Corpo é Templo', 'Paulo condena a imoralidade sexual e lembra que o corpo do crente é templo do Espírito Santo. Fomos comprados por preço: glorifiquemos a Deus no corpo.', '1 Corintios 6:12-20', 'Cuidar do corpo como templo do Espírito Santo', 'O corpo não é para a imoralidade, mas para glorificar a Deus. Somos templos do Espírito.', [
        mc('O que e o corpo do crente?', ['Irrelevante','Templo do Espirito Santo','Prisao','Maquina'], 1, '1 Corintios 6:19 - o vosso corpo e templo'),
        vf('Podemos fazer o que quisermos com nosso corpo.', 'Podemos fazer o que quisermos com nosso corpo.', 0, 'Nao tudo e lícito - 1 Corintios 6:12'),
        mc('Por que devemos glorificar a Deus no corpo?', ['Por obrigacao','Porque fomos comprados por preco','Para ganhar dinheiro','Por medo'], 1, '1 Corintios 6:20 - fostes comprados por preco'),
    ]),
    ('1 Coríntios 13: O Capítulo do Amor', 'Sem amor, nada temos. O amor é paciente, bondoso, não se irrita, não busca seus interesses. A fé, a esperança e o amor permanecem, mas o maior é o amor.', '1 Corintios 13:1-13', 'Entender a centralidade do amor na vida cristã', 'O amor é o mais excelente caminho. Sem ele, todos os dons e sacrifícios são vãos.', [
        mc('Qual e a primeira caracteristica do amor mencionada?', ['Poderoso','Paciente','Bondoso','Esperto'], 1, '1 Corintios 13:4 - o amor e paciente, e bondoso'),
        vf('O amor busca seus proprios interesses.', 'O amor busca seus proprios interesses.', 0, 'O amor nao busca seus interesses - 1 Corintios 13:5'),
        mc('Qual dos tres permanece?', ['Fe','Esperanca','Amor','Todas'], 3, '1 Corintios 13:13 - permanecem a fe, a esperanca e o amor'),
    ]),
    ('1 Coríntios 15: A Ressurreição', 'Paulo recorda que Cristo ressuscitou e apareceu a mais de 500 irmãos. Se Cristo não ressuscitou, a fé é vã. Mas Cristo é a primícia dos que dormem.', '1 Corintios 15:1-58', 'Firmar a fé na ressurreição de Cristo e na nossa', 'A ressurreição de Cristo é o fundamento da fé cristã. Sem ela, não há esperança.', [
        mc('A quem Cristo apareceu apos ressuscitar?', ['A ninguem','A mais de 500 pessoas','A Pedro apenas','A Paulo apenas'], 1, '1 Corintios 15:6 - apareceu a mais de quinhentos'),
        vf('Se Cristo nao ressuscitou, a fe cristã ainda e valida.', 'Se Cristo nao ressuscitou, a fe e valida.', 0, 'A fe seria va - 1 Corintios 15:17'),
        mc('Cristo e chamado de:', ['O primeiro dos mortos','O ultimo dos viventes','O primogenito dos mortos','A primicia dos que dormem'], 3, '1 Corintios 15:20 - primicia dos que dormem'),
    ]),
    ('2 Coríntios 4: Tesouros de Barro', 'Paulo compara o ministério a tesouros em vasos de barro. Sofremos, mas não desanimamos. O poder é de Deus, não de nós. O homem exterior perece, mas o interior se renova.', '2 Corintios 4:7-18', 'Valorizar o tesouro do evangelho em vasos frágeis', 'Nossa fragilidade mostra o poder de Deus. As aflições são leves comparadas à glória eterna.', [
        mc('Onde estao os tesouros?', ['No ceu','Em vasos de barro','Na igreja','Na Biblia'], 1, '2 Corintios 4:7 - em vasos de barro'),
        vf('Paulo desanimou por causa das tribulacoes.', 'Paulo desanimou por causa das tribulacoes.', 0, 'Nao desanimamos - 2 Corintios 4:16'),
        mc('O que se renova dia apos dia?', ['O corpo','O espirito','O mundo','O governo'], 1, 'O homem interior se renova dia apos dia'),
    ]),
    ('2 Coríntios 12: Graça Suficiente', 'Paulo pede que o espinho na carne seja removido, mas Deus responde: "Minha graça te basta, porque o meu poder se aperfeiçoa na fraqueza." Paulo se gloria nas fraquezas.', '2 Corintios 12:1-10', 'Confiar na graça suficiente de Deus nas fraquezas', 'Deus permite fraquezas para que Seu poder se manifeste. A graça de Deus é sempre suficiente.', [
        mc('O que Deus diz sobre a graça?', ['E insuficiente','E temporaria','Te basta','Nao existe'], 2, 'Minha graça te basta'),
        vf('Paulo orgulhava-se de suas forcas pessoais.', 'Paulo orgulhava-se de suas forcas.', 0, 'Glória-se nas fraquezas - 2 Corintios 12:9'),
        mc('O poder de Deus se aperfeicoa na:', ['Riqueza','Forca','Fraqueza','Sabedoria'], 2, 'O poder se aperfeicoa na fraqueza'),
    ]),
    ('Gálatas 2: Justificação pela Fé', 'Paulo confrontou Pedro por se separar dos gentios por medo. A justificação não vem pelas obras da Lei, mas pela fé em Cristo. Cristo morreu pelo pecado dos injustos.', 'Galatas 2:15-21', 'Firmar a justificação pela fé, não pelas obras da Lei', 'A obra da Lei não justifica. Somente a fé em Cristo nos declara justos diante de Deus.', [
        mc('Por que Paulo confrontou Pedro?', ['Por financas','Por se separar dos gentios','Por nao pregar','Por pecar'], 1, 'Galatas 2:11 - porque estava condenavel'),
        vf('As obras da Lei sao necessarias para a salvacao.', 'As obras da Lei sao necessarias para a salvacao.', 0, 'Somos justificados pela fe, nao pelas obras da Lei'),
        mc('Cristo morreu por:', ['Os justos','Os bons','Os injustos','Os perfeitos'], 2, 'Galatas 2:20 - pelos pecadores'),
    ]),
    ('Gálatas 3: Filhos de Deus pela Fé', 'Todos que são de Cristo foram batizados nele e são descendência de Abraão. Não há nem grego nem judeu. A promessa veio pela fé, não pela Lei.', 'Galatas 3:23-29', 'Entender que somos filhos de Deus pela fé em Cristo', 'Em Cristo, todos são um. A distinção entre judeu e gentio, escravo e livre, homem e mulher, é superada pela fé.', [
        mc('Quem sao herdeiros da promessa?', ['Apenas judeus','Apenas gregos','Todos os de Cristo','Apenas sacerdotes'], 2, 'Galatas 3:29 - se sois de Cristo, sois descendencia de Abraao'),
        vf('A Lei foi dada antes da promessa.', 'A Lei foi dada antes da promessa.', 0, 'A promessa veio primeiro - Galatas 3:17'),
        mc('Em Cristo, nao ha:', ['Pecado','Morte','Distincao entre judeu e grego','Deus'], 2, 'Galatas 3:28 - nao ha judeu nem grego'),
    ]),
    ('Gálatas 4: Libertados', 'Enquanto éramos meninos, estávamos sob servidão, mas Deus enviou o Seu Filho para resgatar os que estavam sob a Lei, para que recebêssemos a adoção.', 'Galatas 4:1-7', 'Compreender a liberdade que temos em Cristo', 'Deus nos libertou da escravidão da Lei para vivermos como filhos amados, guiados pelo Espírito.', [
        mc('O que Deus enviou para nos libertar?', ['Um anjo','Um profeta','O Seu Filho','Um livro'], 2, 'Galatas 4:4 - Deus enviou o Seu Filho'),
        vf('Ainda somos escravos da Lei em Cristo.', 'Ainda somos escravos da Lei em Cristo.', 0, 'Fomos libertados - Galatas 4:7'),
        mc('Chamamos a Deus de:', ['Juiz','Senhor','Pai','Rei'], 2, 'Galatas 4:6 - Abba, Pai'),
    ]),
    ('Gálatas 5: O Fruto do Espírito', 'Cristo nos libertou para a liberdade. Andai no Espírito, e não satisfareis os desejos da carne. O fruto do Espírito é amor, gozo, paz, mansidão, bondade, fé, temperança.', 'Galatas 5:16-26', 'Cultivar o fruto do Espírito na vida diária', 'A vida no Espírito se manifesta em fruto, não em obras da carne. A liberdade é para servir pelo amor.', [
        mc('Qual e o primeiro fruto do Espirito mencionado?', ['Poder','Riqueza','Amor','Sabedoria'], 2, 'Galatas 5:22 - amor'),
        vf('A liberdade cristã significa fazer o que a carne quer.', 'A liberdade cristã significa fazer o que a carne quer.', 0, 'Libertados para servir pelo amor - Galatas 5:13'),
        mc('Quantos frutos sao listados?', ['5','7','9','12'], 2, '9 frutos do Espirito'),
        mc('Contra esses frutos nao ha Lei:', ['Verdade','Falso','Depende','As vezes'], 0, 'Galatas 5:23 - contra esses nao ha Lei'),
    ]),
], 50)
print("  Trilha 9 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 10 - Efesios, Filipenses, Colossenses
# ═══════════════════════════════════════════════
t10 = mk_trilha('Efesios, Filipenses, Colossenses', 'As epistolas prisionais de Paulo sobre a riqueza da graça, a humildade de Cristo e a supremacia dEle sobre todas as coisas', 'adulto', 'intermediario', 10, 'emoji_people')
add_licoes(t10, [
    ('Efésios 1: Abençoados com Toda Bênção', 'Deus nos abençoou com todas as bênçãos espirituais nos lugares celestiais em Cristo. Ele nos escolheu antes da fundação do mundo, predestinando-nos para filhos adotivos.', 'Efesios 1:3-14', 'Reconhecer as bênçãos espirituais que temos em Cristo', 'Deus nos abençoou abundantemente e espiritualmente em Cristo, com escolha, adoção, redenção e selamento.', [
        mc('Onde somos abencoados?', ['Na terra','Nos lugares celestiais em Cristo','Na igreja','No ceu apenas'], 1, 'Efesios 1:3 - nos lugares celestiais em Cristo'),
        vf('Deus nos escolheu depois que nascemos.', 'Deus nos escolheu depois que nascemos.', 0, 'Antes da fundacao do mundo - Efesios 1:4'),
        mc('O que Deus fez conosco em amor?', ['Destruir','Perdoar','Predestinar para filhos adotivos','Esquecer'], 2, 'Efesios 1:5 - predestinou-nos para adocao'),
    ]),
    ('Efésios 2: Salvos pela Graça', 'Éramos mortos em pecados, mas Deus nos vivificou com Cristo. Somos salvos pela graça, mediante a fé, não por obras. Somos feitura de Deus, criados para boas obras.', 'Efesios 2:1-10', 'Entender que somos vivificados e salvos pela graça de Deus', 'Deus nos tirou da morte espiritual, nos sentou com Cristo, e nos criou para boas obras.', [
        mc('O que eramos antes de Cristo?', ['Vivos','Mortos em pecados','Sabios','Pobres'], 1, 'Efesios 2:1 - mortos em pecados'),
        vf('Somos salvos pelas nossas boas obras.', 'Somos salvos pelas nossas boas obras.', 0, 'Pela graça, mediante a fe - Efesios 2:8'),
        mc('Para que fomos criados?', ['Para pecar','Para boas obras','Para julgar','Para sofrer'], 1, 'Efesios 2:10 - criados em Cristo para boas obras'),
    ]),
    ('Efésios 3: O Amor Infinito de Cristo', 'Paulo ora para que os efésios compreendam o amor de Cristo, que excede todo conhecimento. Para aquele que pode fazer infinitamente mais, glória na igreja.', 'Efesios 3:14-21', 'Experimentar o amor de Cristo que excede todo conhecimento', 'O amor de Cristo é imensurável, e Deus pode fazer muito mais do que pedimos ou pensamos.', [
        mc('O que Paulo ora para que os efesios compreendam?', ['A Lei','O amor de Cristo','As profecias','O pecado'], 1, 'Efesios 3:19 - o amor de Cristo'),
        vf('O amor de Cristo e limitado ao que podemos medir.', 'O amor de Cristo e limitado.', 0, 'Excede todo conhecimento - Efesios 3:19'),
        mc('Deus pode fazer mais do que:', ['O que pedimos','O que pensamos','Ambos','Nada'], 2, 'Efesios 3:20 - infinitamente mais'),
    ]),
    ('Efésios 4: A Unidade do Espírito', 'Paulo exorta à unidade da fé e do conhecimento do Filho de Deus. Cada membro do corpo de Cristo tem uma função. A verdade em amor faz crescer em Cristo.', 'Efesios 4:1-16', 'Buscar a unidade na diversidade de dons', 'A igreja é um corpo com muitos membros. A verdade em amor promove o crescimento.', [
        mc('Quantos ha?', ['Um batismo','Um Senhor','Uma fe','Todos anteriores'], 3, 'Efesios 4:5 - um Senhor, uma fe, um batismo'),
        vf('A verdade deve ser dita sem amor para ser eficaz.', 'A verdade deve ser dita sem amor.', 0, 'A verdade em amor - Efesios 4:15'),
        mc('O que cada membro do corpo faz?', ['Nada','O mesmo que os outros','Sua parte especifica','Tudo sozinho'], 2, 'Efesios 4:16 - cada membro contribui'),
    ]),
    ('Efésios 6: A Armadura de Deus', 'Veste a armadura de Deus para resistir às ciladas do diabo. Cinto da verdade, couraça da justiça, escudo da fé, capacete da salvação, espada do Espírito e oração.', 'Efesios 6:10-20', 'Vestir-se diariamente com a armadura de Deus', 'A guerra espiritual é real. Deus fornece toda a armadura necessária para resistir ao inimigo.', [
        mc('Qual e o escudo da fe?', ['O batismo','A oracao','Apagar todas as setas do maligno','A Biblia'], 2, 'Efesios 6:16 - apagar todas as setas do maligno'),
        vf('A espada do Espirito e a oracao.', 'A espada do Espirito e a oracao.', 0, 'A espada e a Palavra de Deus'),
        mc('O que devemos fazer em toda oracao?', ['Pedir riquezas','Orar sempre','Cantar','Dormir'], 1, 'Efesios 6:18 - orando em todo tempo no Espirito'),
        mc('O capacete da salvacao e:', ['O conhecimento','A fe em Cristo','A forca','O poder'], 1, 'O capacete e a salvacao pela fe em Cristo'),
    ]),
    ('Filipenses 1: Alegria na Prisão', 'Preso em Roma, Paulo escreve com alegria. O que importa é que Cristo seja anunciado. Para mim viver é Cristo, e morrer é ganho. Ele está confiante que será liberto.', 'Filipenses 1:12-26', 'Cultivar alegria independentemente das circunstâncias', 'Mesmo na prisão, Paulo tinha alegria porque Cristo era anunciado. A sua prioridade era Cristo.', [
        mc('Onde Paulo escreveu esta epistola?', ['Em Jerusalem','Na prisao em Roma','Em Corinto','Em Efeso'], 1, 'Filipenses 1:13 - na corte do pretor'),
        vf('Paulo era triste na prisao.', 'Paulo era triste na prisao.', 0, 'Tinha alegria porque Cristo era anunciado'),
        mc('Para Paulo, viver e:', ['Riqueza','Fama','Cristo','Poder'], 2, 'Filipenses 1:21 - para mim viver e Cristo'),
    ]),
    ('Filipenses 2: A Humildade de Cristo', 'Cristo, sendo em forma de Deus, não teve por usurpação ser igual a Deus, mas esvaziou-se, tomando a forma de servo. Deus o exaltou e lhe deu o nome acima de todo nome.', 'Filipenses 2:5-11', 'Imitar a humildade de Cristo em nossa vida', 'A humildade de Cristo é o exemplo supremo. Ele se humilhou até a morte na cruz, e Deus o exaltou.', [
        mc('O que Cristo nao teve por usurpacao?', ['Ser servo','Ser igual a Deus','Ser pobre','Ser rei'], 1, 'Filipenses 2:6 - ser igual a Deus'),
        vf('Cristo veio para ser servido.', 'Cristo veio para ser servido.', 0, 'Veio para servir - Filipenses 2:7'),
        mc('Que nome Deus deu a Cristo?', ['Profeta','Sacerdote','Rei','O nome acima de todo nome'], 3, 'Filipenses 2:9 - o nome que e sobre todo nome'),
    ]),
    ('Filipenses 4: Posso Todas as Coisas', 'Paulo aprendeu a contentar-se em toda situação. O segredo é a força de Cristo. E o Deus da paz estará convosco. Fixai o pensamento no que é verdadeiro, justo e louvável.', 'Filipenses 4:4-13', 'Aprender o segredo do contentamento em Cristo', 'O contentamento não depende das circunstâncias, mas da força que Cristo dá.', [
        mc('O segredo de Paulo e:', ['Ter muito dinheiro','Poder todas as coisas por meio dAquele que me fortalece','Ser perfeito','Nao dormir'], 1, 'Filipenses 4:13'),
        vf('Paulo aprendeu a ser contente apenas em prosperidade.', 'Paulo era contente apenas em prosperidade.', 0, 'Em toda e qualquer situacao - Filipenses 4:12'),
        mc('O que devemos fixar no pensamento?', ['O mal','O pecado','O que e verdadeiro e justo','O mundo'], 2, 'Filipenses 4:8 - pensai nas coisas verdadeiras'),
    ]),
    ('Colossenses 1: A Supremacia de Cristo', 'Cristo é a imagem do Deus invisível, o primogênito de toda criação. Por Ele foram criadas todas as coisas. Ele é a cabeça da igreja e o primeiro dos que ressuscitaram dos mortos.', 'Colossenses 1:15-20', 'Reconhecer a supremacia absoluta de Cristo sobre toda a criação', 'Cristo é soberano sobre toda a criação, a igreja, e todas as coisas são sustentadas por Ele.', [
        mc('Cristo e a imagem de:', ['Moises','O Deus invisivel','Os anjos','Abraao'], 1, 'Colossenses 1:15 - a imagem do Deus invisivel'),
        vf('Todas as coisas foram criadas sem Cristo.', 'Todas as coisas foram criadas sem Cristo.', 0, 'Todas as coisas foram criadas por Ele e para Ele - Colossenses 1:16'),
        mc('Quem e a cabeca da igreja?', ['Paulo','Pedro','Cristo','Deus Pai'], 2, 'Colossenses 1:18 - Ele e a cabeca do corpo, da igreja'),
    ]),
    ('Colossenses 3: Vida Nova', 'Busquei as coisas lá de cima. Revesti-vos do homem novo, renovado para o conhecimento, segundo a imagem do Criador. Deixai de lado a velha vida e vivei em Cristo.', 'Colossenses 3:1-17', 'Viver a vida nova em Cristo, mortos para o pecado', 'A vida cristã prática envolve deixar o velho homem, vestir o novo e viver em amor e sabedoria.', [
        mc('O que devemos buscar?', ['A terra','As coisas la de cima','O poder','A fama'], 1, 'Colossenses 3:1 - buscai as coisas la de cima'),
        vf('Devemos guardar a velha vida em Cristo.', 'Devemos guardar a velha vida em Cristo.', 0, 'Mortos com Cristo - Colossenses 3:3'),
        mc('O que devemos vestir?', ['Armadura de guerra','O homem novo','Roupas caras','Uniformes'], 1, 'O homem novo, renovado - Colossenses 3:10'),
    ]),
], 50)
print("  Trilha 10 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 11 - Tessalonicenses e Pastorais
# ═══════════════════════════════════════════════
t11 = mk_trilha('Tessalonicenses e Pastorais', 'Paulo instrui a igreja sobre a vinda de Cristo, conduta cristã e qualificacoes para lideres da igreja', 'adulto', 'intermediario', 11, 'engineering')
add_licoes(t11, [
    ('1 Tessalonicenses 4: O Arrebatamento', 'Paulo instrui sobre a santidade e a vinda do Senhor. Os mortos em Cristo ressuscitarão primeiro, e depois nós, que ficarmos, seremos arrebatados juntamente com eles.', '1 Tessalonicenses 4:13-18', 'Entender a esperança do arrebatamento da igreja', 'Deus não quis que ficasseis ignorantes sobre os que dormem. Seremos arrebatados para estar com o Senhor.', [
        mc('O que acontecera com os mortos em Cristo?', ['Perderao tudo','Ressuscitarao primeiro','Ficaram no ceu','Desaparecerao'], 1, '1 Tessalonicenses 4:16 - os mortos em Cristo ressuscitarao primeiro'),
        vf('Devemos estar tristes por quem morreu em Cristo.', 'Devemos estar tristes por quem morreu em Cristo.', 0, 'Nao vos aflijais - 1 Tessalonicenses 4:13'),
        mc('Seremos arrebatados para:', ['Viver na terra','Estar com o Senhor','Morrer','Pecar'], 1, 'Assim estaremos sempre com o Senhor'),
    ]),
    ('1 Tessalonicenses 5: O Dia do Senhor', 'O dia do Senhor vem como um ladrão na noite. Somos filhos da luz, não da escuridão. Examinai tudo e guarda o que é bom. Orai sem cessar.', '1 Tessalonicenses 5:1-28', 'Viver preparados para a vinda do Senhor', 'O crente deve viver como filho da luz, vigilante, orando e rejubilando sempre.', [
        mc('Como vem o dia do Senhor?', ['Com aviso previo','Como um ladrao na noite','Em paz','Com festas'], 1, '1 Tessalonicenses 5:2 - vem como um ladrao na noite'),
        vf('Somos filhos da escuridao.', 'Somos filhos da escuridao.', 0, 'Somos filhos da luz - 1 Tessalonicenses 5:5'),
        mc('Segundo 1 Tessalonicenses 5:16-18, o que Paulo ordena que o crente faça continuamente?', ['Alegrar-se, orar e dar graças','Confiar somente nas próprias forças','Guardar rancor e buscar vingança','Evitar o sofrimento a todo custo'], 0, '1 Tessalonicenses 5:16-18 - alegrai-vos sempre, orai sem cessar, em tudo dai graças'),
    ]),
    ('2 Tessalonicenses 3: A Preguiça', 'Paulo ordena que os preguiçosos não comam. Aquele que não quer trabalhar, não coma. Não desanimem no bem. Não andem como inquietos.', '2 Tessalonicenses 3:6-15', 'Cultivar disciplina e trabalho na vida cristã', 'A fé produtiva e o trabalho honesto são parte da vida cristã. A preguiça desonra o evangelho.', [
        mc('O que Paulo diz ao preguicoso?', ['Que durma mais','Que coma bastante','Que nao coma','Que va embora'], 2, '2 Tessalonicenses 3:10 - aquele que nao quer trabalhar, nao coma'),
        vf('Paulo nunca trabalhou com as proprias maos.', 'Paulo nunca trabalhou com as proprias maos.', 0, 'Trabalhou de noite e de dia - 2 Tessalonicenses 3:8'),
        mc('Como devemos reagir quando desanimamos?', ['Desistir','Continuar no bem','Odiar','Fugir'], 1, 'Nao desanime no bem - 2 Tessalonicenses 3:13'),
    ]),
    ('1 Timóteo 2: Oração por Todos', 'Paulo pede que se façam intercessões, orações, ações de graça por todos os homens. Quer que se reze por reis e por todos os que estão em autoridade.', '1 Timoteo 2:1-8', 'Entender a importância da oração pela sociedade', 'A oração deve ser feita por todos os homens, sem ira nem disputas. Deus quer que todos sejam salvos.', [
        mc('Por quem devemos orar?', ['Apenas por crentes','Por todos os homens','Apenas por familias','Por inimigos apenas'], 1, '1 Timoteo 2:1 - oracoes por todos os homens'),
        vf('Deus nao quer que os lideres politicos sejam salvos.', 'Deus nao quer que os lideres sejam salvos.', 0, 'Deus quer que todos sejam salvos - 1 Timoteo 2:4'),
        mc('Como devemos orar?', ['Com raiva','Sem ira nem disputas','Com soberba','Rapidamente'], 1, '1 Timoteo 2:8 - sem ira nem disputas'),
    ]),
    ('1 Timóteo 3: Qualificações dos Líderes', 'Paulo lista qualificações para bispos e diáconos: irrepreensível, marido de uma só mulher, cheio do Espírito, apto a ensinar, não dado ao vinho.', '1 Timoteo 3:1-13', 'Reconhecer as qualificações bíblicas para líderes da igreja', 'A liderança na igreja exige integridade, sabedoria e santidade de vida.', [
        mc('Qual e uma qualificacao para bispo?', ['Ser rico','Irrepreensivel','Jovem','Celebridade'], 1, '1 Timoteo 3:2 - irrepreensivel'),
        vf('Um bispo pode ter muitas mulheres.', 'Um bispo pode ter muitas mulheres.', 0, 'Marido de uma so mulher - 1 Timoteo 3:2'),
        mc('Os diaconos devem ser:', ['Perfeitos','Cheios de fe e de verdade','Poderosos','Ricos'], 1, 'Cheios de fe e de verdade'),
    ]),
    ('1 Timóteo 4: Timóteo, Exemplo dos Fiéis', 'Paulo encoraja Timóteo a usar bem o seu dom, a se exercitar na piedade e a persistir no ensino. Deve ser modelo em palavra, conduta, amor, fé e castidade.', '1 Timoteo 4:6-16', 'Ser modelo de fé e conduta para os outros', 'O servo de Deus deve se exercitar na piedade, ser diligente no ensino e viver o que ensina.', [
        mc('O que Timoteo deve fazer?', ['Desistir','Ser modelo em conduta','Ocultar o evangelho','Ficar em casa'], 1, '1 Timoteo 4:12 - sejas modelo em palavra'),
        vf('A exercitacao corporal e mais importante que a piedade.', 'A exercitacao corporal e mais importante que a piedade.', 0, 'A piedade para tudo aproveita - 1 Timoteo 4:8'),
        mc('Timoteo deve ser diligent em:', ['Ganhar dinheiro','Ensinar e pregar','Viajar','Dormir'], 1, 'Diligent no teu ministerio'),
    ]),
    ('2 Timóteo 4: Combate o Bom Combate', 'Paulo, prestes a ser martirizado, encoraja Timóteo: prega a palavra, insta a tempo e fora de tempo, repreende, suplica. Combate o bom combate da fé.', '2 Timoteo 4:1-8', 'Ser corajoso e fiel no ministério até o fim', 'O crente deve persistir na verdade, mesmo quando muitos não suportarão a sã doutrina.', [
        mc('O que Paulo pede a Timoteo?', ['Fugir','Pregar a palavra sem desistir','Esconder a fe','Nao falar'], 1, '2 Timoteo 4:2 - prega a palavra, insta a tempo e fora de tempo'),
        vf('Paulo esperava receber a coroa da justica.', 'Paulo esperava receber a coroa da justica.', 1, '2 Timoteo 4:8 - esta guardada para mim a coroa'),
        mc('Muitos nao suportarao:', ['A riqueza','A sa doutrina','O louvor','A oracao'], 1, 'Nao suportarao a sa doutrina'),
    ]),
    ('Tito 2: A Graça que Salva', 'A graça de Deus apareceu, trazendo salvação a todos os homens. Ela nos ensina a negar a impiedade e viver de forma justa e sensata neste mundo.', 'Tito 2:11-14', 'Entender que a graça traz disciplina e salvação', 'A graça não é licença para pecar, mas a força para viver santo, aguardando a vinda de Cristo.', [
        mc('A graça de Deus apareceu para:', ['Apenas judeus','Apenas ricos','Todos os homens','Apenas lideres'], 2, 'Tito 2:11 - apareceu a todos os homens'),
        vf('A graça nos permite viver como quiseres.', 'A graça nos permite viver como quiseres.', 0, 'Nos ensina a negar a impiedade - Tito 2:12'),
        mc('O que estamos aguardando?', ['A morte','A vinda do Senhor','O fim do mundo','O Juizo Final'], 1, 'Aventura gloriosa do nosso grande Deus e Salvador'),
    ]),
    ('Tito 3: Obras Boas', 'Salvos não por obras de justiça que nós mesmos praticamos, mas pela Sua misericórdia. Entretanto, somos criados em Cristo para boas obras.', 'Tito 3:3-8', 'Viver em boas obras como fruto da salvação', 'A salvação é pela graça, mas o crente é chamado a praticar boas obras e ser produtivo.', [
        mc('Somos salvos por:', ['Obras de justica','A misericordia de Deus','Dinheiro','Fama'], 1, 'Salvos pela Sua misericordia - Tito 3:5'),
        vf('Obras boas sao necessarias para ser salvo.', 'Obras boas sao necessarias para ser salvo.', 0, 'Salvos pela graça, mas criados para boas obras'),
        mc('Para que fomos criados?', ['Para pecar','Para boas obras','Para julgar','Para sofrer'], 1, 'Criados em Cristo para boas obras'),
    ]),
    ('Filemom: Perdão', 'Onésimo, escravo de Filemom, fugiu e converteu-se pelo ministério de Paulo. Paulo pede a Filemom que receba de volta Onésimo não como escravo, mas como irmão amado.', 'Filemon 1:1-25', 'Praticar o perdão e a reconciliação entre irmãos na fé', 'O evangelho transforma relações humanas. Em Cristo, não há escravo nem livre.', [
        mc('Quem era Onesimo?', ['Um sacerdote','Um escravo de Filemon','Um romano','Um judeu'], 1, 'Onesimo era escravo de Filemon'),
        vf('Paulo pede que Filemon mate Onesimo.', 'Paulo pede que Filemon mate Onesimo.', 0, 'Paulo pede que o receba de volta como irmao amado'),
        mc('Como Paulo pede que Filemon receba Onesimo?', ['Como escravo','Como inimigo','Como irmao amado','Como estranho'], 2, 'Recebe como irmao amado'),
    ]),
], 50)
print("  Trilha 11 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 12 - Hebreus: Cristo Superior
# ═══════════════════════════════════════════════
t12 = mk_trilha('Hebreus: Cristo Superior', 'A epistola que demonstra a superioridade absoluta de Cristo sobre anjos, Moises, a Lei, os sacerdotes e toda a aliança anterior', 'adulto', 'avancado', 12, 'vertical_align_top')
add_licoes(t12, [
    ('Hebreus 1: O Filho Revelado', 'Deus falou por muitos modos, mas agora nos falou pelo Seu Filho. Cristo é a imagem exata do Deus invisível, sustentando todas as coisas pela palavra do Seu poder.', 'Hebreus 1:1-4', 'Reconhecer que Cristo é a revelação suprema de Deus', 'Cristo supera todos os profetas e anjos. Ele é o Filho, herdador de todas as coisas.', [
        mc('Como Deus falou nos ultimos tempos?', ['Por anjos','Por profetas','Pelo Seu Filho','Por sonhos'], 2, 'Hebreus 1:2 - nos falou pelo Seu Filho'),
        vf('Cristo e inferior aos anjos.', 'Cristo e inferior aos anjos.', 0, 'Cristo e superior a todo anjo'),
        mc('Cristo sustenta todas as coisas:', ['Com as maos','Com poder politico','Pela palavra do Seu poder','Com ajuda humana'], 2, 'Hebreus 1:3 - sustenta todas as coisas pela palavra do Seu poder'),
    ]),
    ('Hebreus 2: Um Pouco Menor', 'Por um tempo, Cristo ficou um pouco menor que os anjos para sofrer a morte e coroar-nos de graça e honra. Assim tornou-se autor da salvação eterna.', 'Hebreus 2:5-18', 'Entender o sofrimento voluntário de Cristo por nós', 'Cristo se humilhou temporariamente para nos trazer a salvação e ser nosso sumo sacerdote misericordioso.', [
        mc('Por que Cristo ficou um pouco menor?', ['Por pecado','Para sofrer a morte por nos','Por fraqueza','Por maldade'], 1, 'Para sofrer a morte pela graça de Deus'),
        vf('Cristo se tornou sumo sacerdote para sempre.', 'Cristo se tornou sumo sacerdote para sempre.', 1, 'Hebreus 2:10 - autor da salvacao eterna'),
        mc('Cristo e nosso:', ['Inimigo','Juiz cruel','Irmão e sumo sacerdote','Nada'], 2, 'Fez-se irmao dos homens'),
    ]),
    ('Hebreus 3: Jesus Superior a Moisés', 'Jesus é digno de maior glória que Moisés, assim como o construtor é maior que a casa. Moisés servo, mas Cristo Filho sobre a casa.', 'Hebreus 3:1-6', 'Reconhecer que Cristo é superior até mesmo a Moisés', 'Moisés foi fiel como servo, mas Cristo é fiel como Filho sobre toda a casa de Deus.', [
        mc('Cristo e superior a Moises porque:', ['E mais antigo','E Filho sobre a casa','E mais forte','E mais rico'], 1, 'Hebreus 3:6 - Cristo e Filho sobre a casa'),
        vf('Moises era mais importante que Cristo.', 'Moises era mais importante que Cristo.', 0, 'Jesus e digno de maior gloria que Moises'),
        mc('Quem construiu a casa?', ['Moises','Deus Pai','Cristo','Abraao'], 2, 'Cristo e o construtor de tudo'),
    ]),
    ('Hebreus 4: Entrando no Descanso', 'Deus preparou um descanso para o Seu povo. Não endureçais os vossos corações. A Palavra de Deus é viva e eficaz, penetrante até dividir espírito e alma.', 'Hebreus 4:1-16', 'Buscar o descanso que Deus oferece pela fé', 'Há um descanso espiritual para os que creem. A Palavra de Deus é cortante e penetrante.', [
        mc('Deus preparou:', ['Um castigo','Um descanso','Um carcere','Um palacio'], 1, 'Hebreus 4:9 - ha um descanso para o povo de Deus'),
        vf('A Palavra de Deus e morta e ineficaz.', 'A Palavra de Deus e morta e ineficaz.', 0, 'Viva e eficaz - Hebreus 4:12'),
        mc('A Palavra de Deus penetra ate:', ['O corpo','A alma e o espirito','A mente apenas','O coracao apenas'], 1, 'Hebreus 4:12 - dividir alma e espirito'),
    ]),
    ('Hebreus 5-6: O Sumo Sacerdote', 'Cristo se tornou sumo sacerdote para sempre, segundo a ordem de Melquisedeque. Perseverarei na fé e no ensino, não caindo de novo no arrependimento.', 'Hebreus 5:10-6:12', 'Firmar a fé e não cair para trás', 'A perseverança é fundamental. Cristo é nosso sumo sacerdote eterno, capaz de compadecer-se.', [
        mc('Cristo e sumo sacerdote segundo a ordem de:', ['Aaron','Levi','Melquisedeque','Davi'], 2, 'Hebreus 5:10 - segundo a ordem de Melquisedeque'),
        vf('Podemos cair da graça e nao termos voltada.', 'Podemos cair e nao termos volta.', 0, 'Hebreus 6:4-6 - fala da gravidade da queda'),
        mc('O que devemos fazer quanto a fe?', ['Abandonar','Perseverar','Trocar','Esquecer'], 1, 'Aperseverai na fe'),
    ]),
    ('Hebreus 7: A Melhor Aliança', 'Melquisedeque, rei de Salém, sacerdote do Deus Altíssimo, abençoou Abraão. Cristo é sumo sacerdote eterno segundo essa ordem, estabelecendo melhor aliança.', 'Hebreus 7:1-28', 'Entender por que a aliança de Cristo é melhor', 'O sacerdócio de Melquisedeque é eterno e superior ao de Arão. A aliança de Cristo é melhor e irrevogável.', [
        mc('Quem abencoa Abraao?', ['Moises','Aaron','Melquisedeque','Davi'], 2, 'Hebreus 7:1-2 - Melquisedeque abencoa Abraao'),
        vf('A aliança antiga era melhor que a nova.', 'A aliança antiga era melhor que a nova.', 0, 'Cristo e fiel - melhor aliança'),
        mc('Cristo e sumo sacerdote:', ['Temporario','Segundo a Lei de Aaron','Eterno, segundo Melquisedeque','Nao e sacerdote'], 2, 'Hebreus 7:24 - eterno e imutavel'),
    ]),
    ('Hebreus 9: O Sangue Definitivo', 'O sangue de bodes e bezerros não pode remover pecados. Cristo entrou no santo dos santos com o seu próprio sangue, oferecendo-se uma vez por todas.', 'Hebreus 9:11-28', 'Reconhecer que o sangue de Cristo é definitivo e suficiente', 'O sangue de Cristo é mais precioso e eficaz que qualquer sacrifício antigo. Uma vez, bastou.', [
        mc('O sangue de Cristo e melhor que:', ['O ouro','Os animais do sacrificio','A Lei','Os anjos'], 1, 'Sangue de animais nao remove pecados'),
        vf('Deus precisa de sacrificios repetidos.', 'Deus precisa de sacrificios repetidos.', 0, 'Cristo se offerceu uma vez por todas'),
        mc('Cristo entrou no:', ['Templo de Salomao','Sancto sanctos do ceu','Tabernaculo terrestre','Nao entrou em lugar nenhum'], 1, 'No sancto sanctos do ceu'),
    ]),
    ('Hebreus 10: O Sacrifício Único', 'É impossível que sangue de touros e bodes tire pecados. Quando Cristo se ofereceu, acabou o pecado para sempre. Entremos com confiança ao trono da graça.', 'Hebreus 10:1-23', 'Ter confiança no sacrifício único e perfeito de Cristo', 'O sacrifício de Cristo é único e perfeito. Podemos ter certeza da nossa salvação nele.', [
        mc('O sacrificio de Cristo foi:', ['Temporario','Unico e perfeito','Insuficiente','Animado'], 1, 'Uma vez por todas, perfeito'),
        vf('Precisamos continuar oferecendo sacrificios por pecados.', 'Precisamos continuar oferecendo sacrificios por pecados.', 0, 'Cristo acabou com o pecado para sempre'),
        mc('Devemos entrar com confianca ao:', ['Trono do diabo','Trono da graça','Trono do imperador','Trono de julgamento'], 1, 'Trono da graça - Hebreus 10:19'),
    ]),
    ('Hebreus 11: A Fé', 'A fé é a certeza daquilo que esperamos e a prova das coisas que não vemos. Abraão, Moisés, Raabe e muitos outros viveram pela fé e não receberam a promessa completa.', 'Hebreus 11:1-40', 'Cultivar uma fé firme e inabalável', 'Fé é agir com base na palavra de Deus, mesmo não vendo. O exemplo dos antigos nos encoraja.', [
        mc('O que e a fe?', ['Certeza de que e verdade','Conhecimento por experiencia','Acertar no jogo','Pensar positivo'], 0, 'Hebreus 11:1 - certeza daquilo que esperamos'),
        vf('Abraao recebeu todas as promessas na terra.', 'Abraao recebeu todas as promessas na terra.', 0, 'Viveu como forasteiro, sem receber a heranca completa'),
        mc('Quem mais e mencionado?', ['Noe','Abraao','Raabe','Todos anteriores'], 3, 'Muitos heros da fe sao mencionados'),
    ]),
    ('Hebreus 12: A Corrida da Fé', 'Nossa fé é cercada por tão grande nuvem de testemunhas. Corramos com perseverança a carreira que temos diante de nós, olhando para Jesus, autor e consumador da fé.', 'Hebreus 12:1-29', 'Correr com perseverança a carreira da fé', 'Os antigos nos cercam. Cristo é nosso exemplo e objetivo. Não nos cansemos de seguir o caminho.', [
        mc('O que nos cerca?', ['Duvidas','Tao grande nuvem de testemunhas','Inimigos','Maldicoes'], 1, 'Hebreus 12:1 - tao grande nuvem de testemunhas'),
        vf('Devemos parar quando encontrarmos dificuldades.', 'Devemos parar quando encontrarmos dificuldades.', 0, 'Corramos com perseveranca'),
        mc('Em quem devemos olhar?', ['Para nos mesmos','Para Jesus','Para o mundo','Para o diabo'], 1, 'Olhando para Jesus, autor e consumador da fe'),
    ]),
], 50)
print("  Trilha 12 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 13 - Tiago e Pedro: Fe em Acao
# ═══════════════════════════════════════════════
t13 = mk_trilha('Tiago e Pedro: Fe em Acao', 'Ensinamentos praticos sobre como a fe se expressa em obras, palavras e amor ao proximo na vida cotidiana', 'adulto', 'intermediario', 13, 'thumb_up')
add_licoes(t13, [
    ('Tiago 1: Provações', 'Considerai pura a alegria quando entrais em provações de muitas sortes, porque a fé, provada, produz perseverança. Se falta sabedoria, peça a Deus.', 'Tiago 1:2-12', 'Encontrar propósito nas provações da vida', 'As provações produzem perseverança, que produz maturidade. Deus dá sabedoria liberalmente a quem pede.', [
        mc('O que tiago diz sobre provacoes?', ['Sa ruins','Considerai alegria','Nao servem pra nada','Devemos fugir'], 1, 'Considerai pura a alegria quando entrais em provacoes'),
        vf('Devemos pedir sabedoria com duvidas.', 'Devemos pedir sabedoria com duvidas.', 0, 'De sem duvidas - Tiago 1:6'),
        mc('A fe provada produz:', ['Pecado','Perseveranca','Medo','Desespero'], 1, 'A fe provada produz perseveranca'),
    ]),
    ('Tiago 2: Fé sem Obras', 'Se alguém diz que tem fé e não tem obras, que lhe aproveita? A fé sem obras é morta. Abraão foi justificado pelas obras quando ofereceu Isaque.', 'Tiago 2:14-26', 'Entender que a fé genuína produz obras', 'A fé verdadeira se demonstra por ações. Fé e obras caminham juntas na vida do crente.', [
        mc('Fe sem obras e:', ['Valiosa','Morta','Grande','Suficiente'], 1, 'Tiago 2:17 - a fe, se nao tiver obras, e morta'),
        vf('Somos justificados somente pela fe, e nao pelas obras.', 'Somos justificados somente pela fe, e nao pelas obras.', 1, 'Romanos 3:28 e Efesios 2:8-9 - pela fe, nao por obras'),
        mc('Quem foi justificado pelas obras?', ['Moises','Abel','Abraao','Noe'], 2, 'Abraao foi justificado quando ofereceu Isaque'),
    ]),
    ('Tiago 3: A Língua', 'A língua é um pequeno membro, mas faz grandes estragos. Ninguém pode domar a língua. Ela é um mundo de maldade, cheia de veneno mortal.', 'Tiago 3:1-12', 'Aprender a controlar a própria língua', 'A língua pode destruir ou construir. O crente deve ser cuidadoso com suas palavras.', [
        mc('O que e a lingua?', ['Irrelevante','Pequena mas poderosa','Inofensiva','Sem efeito'], 1, 'Pequena membro, mas faz grandes estragos'),
        vf('E facil controlar a lingua.', 'E facil controlar a lingua.', 0, 'Ninguem pode domar a lingua'),
        mc('O que a lingua pode fazer?', ['Apenas palavras boas','Nada','Apenas palavras ruins','Construir e destruir'], 3, 'Pode construir e destruir vidas'),
    ]),
    ('Tiago 4: Humildade', 'Resisti ao diabo, e fugirá de vós. Aproximai-vos de Deus, e Ele se aproximará de vós. Não vanglorieis de amanhã. Humilhai-vos diante do Senhor, e vos exaltará.', 'Tiago 4:1-10', 'Viver em humildade diante de Deus e dos outros', 'A soberba leva à queda. A humildade atrai a exaltação divina. Proximidade com Deus e consequência de humildade.', [
        mc('O que devemos resistir?', ['A oracao','A verdade','O diabo','A bondade'], 2, 'Resisti ao diabo, e fugira'),
        vf('Deus resiste aos humildes.', 'Deus resiste aos humildes.', 0, 'Deus resiste aos soberbos - Tiago 4:6'),
        mc('Quando Deus nos exaltara?', ['Agora','Nunca','Quando nos humilharmos','Se ganharmos dinheiro'], 2, 'Humilhai-vos diante do Senhor'),
    ]),
    ('Tiago 5: A Oração dos Justos', 'A oração é muito eficaz. Elias era homem sujeito às mesmas paixões que nós, mas orou e não choveu por três anos. Confessai as vossas culpas uns aos outros e orai.', 'Tiago 5:13-18', 'Valorizar o poder da oração no ministério', 'A oração é poderosa e eficaz. Os justos devem orar uns pelos outros.', [
        mc('A oracao dos justos e:', ['Inutil','Muito eficaz','Insuficiente','Perigosa'], 1, 'Tiago 5:16 - e muito eficaz'),
        vf('Elias nunca teve problemas.', 'Elias nunca teve problemas.', 0, 'Era homem sujeito as mesmas paixoes que nos'),
        mc('O que devemos fazer uns aos outros?', ['Odiar','Confessar culpas e orar','Julgar','Ignorar'], 1, 'Confessai as vossas culpas e orai'),
    ]),
    ('1 Pedro 1: Viva Esperança', 'Nascemos de novo pela palavra viva e eterna de Deus. Nossa fé, mais preciosa que o ouro provado pelo fogo, resulta em louvor, glória e honra.', '1 Pedro 1:3-9', 'Cultivar uma viva esperança na redenção', 'A herança é incorruptível. Nossa fé, provada pelo fogo, é mais preciosa que o ouro.', [
        mc('De que nascemos de novo?', ['De agua','Da palavra viva de Deus','De sangue','De energia'], 1, 'Pela palavra viva e eterna de Deus'),
        vf('Nossa fe e menos importante que o ouro.', 'Nossa fe e menos importante que o ouro.', 0, 'Mais preciosa que o ouro provado pelo fogo'),
        mc('A heranca dos santos e:', ['Corruptivel','Incorruptivel','Temporaria','Nula'], 1, 'Incorruptivel, reservada no ceu'),
    ]),
    ('1 Pedro 2: Pedras Vivas', 'Vos mesmos, como pedras vivas, sede edificados espiritualmente em casa sacerdotal. Cristo é a pedra angular, a pedra de esquina, a pedra do tropeço.', '1 Pedro 2:1-10', 'Ser parte viva da casa espiritual de Deus', 'Somos pedras vivas no templo espiritual. Cristo é a pedra angular que sustenta tudo.', [
        mc('Que somos como pedras?', ['Mortas','Vivas','Pesadas','Frias'], 1, 'Pedras vivas, edificados espiritualmente'),
        vf('A pedra angular e Paulo.', 'A pedra angular e Paulo.', 0, 'Cristo e a pedra angular'),
        mc('Somos uma casa sacerdotal:', ['Para sacrificio','Espiritual','Material','Politica'], 1, 'Casa sacerdotal espiritual'),
    ]),
    ('1 Pedro 3: Casamento', 'Vós, mulheres, sujeitai-vos ao vosso marido. Vós, maridos, vivei com elas com entendimento, honrando-as como vasos mais fracos. A graça é a herança da vida.', '1 Pedro 3:1-7', 'Viver em harmonia no casamento segundo Deus', 'O amor mútuo, o respeito e a oração fortalecem o casamento cristão.', [
        mc('As mulheres devem ser:', ['Dominadas','Sujeitas com entendimento','Obedientes sem pensar','Lideres'], 1, 'Sujeitas com entendimento'),
        vf('Os maridos podem tratar mal as esposas.', 'Os maridos podem tratar mal as esposas.', 0, 'Vivei com entendimento, honrando-as'),
        mc('Segundo 1 Pedro 3:7, o que pode impedir as oracoes?', ['O marido nao honrar a esposa','A oracao em si mesma','A idade do casal','A profissao do esposo'], 0, '1 Pedro 3:7 - para que as vossas oracoes nao sejam impedidas'),
    ]),
    ('2 Pedro 1: Crescimento Espiritual', 'Procurai tornar ainda mais firmes a vocação e a eleição. Acrescentai a vossa fé à virtude, a virtude ao conhecimento, o conhecimento à temperança.', '2 Pedro 1:3-11', 'Crescer ativamente na fé e nas virtudes', 'O crescimento espiritual e intencional. Cada virtude leva a outra, produzindo frutos.', [
        mc('O que devemos acrescentar a fe?', ['Nada','Virtude','Riqueza','Fama'], 1, 'Acrescentai a vossa fe a virtude'),
        vf('O crente nao precisa se esforcar para crescer.', 'O crente nao precisa se esforcar para crescer.', 0, 'Procurai tornar firmes - esforco intencional'),
        mc('Sem essas qualidades, o crente e:', ['Cego','Pobre','Esquecido','Fortalecido'], 0, 'Cego e esquecido'),
    ]),
    ('2 Pedro 3: O Dia do Senhor', 'O dia do Senhor virá como ladrão. Nos novos céus e nova terra, habita justiça. Aguardai e apressai-vos pela vinda do Senhor.', '2 Pedro 3:8-13', 'Viver na expectativa do dia do Senhor', 'Deus não tarda a sua promessa. Devemos viver santamente esperando os novos céus e terra.', [
        mc('O dia do Senhor vem como:', ['Festival','Aviao','Ladrao na noite','Desfile'], 2, 'Vira como ladrao na noite'),
        vf('Deus tarda por esquecimento.', 'Deus tarda por esquecimento.', 0, 'Nao e tardio, mas paciente - 2 Pedro 3:9'),
        mc('O que haverá?', ['Novos ceus e nova terra','Destruicao total','Nada','Mesma terra velha'], 0, 'Novos ceus e nova terra, onde habita justica'),
    ]),
], 50)
print("  Trilha 13 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 14 - Joao e Cartas Breves
# ═══════════════════════════════════════════════
t14 = mk_trilha('Joao e Cartas Breves', 'As cartas apostolicas sobre a verdade, o amor, a comunhao com Deus e a defesa da fe contra falsos ensinos', 'adulto', 'intermediario', 14, 'mail')
add_licoes(t14, [
    ('1 João 1: Luz e Comunhão', 'A vida eterna era com o Pai e foi revelada aos apóstolos. Anunciamos a vós o que vimos e ouvimos, para que também tenhais comunhão conosco e com o Pai.', '1 Joao 1:1-4', 'Cultivar comunhão genuína com Deus e com os irmãos', 'A comunhão com Deus se dá pela luz e pela confissão do pecado. Jesus é a luz que purifica.', [
        mc('O que os apostolos anunciaram?', ['Riqueza','O que viram e ouviram','Poder','Fama'], 1, 'O que vimos e ouvimos'),
        vf('Podemos ter comunhao com Deus vivendo na escuridao.', 'Podemos ter comunhao com Deus vivendo na escuridao.', 0, 'Deus e luz - 1 Joao 1:5'),
        mc('Se confessarmos os pecados:', ['Deus nos ama mais','Deus e fiel e justo para nos perdoar','Nada acontece','Perdemos a salvacao'], 1, 'Deus e fiel e justo para perdoar'),
    ]),
    ('1 João 2: O Advogado', 'Se alguém pecar, temos um advogado junto ao Pai, Jesus Cristo, o justo. Ele é a propiciação pelos nossos pecados. Guardai os Seus mandamentos.', '1 Joao 2:1-6', 'Ter confiança no advogado Jesus Cristo', 'Jesus intercede por nós. Quem conhece a Deus guarda os Seus mandamentos.', [
        mc('Quem e nosso advogado?', ['Paulo','Pedro','Jesus Cristo','Tiago'], 2, 'Jesus Cristo, o justo'),
        vf('Jesus nao pode nos perdoar de pecados futuros.', 'Jesus nao pode nos perdoar de pecados futuros.', 0, 'E propiciação pelos nossos pecados - presente e futuro'),
        mc('O que o crente deve fazer?', ['Pecar muito','Guardar os mandamentos','Nao orar','Ignorar a Lei'], 1, 'Guardai os mandamentos'),
    ]),
    ('1 João 3: Filhos de Deus', 'Vede que amor nos deu o Pai, para que fôssemos chamados filhos de Deus. Ninguém o viu, mas se amamos uns aos outros, Deus permanece em nós.', '1 Joao 3:1-24', 'Viver como filhos amados de Deus', 'Somos filhos de Deus e seremos como Ele. O amor fraternal prova que estamos nele.', [
        mc('Que amor nos deu o Pai?', ['Amor mundano','Para sermos chamados filhos de Deus','Amor condicional','Amor temporario'], 1, 'Para que fôssemos chamados filhos de Deus'),
        vf('Vimos a Deus com os olhos fisicos.', 'Vimos a Deus com os olhos fisicos.', 0, 'Ninguem o viu - 1 Joao 3:2'),
        mc('O que prova que estamos nEle?', ['Riqueza','O amor fraternal','Fama','Conhecimento'], 1, 'Se amamos uns aos outros'),
    ]),
    ('1 João 4: Deus e Amor', 'Deus é amor. Quem ama a Deus ama também ao seu irmão. Neles se revelou o amor de Deus: em nos ter mandado o Seu Filho unigênito como propiciação.', '1 Joao 4:7-21', 'Amar porque Deus amou primeiro', 'O amor é a essência de Deus. Quem O ama, ama a seus irmãos. O amor perfeito expulsa o medo.', [
        mc('Deus e:', ['Apenas justiça','Apenas poder','Amor','Ira'], 2, 'Deus e amor'),
        vf('O amor e opcional na vida cristã.', 'O amor e opcional na vida cristã.', 0, 'Quem ama a Deus ama tambem ao seu irmao'),
        mc('O amor perfeito expulsa:', ['A graça','O medo','A fe','A esperanca'], 1, 'O amor perfeito expulsa o medo'),
    ]),
    ('1 João 5: A Vitória', 'Toda a fé no nome do Filho de Deus nos vence o mundo. A vitória que vence o mundo é a nossa fé. Sabemos que o Filho de Deus veio e nos deu entendimento.', '1 Joao 5:1-12', 'Viver na certeza da vitória pela fé', 'A fé em Cristo nos dá vitória sobre o mundo. Temos a certeza da vida eterna.', [
        mc('O que nos vence o mundo?', ['A forca','O dinheiro','A fe no nome de Cristo','A inteligencia'], 2, 'A fe no Filho de Deus'),
        vf('Nao temos certeza da vida eterna.', 'Nao temos certeza da vida eterna.', 0, 'Temos a vida eterna - 1 Joao 5:11-12'),
        mc('A vitoria e:', ['Do mundo','Do diabo','A nossa fe','Nao existe'], 2, 'A vitoria que vence o mundo e a nossa fe'),
    ]),
    ('2 João: A Verdade', 'A verdade permanece em nós e estará conosco para sempre. Guardai-vos dos enganadores que não trazem a doutrina de Cristo. A graça, a misericórdia e a paz estejam conosco.', '2 Joao 1:1-13', 'Guarda a verdade e não se desvie do evangelho', 'A verdade em Cristo é eterna. Devemos rejeitar falsos ensinos e andar na verdade.', [
        mc('O que devemos guardar?', ['Riqueza','A verdade de Cristo','O poder','O mundo'], 1, 'A verdade que permanece'),
        vf('Devemos aceitar qualquer ensino.', 'Devemos aceitar qualquer ensino.', 0, 'Guardai-vos dos enganadores'),
        mc('A verdade estara:', ['Apenas hoje','Para sempre','Nunca','As vezes'], 1, 'Para sempre connosco'),
    ]),
    ('3 João: Gaio', 'Gaio é elogiado por sua hospitalidade e fidelidade à verdade. Diotrefes, ao contrário, recusa receber os irmãos e fala maldade. Demétrio é testemunhado por todos.', '3 Joao 1:1-15', 'Praticar hospitalidade e fidelidade à verdade', 'A hospitalidade genuína é fruto da fé. Gaio é exemplo de amor e serviço aos irmãos.', [
        mc('Gaius e elogiado por:', ['Ser rico','Hospitalidade e fidelidade','Ser famoso','Ter poder'], 1, 'Hospitalidade e fidelidade a verdade'),
        vf('Diotrefes era um bom lider.', 'Diotrefes era um bom lider.', 0, 'Recusava receber os irmaos e falava maldade'),
        mc('O que a hospitalidade demonstra?', ['Maldade','Amor e fidelidade','Fraqueza','Superioridade'], 1, 'Amor e fidelidade a verdade'),
    ]),
    ('Judas: Defenda a Fé', 'Lutai pela fé que uma vez foi entregue aos santos. Há homens perversos que transformam a graça de Deus em licença para pecar. Mas Aquele que pode guardar-vos sem tropeço.', 'Jude 1:3-25', 'Defender a fé ortodoxa contra falsos ensinadores', 'A fé precisa ser defendida. Falsos mestres entram na igreja para destruir.', [
        mc('O que devemos fazer pela fe?', ['Ignorar','Lutar por ela','Trocar','Esquecer'], 1, 'Lutai pela fe que uma vez foi entregue'),
        vf('Os falsos ensinadores sao faceis de identificar.', 'Os falsos ensinadores sao faceis de identificar.', 0, 'Entrao na igreja disfarçados'),
        mc('Quem pode guardar-nos sem tropeco?', ['Nos mesmos','Deus','O diabo','Os anjos'], 1, 'Aquele que pode guardar-vos sem tropeco'),
    ]),
    ('Lamentações 3: Misericórdias de Deus', 'As misericórdias de Deus não se esgotam. São novas a cada manhã. Grande é a fidelidade do Senhor. O Senhor não rejeita para sempre.', 'Lamentacoes 3:22-33', 'Renovar a esperança nas misericórdias de Deus', 'Mesmo na maior tribulação, as misericórdias de Deus se renovam. Sua fidelidade é grande.', [
        mc('As misericordias de Deus sao:', ['Velhas e esgotadas','Novas a cada manha','Limitadas','Inexistentes'], 1, 'Novas a cada manha'),
        vf('Deus nos rejeita para sempre quando pecamos.', 'Deus nos rejeita para sempre quando pecamos.', 0, 'O Senhor nao rejeita para sempre'),
        mc('Grande e:', ['O dinheiro','A fidelidade do Senhor','O pecado','O mundo'], 1, 'A fidelidade do Senhor'),
    ]),
    ('Apocalipse 1: Jesus Glorificado', 'João viu uma visão do Filho do homem, vestido com uma faixa dourada, com cabelos brancos como lã, olhos como chamas de fogo. "Eu sou o Alfa e o Ômega."', 'Apocalipse 1:9-20', 'Rever a glória e o poder de Jesus Cristo', 'Jesus é glorificado e poderoso. Ele morreu e vive para sempre. Ele tem as chaves da morte e do Hades.', [
        mc('Como sao os olhos de Cristo na visao?', ['Azuis','Verdes','Como chamas de fogo','Pretos'], 2, 'Olhos como chamas de fogo'),
        vf('Jesus e chamado de Alfa e Omega porque e o primeiro e o ultimo.', 'Jesus e o primeiro e o ultimo.', 1, 'Alfa e Omega, o primeiro e o ultimo'),
        mc('Jesus tem as chaves de:', ['A vida','O ceu','A morte e o hades','O mundo'], 2, 'As chaves da morte e do hades'),
    ]),
], 50)
print("  Trilha 14 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 15 - Apocalipse: A Consumacao
# ═══════════════════════════════════════════════
t15 = mk_trilha('Apocalipse: A Consumacao', 'A revelação final de Deus sobre o triunfo de Cristo, o julgamento do mal e a consumação de todas as coisas na nova criacao', 'adulto', 'avancado', 15, 'explore')
add_licoes(t15, [
    ('Apocalipse 1: A Revelação', 'João recebeu a revelação de Jesus Cristo. Ele a viu em visão na ilha de Patmos. O Alfa e o Ômega, que era, que é e que há de vir, enviou seu anjo para mostrar as coisas que devem brevemente acontecer.', 'Apocalipse 1:1-8', 'Entender a natureza e o propósito do Apocalipse', 'O Apocalipse é a revelação de Jesus Cristo, dada para mostrar aos servos o que deve acontecer.', [
        mc('A quem a revelação foi dada?', ['A Paulo','A Pedro','A Joao','A Tiago'], 2, 'Joao recebeu a revelação'),
        vf('O Apocalipse e um livro sobre o passado.', 'O Apocalipse e um livro sobre o passado.', 0, 'Mostra as coisas que devem brevemente acontecer'),
        mc('Jesus se chama:', ['O primeiro','O ultimo','Alfa e Omega','Todas as anteriores'], 3, 'Alfa e Omega, o primeiro e o ultimo'),
    ]),
    ('Apocalipse 4-5: O Trono e o Cordeiro', 'João viu o trono no céu e 24 anciãos em volta. No meio do trono estava o Cordeiro como tendo sido morto, digno de receber poder, riquezas, sabedoria, honra e glória.', 'Apocalipse 4:1-5:14', 'Adorar a Deus no trono e ao Cordeiro digno', 'O Cordeiro que foi morto e digno de abrir o livro dos selos. Toda a criação o adora.', [
        mc('Quantos ancioes estavam ao redor do trono?', ['12','24','48','72'], 1, '24 ancioes em volta do trono'),
        vf('O Cordeiro foi morto e voltou a viver.', 'O Cordeiro foi morto e voltou a viver.', 1, 'Como tendo sido morto, esta de pe'),
        mc('O Cordeiro e digno de receber:', ['Nada','Poder, riquezas, sabedoria, honra e gloria','Apenas poder','Dinheiro'], 1, 'Poder, riquezas, sabedoria, honra e gloria'),
    ]),
    ('Apocalipse 6: Os Selos', 'O Cordeiro abriu os selos um por um. O primeiro selo: cavaleiro branco (conquista). O segundo: vermelho (guerra). O terceiro: preto (fome). O quarto: verde (morte).', 'Apocalipse 6:1-17', 'Reconhecer os juízos que precedem a consumação', 'Os selos representam juízos progressivos sobre a terra. O sétimo selo traz silêncio no céu.', [
        mc('O que o cavaleiro branco representa?', ['Paz','Conquista','Morte','Guerra'], 1, 'O primeiro cavaleiro, que sai conquistando'),
        vf('O terceiro selo traz alegria.', 'O terceiro selo traz alegria.', 0, 'O terceiro selo traz fome e escassez'),
        mc('O que acontece quando o sexto selo e aberto?', ['Paz','Grandes tremores de terra','Alegria','Nao acontece nada'], 1, 'Grandes tremores de terra e eclipses'),
    ]),
    ('Apocalipse 7: A Multidão', 'Uma multidão enorme, que ninguém podia contar, de todas as nações, tribos, povos e língua, estava de pé diante do trono e do Cordeiro, com palmas nas mãos.', 'Apocalipse 7:9-17', 'Ter visão da multidão dos resgatados', 'De todos os povos e nações, a multidão dos redimidos adora a Deus e ao Cordeiro.', [
        mc('De onde veio a multidao?', ['De Israel apenas','De todas as nações','De Roma','De Atenas'], 1, 'De todas as nações, tribos, povos e lingua'),
        vf('A multidao era apenas de judeus.', 'A multidao era apenas de judeus.', 0, 'De todas as nações'),
        mc('O que a multidao faz?', ['Chora','Canta louvor ao Cordeiro','Luta','Dorme'], 1, 'Clamou em voz alta: a salvacao e do nosso Deus'),
    ]),
    ('Apocalipse 8-9: As Trombetas', 'Sete anjos tocam trombetas. Grandes destruições caem sobre a terra: metade das árvores queimadas, os mares transformados em sangue, trevas sobre a terra.', 'Apocalipse 8:1-9:21', 'Entender a gravidade dos juízos das trombetas', 'Os juízos se intensificam. Mesmo assim, os homens não se arrependem de suas obras.', [
        mc('O que acontece quando a primeira trombeta soa?', ['Paz','Granizo e fogo misturado com sangue caem na terra','Nada','Nuvens'], 1, 'Granizo e fogo misturado com sangue caem na terra'),
        vf('Os homens se arrependem completamente com as trombetas.', 'Os homens se arrependem completamente.', 0, 'Nao se arrependem de suas obras'),
        mc('O que o terceiro anjo derrama?', ['Agua limpa','Absinto (amargura)','Ouro','Leite'], 1, 'Apocalipse 8:10-11 - a estrela Absinto torna as aguas amargas'),
    ]),
    ('Apocalipse 12: A Mulher e o Dragão', 'Uma mulher revestida de sol, com a lua sob seus pés, deu à luz um varão que governaria as nações. O grande dragão, a serpente antiga, perseguiu a mulher e o seu descendente.', 'Apocalipse 12:1-17', 'Reconhecer a guerra espiritual entre o bem e o mal', 'A mulher representa Israel/Igreja. O dragão é Satanás. O descendente é Cristo. A guerra espiritual e real.', [
        mc('O dragao e identificado como:', ['O imperador romano','Satanás, a serpente antiga','Um animal real','O profeta falso'], 1, 'Satanás, a serpente antiga, o diabo'),
        vf('O varao que governaria as nações e Paulo.', 'O varao que governaria as nações e Paulo.', 0, 'E Cristo, que pastoreia todas as nações com vara de ferro'),
        mc('Como o dragao e derrotado?', ['Pelo exercito','Pelo sangue do Cordeiro e pela palavra do testemunho','Pela forca humana','Nao e derrotado'], 1, 'Pelo sangue do Cordeiro e pela palavra do testemunho'),
    ]),
    ('Apocalipse 13: A Besta', 'Uma besta subiu do mar, com dez chifres e sete cabeças, blasfemando contra Deus. O mundo inteiro adorou a besta. Outra besta fez um nome para a primeira.', 'Apocalipse 13:1-18', 'Reconhecer os sistemas malignos contra o povo de Deus', 'A besta representa poderes políticos anticristos. A marca da besta controla o comércio e a vida.', [
        mc('De onde subiu a besta?', ['Do ceu','Do mar','Da terra','Do inferno'], 1, 'Do mar, com dez chifres e sete cabecas'),
        vf('A besta recebeu poder do diabo.', 'A besta recebeu poder do diabo.', 1, 'O dragao deu poder a besta - Apocalipse 13:2'),
        mc('Quantos podem ser comerciaveis sem a marca?', ['Todos','Ninguem','Apenas ricos','Apenas lideres'], 1, 'Ninguem pode comprar ou vender sem a marca'),
    ]),
    ('Apocalipse 14: O Ceifão', 'Anjos ceifam a terra. O ceifador é mandado porque a terra já está madura para o juízo. Outro anjo ceifou os cachos da terra, atirando-os no grande lagar da ira de Deus.', 'Apocalipse 14:14-20', 'Entender a vindima final e o juízo de Deus', 'A terra está madura para o juízo. Deus separa os justos e os injustos.', [
        mc('O que a ceifa da terra representa?', ['A colheita comum','O juizo final de Deus','A festa de acao de gracas','Um dia comum de trabalho'], 1, 'Apocalipse 14:14-20 - a terra esta madura para o juizo'),
        vf('O juizo de Deus e justo.', 'O juizo de Deus e justo.', 1, 'Os pecados sao julgados conforme suas obras'),
        mc('O que e o grande lagar?', ['Um rio','A ira de Deus derramada','Um lago de agua','Um campo'], 1, 'A ira de Deus derramada sem misericordia'),
    ]),
    ('Apocalipse 19: O Cavaleiro Fiel', 'O cavaleiro (Jesus) aparece montado em um cavalo branco. Seus olhos são como chamas de fogo. Na sua boca uma espada afiada. É rei dos reis e senhor dos senhores.', 'Apocalipse 19:11-21', 'Vitória final de Cristo sobre todos os inimigos', 'Jesus retorna como juiz e rei. É justo e fiel. As nações são pastoreadas com vara de ferro.', [
        mc('Como Jesus retorna?', ['Cavalo preto','Cavalo branco','A pe','De carroça'], 1, 'Montado num cavalo branco'),
        vf('Jesus retorna como servo.', 'Jesus retorna como servo.', 0, 'Retorna como rei dos reis e senhor dos senhores'),
        mc('Na boca de Jesus ha:', ['Uma coroa','Uma espada afiada','Uma moeda','Uma ampulheta'], 1, 'Uma espada afiada'),
    ]),
    ('Apocalipse 21-22: A Nova Jerusalém', 'Vi os novos céus e a nova terra. A Nova Jerusalém desce do céu, preparada como uma noiva adornada. Não haverá mais lágrimas, nem morte, nem dor. O Alfa e o Ômega está ali.', 'Apocalipse 21:1-22:21', 'Esperar a Nova Jerusalém e a consumação de todas as coisas', 'A promessa final é a restauração completa. Sem lágrimas, sem morte, sem dor. A presença de Deus é eterna.', [
        mc('O que nao haverá na nova criacao?', ['Alegría','Larmas, morte e dor','Louvor','Amor'], 2, 'Nao haverá mais larmas, nem morte, nem dor'),
        vf('A Nova Jerusalem e um lugar simbolico sem realidade.', 'A Nova Jerusalem e apenas simbolica.', 0, 'E a cidade real de Deus, desce do ceu'),
        mc('Quem esta no centro da nova criacao?', ['O homem','Deus e o Cordeiro','Os anjos','O diabo'], 1, 'Deus e o Cordeiro'),
    ]),
], 50)
print("  Trilha 15 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 16 - Sabedoria e Poesia
# ═══════════════════════════════════════════════
t16 = mk_trilha('Sabedoria e Poesia', 'Proverbios, Eclesiastes e Cantares: a busca pela sabedoria, o sentido da vida e o amor segundo Deus', 'adulto', 'iniciante', 16, 'psychology')
add_licoes(t16, [
    ('Provérbios 1: O Princípio da Sabedoria', 'O temor do Senhor é o princípio da sabedoria. Os provérbios ensinam sabedoria, disciplina e entendimento. O filho prudente escuta o pai e a mãe.', 'Proverbios 1:1-33', 'Entender que o temor do Senhor é a base de toda sabedoria', 'A sabedoria bíblica começa com reverência a Deus. Sem isso, todo conhecimento é vazio.', [
        mc('Qual e o principio da sabedoria?', ['Ter dinheiro','Ter poder','O temor do Senhor','Saber tudo'], 2, 'Proverbios 1:7 - o temor do Senhor e o principio da sabedoria'),
        vf('A sabedoria biblica comeca com o conhecimento humano.', 'A sabedoria comeca com o conhecimento humano.', 0, 'Comeca com o temor do Senhor'),
        mc('O que o filho prudente faz?', ['Obedece aos pais','Ignora os pais','Foge de casa','Desafia os pais'], 0, 'Proverbios 1:8 - escuta a instrucao do teu pai'),
    ]),
    ('Provérbios 3: Confie no Senhor', 'Confia no Senhor de todo o teu coração e não te estribes no teu próprio entendimento. Reconhece-O em todos os teus caminhos, e Ele endireitará as tuas veredas.', 'Proverbios 3:1-26', 'Aprender a confiar plenamente em Deus em todas as situações', 'A confiança em Deus substitui a ansiedade. Ele é a sabedoria e o poder eterno.', [
        mc('No que nao devemos nos estribar?', ['Em Deus','No proprio entendimento','Na Biblia','Na oracao'], 1, 'Proverbios 3:5 - nao te estribes no teu propio entendimento'),
        vf('Devemos confiar em Deus apenas quando faz sentido.', 'Devemos confiar apenas quando faz sentido.', 0, 'De todo o teu coracao'),
        mc('O que Deus faz com quem O reconhece?', ['Abandona','Ignora','Endireita os caminhos','Pune'], 2, 'Proverbios 3:6 - Ele endireitara as tuas veredas'),
    ]),
    ('Provérbios 22: O Nome Bom', 'Melhor é o bom nome do que grandes riquezas, e a benevolência mais que o ouro e a prata. O rico e o pobre se encontram; ambos o Senhor os fez.', 'Proverbios 22:1-29', 'Valorizar o caráter acima da riqueza material', 'A reputação construída na justiça é mais valiosa que qualquer fortuna.', [
        mc('O que e melhor que grandes riquezas?', ['Ter poder','Ter fama','O bom nome','Ter um exercito'], 2, 'Proverbios 22:1 - melhor o bom nome que grandes riquezas'),
        vf('O rico e mais importante que o pobre aos olhos de Deus.', 'O rico e mais importante aos olhos de Deus.', 0, 'Proverbios 22:2 - ambos o Senhor os fez'),
        mc('Quem fez o rico e o pobre?', ['A sorte','O governo','O Senhor','A natureza'], 2, 'Proverbios 22:2 - ambos o Senhor os fez'),
    ]),
    ('Provérbios 31: A Mulher Virtuosa', 'Quem achará esposa virtuosa? Ela traz lucro e não perdas. Abre a boca com sabedoria, e na sua língua há lição de bondade. Deita e levanta à noite e de dia trabalha.', 'Proverbios 31:10-31', 'Reconhecer e valorizar o trabalho e o caráter da mulher virtuosa', 'A mulher virtuosa é exemplo de diligência, sabedoria, bondade e temor a Deus.', [
        mc('O que a mulher virtuosa traz?', ['Lucro e nao perdas','Perdas e lucro','Nada','Apenas perdas'], 0, 'Proverbios 31:11 - traz lucro e nao perdas'),
        vf('A mulher virtuosa e definida pelas riquezas.', 'E definida pelas riquezas.', 0, 'E definida pelo temor do Senhor e pelo trabalho'),
        mc('Quem louva a mulher virtuosa?', ['Os filhos e o marido','Os vizinhos','Os reis','Ninguem'], 0, 'Proverbios 31:28 - seus filhos a levantam e o marido a louva'),
    ]),
    ('Eclesiastes 1: Vaidade de Vaidades', 'Vaidade de vaidades, diz o Eclesiastes, vaidade de vaidades, tudo é vaidade. Que proveito tem o homem de todo o seu trabalho? O sol nasce e se põe, e volta ao seu lugar.', 'Eclesiastes 1:1-18', 'Refletir sobre o sentido da vida e a vaidade das coisas terrenas', 'O autor conclui que o trabalho e os prazeres são passageiros. A verdadeira satisfação está em Deus.', [
        mc('Qual e a frase-chave de Eclesiastes?', ['Tudo e bom','Vaidade de vaidades','A vida e facil','Nada importa'], 1, 'Eclesiastes 1:2 - vaidade de vaidades'),
        vf('Eclesiastes diz que o trabalho humano nao tem sentido algum.', 'Diz que o trabalho nao tem sentido algum.', 0, 'Questiona o sentido eterno, mas reconhece o valor no trabalho'),
        mc('O que acontece com o sol?', ['Para de girar','Nasce e volta ao seu lugar','Nao existe','Muda de cor'], 1, 'O sol nasce e volta ao seu lugar'),
    ]),
    ('Eclesiastes 2: Tentativas Vãs', 'Provei com o vinho, com a música, com as grandes obras, com palácios e jardins. Tudo era vaidade e aflição de espírito. Não há nada de novo sob o sol.', 'Eclesiastes 2:1-26', 'Entender que prazeres e conquistas não satisfazem plenamente', 'O autor experimentou tudo, mas nada trouxe satisfação duradoura. O bem está em Deus.', [
        mc('O que o autor experimentou?', ['Apenas oracao','Vinho, musica, obras, palacios','Nada','Apenas trabalho'], 1, 'Eclesiastes 2 - provou todas as coisas'),
        vf('O autor encontrou satisfacao total na riqueza.', 'Encontrou satisfacao total na riqueza.', 0, 'Tudo era vaidade e aflicao de espirito'),
        mc('Onde esta o bem?', ['No dinheiro','Em si mesmo','Em Deus','No mundo'], 2, 'Eclesiastes 2:24 - nao ha nada melhor do que alegrar-se'),
    ]),
    ('Eclesiastes 12: Lembra do Criador', 'Lembra do teu Criador na flora da tua juventude, antes que venham os maus dias e se aproximem os anos em que dirás: não tenho nele prazer algum.', 'Eclesiastes 12:1-14', 'Buscar a Deus desde jovem e viver com eternidade em vista', 'A juventude é o tempo de buscar a Deus. A vida é vaidade sem Ele.', [
        mc('Quando devemos lembrar do Criador?', ['Na velhice','Na flora da juventude','Nunca','Apenas no sabado'], 1, 'Eclesiastes 12:1 - na flora da tua juventude'),
        vf('Eclesiastes diz para lembrar de Deus apenas na velhice.', 'Diz para lembrar apenas na velhice.', 0, 'Na flora da juventude'),
        mc('Qual e o temor de Deus segundo Eclesiastes?', ['Medo','Guarda os mandamentos e julga toda obra','Indiferenca','Alegria'], 1, 'Eclesiastes 12:13 - teme a Deus e guarda os seus mandamentos'),
    ]),
    ('Cantares 1: O Amor', 'Deixe-me beijar-te com o beijo da tua boca. O teu amor é melhor que o vinho. Somos negras, mas formosas. Digam-me onde apascentas o teu rebanho.', 'Cantares 1:1-17', 'Valorizar o amor como presente divino', 'O Cantares celebra o amor humano como reflexo do amor divino. É belo e puro.', [
        mc('O que e melhor que o vinho segundo o Cantares?', ['O poder','O amor','A riqueza','A fama'], 1, 'Cantares 1:2 - o teu amor e melhor que o vinho'),
        vf('O Cantares fala apenas de amor espiritual.', 'Fala apenas de amor espiritual.', 0, 'Celebra o amor humano e marital'),
        mc('O que as mulheres pedem?', ['Dinheiro','Para onde apascenta o rebanho','Poder','Roupa'], 1, 'Cantares 1:7 - digam-me onde apascentas'),
    ]),
    ('Cantares 2: O Amor Compartilhado', 'Eu sou a rosa de Sarom, o lírio dos vales. Eis aqui o meu amado, eis aqui ele, saltando pelo monte. As raposas têm casas, mas o Filho do Homem não tem onde repousar.', 'Cantares 2:1-17', 'Reconhecer a beleza do amor compartilhado e o cuidado mútuo', 'O amor é descrito com imagens da natureza: flores, montes e campos.', [
        mc('O que a amada se compara?', ['A uma espada','A uma rosa de Sarom','A uma nuvem','A um rio'], 1, 'Cantares 2:1 - sou a rosa de Sarom'),
        vf('O amor descrito no Cantares e destrutivo.', 'E destrutivo.', 0, 'E belo e edificante'),
        mc('O que o amado faz?', ['Foge','Vem saltando pelo monte','Dorme','Chora'], 1, 'Cantares 2:8 - saltando pelos montes'),
    ]),
    ('Cantares 8: O Amor Forte', 'Põe-me como selo sobre o teu coração, como selo sobre o teu braço, porque o amor é forte como a morte. As muitas águas não podem apagar o amor.', 'Cantares 8:1-14', 'Compreender a força e a permanência do amor verdadeiro', 'O amor descrito no Cantares é mais forte que a morte e irrevogável.', [
        mc('O que o amor e tao forte quanto?', ['A guerra','A morte','O vento','O fogo'], 1, 'Cantares 8:6 - o amor e forte como a morte'),
        vf('As aguas podem apagar o amor verdadeiro.', 'As aguas podem apagar o amor.', 0, 'Muitas aguas nao podem apagar'),
        mc('O que o amor deve ser?', ['Um selo no coracao','Um peso','Uma opcao','Uma obrigatoriedade'], 0, 'Cantares 8:6 - po-me como selo sobre o teu coracao'),
    ]),
], 50)
print("  Trilha 16 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 17 - Historia de Israel
# ═══════════════════════════════════════════════
t17 = mk_trilha('Historia de Israel', 'Dos reis ao exilio e retorno: a monarquia, o reino dividido, o cativeiro babilonico e a reconstrucao', 'adulto', 'iniciante', 17, 'history_edu')
add_licoes(t17, [
    ('1 Reis 3: A Sabedoria de Salomão', 'Deus apareceu a Salomão em sonho e ofereceu o que quisesse. Salomão pediu sabedoria para governar o povo. Deus lhe deu um coração sábio e prudente.', '1 Reis 3:1-15', 'Reconhecer que a sabedoria vem de Deus', 'Salomão pediu sabedoria em vez de riquezas, e Deus lhe deu tudo mais.', [
        mc('O que Salomao pediu a Deus?', ['Riqueza','Poder','Sabedoria','Vida longa'], 2, '1 Reis 3:11 - pediste sabedoria'),
        vf('Deus ficou irritado com o pedido de Salomao.', 'Deus ficou irritado.', 0, 'Deus se agradou e lhe deu um coracao sabio'),
        mc('O que Deus deu a Salomao alem da sabedoria?', ['Nada','Riquezas e honra','Um exercito','Um palacio apenas'], 1, 'Deu-lhe tambem riquezas e honra'),
    ]),
    ('1 Reis 12: O Reino Dividido', 'Roboão, filho de Salomão, recusou aliviar o jugo do povo. Dez tribos se revoltaram sob Jeroboão. Israel se dividiu em dois reinos: norte e sul.', '1 Reis 12:1-24', 'Entender as consequências da insolência e da divisão', 'A arrogância de Roboão dividiu o reino. A desobediência sempre traz consequências.', [
        mc('Por que o reino se dividiu?', ['Fome','Insistencia de Roboao em pesado jugo','Exilio','Guerra externa'], 1, 'Roboao endureceu o jugo'),
        vf('Todos apoiaram Roboao.', 'Todos apoiaram Roboao.', 0, 'Dez tribos se revoltaram'),
        mc('Quem liderou as tribos do norte?', ['Davi','Salomao','Jeroboam','Roboao'], 2, 'Jeroboam liderou as dez tribos'),
    ]),
    ('1 Reis 18-19: Elias no Carmelo', 'Elias desafiou os 450 profetas de Baal no Monte Carmelo. Fogo caiu do céu sobre o sacrifício de Elias. Depois, Deus falou com Elias num murmúrio suave.', '1 Reis 18:1-19:21', 'Confiar no poder de Deus mesmo contra adversários numerosos', 'O confronto no Carmelo prova que o Deus de Israel é o único Deus verdadeiro.', [
        mc('Contra quantos profetas de Baal Elias lutou?', ['100','250','450','1000'], 2, '450 profetas de Baal'),
        vf('Fogo caiu sobre o sacrificio dos profetas de Baal.', 'Fogo caiu sobre o sacrificio de Baal.', 0, 'Fogo caiu apenas sobre o sacrificio de Elias'),
        mc('Como Deus falou com Elias depois?', ['Em tempestade','Num murmurio suave','Em trovao','Num terremoto'], 1, 'Num murmurio suave - 1 Reis 19:12'),
    ]),
    ('2 Reis 2: Elias Elevado', 'Elias foi elevado ao céu num redemoinho, com uma carruagem de fogo. Eliseu, seu discípulo, herdou o seu dom duplo.', '2 Reis 2:1-15', 'Entender a transmissão de autoridade espiritual', 'Elias não viu a morte. Eliseu herdou o poder profético em dobro.', [
        mc('Como Elias foi elevado?', ['Morreu normalmente','Num redemoinho de fogo','Nadou no ceu','Caminhou ate la'], 1, 'Num redemoinho de fogo'),
        vf('Elias foi enterrado como qualquer homem.', 'Foi enterrado como qualquer homem.', 0, 'Foi elevado ao ceu'),
        mc('Quem herdou o don de Elias?', ['Salomao','Roboao','Eliseu','Jeroboam'], 2, 'Eliseu pediu don duplo'),
    ]),
    ('2 Reis 17: O Exílio de Samaria', 'O rei da Assíria deportou Israel para a Assíria por causa da infidelidade a Deus. Samaria caiu porque Israel pecou, serviu a outros deuses e rejeitou a aliança.', '2 Reis 17:1-41', 'Reconhecer que o exílio foi consequência da desobediência', 'O exílio do norte foi o juízo divino pela idolatria persistente.', [
        mc('Para onde Israel foi deportado?', ['Para o Egito','Para a Assiria','Para Babilonia','Para Roma'], 1, 'Reis 17 - para a Assiria'),
        vf('Israel caiu por causa da fraqueza militar apenas.', 'Caiu por fraqueza militar apenas.', 0, 'Caiu por infidelidade a Deus'),
        mc('Qual foi o pecado principal de Israel?', ['Gula','Servir a outros deuses','Cobardia','Avareza'], 1, 'Serviram a outros deuses e rejeitaram a alianca'),
    ]),
    ('Esdras 7: O Retorno', 'Artaxerxes, rei da Pérsia, permitiu que Esdras voltasse a Jerusalém com autoridade para ensinar a Lei de Deus. Muitos judeus retornaram do exílio.', 'Esdras 7:1-28', 'Reconhecer o cumprimento da promessa de retorno', 'Deus tocou o coração do rei persa para libertar o povo.', [
        mc('Quem permitiu o retorno?', ['Ciro','Artaxerxes','Dario','Cambises'], 1, 'Esdras 7:1 - Artaxerxes, rei da Persia'),
        vf('Todos os judeus retornaram do exilio.', 'Todos retornaram.', 0, 'Muitos voltaram, nem todos'),
        mc('O que Esdras levou de volta?', ['Exercito','A Lei de Deus e a autoridade real','Ouro apenas','Nada'], 1, 'Levou a Lei e a autoridade para ensinar'),
    ]),
    ('Neemias 2: Reconstrução dos Muros', 'Neemias, copeiro do rei, ficou triste ao saber que os muros de Jerusalém estavam destruídos. Pediu licença ao rei e reconstruiu os muros em 52 dias.', 'Neemias 2:1-20', 'Entender que a restauração requer coragem e ação', 'A reconstrução dos muros simboliza a restauração da identidade e proteção do povo.', [
        mc('Quanto tempo levou para reconstruir os muros?', ['1 ano','52 dias','10 anos','5 meses'], 1, 'Neemias 2 - 52 dias'),
        vf('Neemias era sacerdote.', 'Era sacerdote.', 0, 'Era copeiro do rei'),
        mc('O que Neemias fez ao saber da destruicao?', ['Ignorou','Orou e pediu ao rei para voltar','Desistiu','Largou tudo'], 1, 'Orou e pediu autorizacao ao rei'),
    ]),
    ('Neemias 6-8: A Leitura da Lei', 'Esdras leu publicamente a Lei de Deus diante de todo o povo. O povo chorou ao ouvir, mas Neemias disse: A alegria do Senhor e a vossa fortaleza.', 'Neemias 8:1-12', 'Reconhecer a importância da Palavra de Deus na vida do povo', 'A leitura pública da Lei renovou a aliança e trouxe alegria ao povo.', [
        mc('Quem leu a Lei publicamente?', ['Neemias','Esdras','Salomao','Davi'], 1, 'Esdras leu publicamente'),
        vf('O povo ficou alegre ao ouvir a Lei.', 'Ficou alegre imediatamente.', 0, 'Primeiro choraram, depois se alegraram'),
        mc('O que Neemias disse ao povo?', ['Chorem mais','A alegria do Senhor e a vossa fortaleza','Desistam','Fujam'], 1, 'Neemias 8:10 - a alegria do Senhor e a vossa fortaleza'),
    ]),
    ('Ester 4: Para Tal Tempo', 'Mardoqueu disse a Ester: Quem sabe se não foste elevada a tal posição para um tempo como este? Ester arriscou a vida para salvar o povo judeu.', 'Ester 4:1-17', 'Reconhecer que Deus nos coloca onde precisa para cumprir Sua vontade', 'Ester foi colocada no palácio para um propósito divino de salvar seu povo.', [
        mc('Por que Mardoqueu disse isso a Ester?', ['Para pedir dinheiro','Para a salvar de Haman','Para lembrar seu proposito divino','Para pedir que fugisse'], 2, 'Para tal tempo quanto esta foste elevada'),
        vf('Ester recusou ajudar o povo.', 'Recusou ajudar.', 0, 'Arriscou a vida para salvar o povo'),
        mc('O que Ester disse antes de agir?', ['Nao vou','Se eu perecer, perecerei','Preciso de ajuda','Vou fugir'], 1, 'Se eu perecer, perecerei'),
    ]),
    ('Ester 9: O Decreto de Purim', 'Os judeus venceram seus inimigos na Pérsia. Ester e Mardoqueu estabeleceram a festa de Purim para lembrar a libertação. A alegria substituiu o luto.', 'Ester 9:1-32', 'Celebrar a libertação de Deus mesmo em tempos difíceis', 'Purim celebra a vitória divina sobre os opressores.', [
        mc('Que festa foi estabelecida?', ['Pascoa','Pentecostes','Purim','Tabernaculos'], 2, 'Ester 9 - a festa de Purim'),
        vf('Purim e uma festa de tristeza.', 'E uma festa de tristeza.', 0, 'E uma festa de alegria e celebracao'),
        mc('O que os judeus venceram?', ['Um exercito romano','Os seus inimigos na Persia','Os filisteus','Os babilonios'], 1, 'Venceram seus inimigos na Persia'),
    ]),
], 50)
print("  Trilha 17 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 18 - Juizes e Ruth
# ═══════════════════════════════════════════════
t18 = mk_trilha('Juizes e Ruth', 'O ciclo dos juizes, as historias de Debora, Gideao, Sansao e a bela historia de fidelidade de Ruth', 'adulto', 'iniciante', 18, 'gavel')
add_licoes(t18, [
    ('Juízes 2: O Ciclo dos Juízes', 'Israel pecou, entregou a Deus, Deus os vendeu a inimigos, Israel clamou, e Deus levantou um juiz para livrar. O ciclo se repetiu muitas vezes.', 'Juizes 2:1-23', 'Entender o padrão de pecado, juízo e misericórdia', 'O ciclo dos juízes revela a paciência de Deus e a tendência humana de repetir erros.', [
        mc('O que Israel fazia?', ['Servia sempre a Deus','Pecava e era entregue a inimigos','Nunca clamou','Ignorava a Deus'], 1, 'Israel pecava, era entregue, clamava e Deus livrava'),
        vf('Deus nunca livrou Israel dos inimigos.', 'Deus nunca livrou.', 0, 'Deus sempre levantou juizes para livrar'),
        mc('Quem Deus levantava?', ['Reis','Juizes','Profetas','Sacerdotes'], 1, 'Levantava juizes para livrar Israel'),
    ]),
    ('Juízes 4: Débora, Juíza de Israel', 'Débora, profetisa, julgava Israel sob uma palmeira. Baraque se recusou a lutar sem ela. Débora profetizou que a glória da vitória iria para uma mulher.', 'Juizes 4:1-24', 'Reconhecer que Deus usa mulheres poderosamente', 'Débora foi líder, profetisa e juíza. Deus usa quem Ele quer, independente de gênero.', [
        mc('Onde Debora julgava Israel?', ['No templo','Sob uma palmeira','Na guerra','No palacio'], 1, 'Sob a palmeira de Debora'),
        vf('Baraque lutou sozinho contra Sisera.', 'Lutou sozinho.', 0, 'Recusou ir sem Debora'),
        mc('Quem venceu Sisera, o general?', ['Baraque','Debora','Jael, a mulher de Heber','Moises'], 2, 'Jael matou Sisera com um prego'),
    ]),
    ('Juízes 6: Gideão, o Valente', 'Deus chamou Gideão, o menor da família mais fraca, para libertar Israel. Gideão pediu sinais: o orvalho no véu de lã e o orvalho na eira.', 'Juizes 6:1-40', 'Entender que Deus usa os fracos para confundir os fortes', 'Gideão duvidou, mas Deus o fortaleceu e usou seu exército pequeno.', [
        mc('Quem Deus chamou para libertar Israel?', ['Um grande guerreiro','Gideao, o menor da familia mais fraca','O rei','O sacerdote'], 1, 'Gideao, o menor da familia mais fraca'),
        vf('Gideao aceitou imediatamente o chamado.', 'Aceitou imediatamente.', 0, 'Duvidou e pediu sinais'),
        mc('O que Gideao pediu como sinal?', ['Um exercito','O orvalho no velo de la e na eira','Um anjo','Um rei'], 1, 'Juizes 6:37-40 - o velo de la na eira'),
    ]),
    ('Juízes 7: Os 300 Homens', 'Deus reduziu o exército de Gideão de 32 mil para 300, usando o método do rio. Com tochas, cântaros e trombetas, os 300 venceram os midianitas.', 'Juizes 7:1-25', 'Confiar que Deus vence com pouco', 'A vitória não depende do número, mas do poder de Deus.', [
        mc('De 32 mil para quantos Deus reduziu?', ['1000','300','100','50'], 1, '300 homens'),
        vf('Deus queria todos os 32 mil para lutar.', 'Queria todos os 32 mil.', 0, 'Reduziu para que Israel nao se vangloriasse'),
        mc('O que os 300 levaram?', ['Espadas e escudos','Torchas, cantaros e trombetas','Arco e flecha','Nada'], 1, 'Torchas, cantaros e trombetas'),
    ]),
    ('Juízes 13-16: Sansão', 'Sansão nasceu com força sobrenatural do Espírito do Senhor. Trabalhou incansavelmente contra os filisteus, mas foi traído por Dalila que descobriu o segredo do seu poder.', 'Juizes 13:1-16:31', 'Reconhecer que o poder vem de Deus e deve ser usado com sabedoria', 'A força de Sansão estava no cabelo, símbolo do voto nazireu. A perda do voto foi a perda do poder.', [
        mc('Qual era o segredo da forca de Sansao?', ['Os musculos','O voto nazireu e o cabelo','Uma armadura','Um amuleto'], 1, 'O voto nazireu, simbolizado pelo cabelo'),
        vf('Sansao nunca pecou.', 'Nunca pecou.', 0, 'Muitas vezes desobedeceu a Deus'),
        mc('Quem traiu Sansao?', ['Debora','Jael','Dalila','Rute'], 2, 'Dalila descobriu o segredo'),
    ]),
    ('Rute 1: Fidelidade de Rute', 'Rute, moabita, se recusou a deixar sua sogra Noemi: “O teu povo será o meu povo, e o teu Deus será o meu Deus.” Rute seguiu Noemi a Belém.', 'Rute 1:1-22', 'Entender a fidelidade e a lealdade no amor', 'Rute abriu mão de sua terra e seu povo para seguir a Deus e a sua sogra.', [
        mc('O que Ruth disse a Noemi?', ['Vou embora','O teu povo sera o meu povo','Odeio-te','Preciso de dinheiro'], 1, 'O teu povo sera o meu povo, o teu Deus sera o meu Deus'),
        vf('Rute era israelita.', 'Era israelita.', 0, 'Era moabita'),
        mc('Para onde Ruth e Noemi foram?', ['Egito','Belém','Ninive','Assiria'], 1, 'A Belém de Judá'),
    ]),
    ('Rute 2: No Campo de Boaz', 'Rute colhia espigas no campo de Boaz, um homem rico e parente de Noemi. Boaz mandou tratá-la bem e a protegeu.', 'Rute 2:1-23', 'Reconhecer a providência de Deus através de pessoas bondosas', 'Deus providenciou Boaz para proteger e sustentar Ruth e Noemi.', [
        mc('Quem era Boaz?', ['Um inimigo','Um parente rico e bondoso','Um sacerdote','O rei'], 1, 'Um parente rico e bondoso'),
        vf('Boaz expulsou Ruth do campo.', 'Expulsou Ruth do campo.', 0, 'Mandou tratá-la bem e a protegeu'),
        mc('O que Ruth fazia no campo?', ['Brincava','Colhia espigas','Dormia','Lutia'], 1, 'Colhia espigas'),
    ]),
    ('Rute 3-4: O Resgate', 'Boaz se ofereceu para ser o resgatador de Ruth, cumprindo a Lei do levirato. Casou-se com ela e eles foram ancestrais de Davi e de Jesus.', 'Rute 3:1-4:22', 'Entender que a providência de Deus se cumpre através de pessoas fiéis', 'A história de Ruth e Boaz é tipo da redenção: Deus sempre provê um resgatador.', [
        mc('O que Boaz fez por Ruth?', ['Rejeitou-a','Casou-se e foi seu resgatador','Expulsou-a','Ignorou-a'], 1, 'Casou-se com ela e foi resgatador'),
        vf('Rute e Boaz nao tiveram descendencia.', 'Nao tiveram descendencia.', 0, 'Foram ancestrais de Davi e de Jesus'),
        mc('De quem Ruth e Boaz foram ancestrais?', ['Moises','Abraao','Davi','Salomao'], 2, 'Obed, pai de Jessé, avo de Davi'),
    ]),
    ('Juízes 17-21: Anarquia', 'Na ausência de rei, Israel vivia em anarquia. Cada um fazia o que lhe parecia certo. A história do levita e sua concubina demonstra a depravação moral do período.', 'Juizes 17:1-21:25', 'Entender a necessidade de autoridade e de Deus como governante', 'O período dos juízes termina com caos moral. Israel precisa de um rei justo.', [
        mc('Qual era o lema do periodo?', ['Deus e rei','Cada um fazia o certo aos seus olhos','Nao havia pecado','O povo era santo'], 1, 'Cada um fazia o que lhe parecia certo'),
        vf('O livro de Juizes termina com paz.', 'Termina com paz.', 0, 'Termina com violencia e caos moral'),
        mc('O que a anarquia demonstra?', ['Que Deus nao existe','A necessidade de autoridade e de Deus','Que o povo e bom','Que a Lei e desnecessaria'], 1, 'A necessidade de um rei justo e de Deus como governante'),
    ]),
    ('Juízes 19: A Violência', 'Um levita entregou sua concubina a uma multidão perversa em Gibea para salvar a si mesmo. O que aconteceu chocou todo o Israel e levou à guerra civil.', 'Juizes 19:1-30', 'Reconhecer o extremo da queda humana sem Deus', 'A violência em Gibea é o momento mais sombrio de Juízes, mostrando a urgência de mudança.', [
        mc('O que o levita fez?', ['Lutou contra a multidão','Entregou a concubina','Fugiu','Orou'], 1, 'Entregou sua concubina a multidao'),
        vf('O episodio de Gibea nao teve consequencias.', 'Nao teve consequencias.', 0, 'Levou a guerra civil contra a tribo de Benjamim'),
        mc('O que Israel decidiu fazer?', ['Ignorar o fato','Declarar guerra a Benjamim','Perdoar','Mudar de terra'], 1, 'Declararam guerra a tribo de Benjamim'),
    ]),
], 50)
print("  Trilha 18 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 19 - Numeros e Deuteronomio
# ═══════════════════════════════════════════════
t19 = mk_trilha('Numeros e Deuteronomio', 'A jornada de Israel no deserto, a desobediencia, as leis de Moises e as ultimas instrucoes antes de entrar na Terra Prometida', 'adulto', 'iniciante', 19, 'straighten')
add_licoes(t19, [
    ('Números 13-14: Os Espiões', 'Moisés mandou 12 espias para Canaã. 10 voltaram com medo, dizendo que os cananeus eram gigantes. Apenas Josué e Calebe confiaram em Deus. O povo chorou e queria voltar ao Egito.', 'Numeros 13:1-14:45', 'Entender que a desobediência e o medo geram consequências severas', 'A incredulidade dos 10 espias fez todo o povo errar no deserto por 40 anos.', [
        mc('Quantos espias foram mandados?', ['7','10','12','15'], 2, '12 espias'),
        mc('Quais voltaram com otimismo?', ['Todos','10','Apenas Josue e Calebe','Nenhum'], 2, 'Apenas Josue e Calebe'),
        vf('Deus perdoou o povo sem nenhuma consequencia.', 'Deus perdoou sem consequencia.', 0, 'Condenou os 40 anos no deserto'),
        mc('Quanto tempo o povo ficou no deserto?', ['40 dias','40 meses','40 anos','10 anos'], 2, '40 anos'),
    ]),
    ('Números 20: A Rocha Golpeada', 'No deserto de Sinai, o povo reclamou da falta de água. Deus ordenou a Moisés que falasse com a rocha, mas Moisés golpeou a rocha duas vezes com a vara.', 'Numeros 20:1-13', 'Reconhecer que a desobediência tem consequências mesmo para líderes fiéis', 'Moisés não entrou na Terra Prometida por causa da sua desobediência na rocha.', [
        mc('O que Moises fez com a rocha?', ['Falou com ela','Golpeou-a duas vezes','Pediu ajuda','Orou sobre ela'], 1, 'Golpeou-a duas vezes'),
        vf('Moises entrou na Terra Prometida.', 'Entrou na Terra Prometida.', 0, 'Foi impedido por causa da desobediencia'),
        mc('O que a rocha representava?', ['A agua','O pecado','Cristo que seria ferido','Nada'], 2, 'Cristo que seria ferido uma vez'),
    ]),
    ('Números 21-22: A Serpente e Balaão', 'No deserto, serpentes venenosas atacaram Israel. Deus mandou Moisés fazer uma serpente de bronze; quem a olhasse vivia. Depois, Balaão foi contratado para amaldiçoar Israel.', 'Numeros 21:1-22:41', 'Entender o julgamento e a proteção divina simultâneas', 'A serpente de bronze é tipo de Cristo levantado. Balaão não pôde amaldiçoar o que Deus abençoou.', [
        mc('Por que serpentes atacaram Israel?', ['Porque oraram','Porque reclamaram contra Deus e Moises','Porque dormiram','Porque trabalharam'], 1, 'Reclamaram contra Deus e Moises'),
        mc('O que Moises fez para curar os picados?', ['Uma pomada','Uma serpente de bronze erguida','Uma oracao','Um sacrificio'], 1, 'Uma serpente de bronze erguida'),
        vf('Balaao conseguiu amaldicoar Israel.', 'Conseguiu amaldicoar.', 0, 'Deus transformou a amaldicao em bencao'),
        mc('De quem a serpente de bronze e tipo?', ['De Moises','De Jesus Cristo','De Balaao','De Josue'], 1, 'Jesus Cristo levantado na cruz'),
    ]),
    ('Números 32: Gade e Rúben', 'As tribos de Gade e Rúben pediram terra além do Jordão por terem muitos rebanhos. Moisés concordou com a condição de ajudar a conquistar a terra.', 'Numeros 32:1-42', 'Entender que privilégios trazem responsabilidades', 'Gade e Rúben receberam terra, mas tiveram que lutar primeiro com os outros.', [
        mc('O que Gade e Rubem pediram?', ['Voltar ao Egito','Terra alem do Jordao','Um rei','Tesoros'], 1, 'Terra alem do Jordao'),
        vf('Moises negou o pedido sem condicoes.', 'Negou sem condicoes.', 0, 'A condicao era ajudar a conquistar a terra primeiro'),
        mc('Por que pediram aquela terra?', ['Era bonita','Por causa dos seus grandes rebanhos','Porque la tinha ouro','Era perto do Egito'], 1, 'Por causa dos seus grandes rebanhos'),
    ]),
    ('Deuteronômio 6: O Shema', 'Ouve, Israel: o Senhor é o nosso Deus, o Senhor é um só. Amarás ao Senhor de todo o teu coração, de toda a tua alma e de todas as tuas forças.', 'Deuteronomio 6:1-9', 'Entender o mandamento central da fé israelita', 'O Shema é a declaração monoteísta mais importante de Israel.', [
        mc('O que o Shema declara?', ['Muitos deuses','O Senhor e um so','O homem e Deus','O diabo e forte'], 1, 'O Senhor e um so'),
        mc('Onde as palavras deviam estar?', ['Apenas no templo','No coracao, e nos bracos e portas','Apenas na mente','Em nenhum lugar'], 1, 'No coracao, nos bracos e nas portas'),
        vf('O Shema ensina polytheismo.', 'Enseina polytheismo.', 0, 'Ensina monotheismo - o Senhor e um so'),
    ]),
    ('Deuteronômio 8: Lembra do Senhor', 'Lembra-te de todo o caminho por onde o Senhor te conduziu no deserto, para te humilhar e para provares se guardas ou não os mandamentos.', 'Deuteronomio 8:1-20', 'Reconhecer que tudo vem de Deus e que devemos obedecer', 'Deus humilhou Israel no deserto para ensinar que não só de pão vive o homem.', [
        mc('Por que Deus conduziu Israel no deserto?', ['Para punir','Para humilhar e provar obediencia','Para recrear','Para matar'], 1, 'Para te humilhar e provar se guardas os mandamentos'),
        vf('Israel podia se gabar por sua forca.', 'Podia se gabar.', 0, 'Lembra de que tudo vem de Deus'),
        mc('O homem nao vive soe de:', ['Pao','Agua','Palavras de Deus','Dinheiro'], 0, 'Deuteronomio 8:3 - nao so de pao vive o homem, mas de toda palavra que sai da boca de Deus'),
    ]),
    ('Deuteronômio 28: Bênçãos e Pragas', 'Se ouvires a voz do Senhor, serás abençoado em tudo. Mas se não ouvires, virão pragas, fome, peste e exílio. A desobediência traz maldição.', 'Deuteronomio 28:1-68', 'Entender as consequências da obediência e da desobediência', 'A aliança traz bênçãos na obediência e pragas na desobediência.', [
        mc('Se Israel obedecesse, seria:', ['Apenas pobre','Abençoado em tudo','Igual aos outros','Irrelevante'], 1, 'Abencoado na cidade e no campo'),
        mc('Quais sao pragas mencionadas?', ['Chuva de pedras','Peste, fome, cegueira','Nuvens coloridas','Nada mau'], 1, 'Peste, fome e exilio'),
        vf('As pragas sao eternas e irreversiveis.', 'Sao eternas.', 0, 'Ha arrependimento e restauracao possiveis'),
        mc('A maldicao caia sobre quem?', ['Apenas reis','Apenas sacerdotes','Aquele que nao ouvir a voz do Senhor','Ninguem'], 2, 'Aquele que nao ouvir a voz do Senhor'),
    ]),
    ('Deuteronômio 30: Vida e Morte', 'Propus diante de ti a vida e a morte, a bênção e a maldição. Escolhe a vida para que vivas tu e a tua descendência, amando o Senhor teu Deus.', 'Deuteronomio 30:1-20', 'Fazer a escolha pela vida em Deus', 'Deus apresenta a escolha: vida com Deus ou morte sem Ele.', [
        mc('O que Deus propõe?', ['Apenas a morte','Vida e morte, bencao e maldicao','Nada','Apenas o sofrimento'], 1, 'A vida e a morte, a bencao e a maldicao'),
        vf('O homem nao pode escolher.', 'Nao pode escolher.', 0, 'Escolhe a vida'),
        mc('O que Deus pede?', ['Odiar a vida','Ama-me de todo o coracao','Ignorar','Nao escolher'], 1, 'Ama-me de todo o teu coracao'),
    ]),
    ('Deuteronômio 34: A Morte de Moisés', 'Moisés subiu ao monte Nebo e viu toda a terra prometida. Morreu ali aos 120 anos, ainda com a vista boa e a força inteira. Nenhum profeta se levantou como ele.', 'Deuteronomio 34:1-12', 'Honrar a liderança de Moisés e a soberania de Deus', 'Moisés viu a terra mas não entrou. Deus cumpriu Sua palavra.', [
        mc('De onde Moises viu a terra?', ['Monte Sinai','Monte Nebo','Monte Carmelo','Monte das Oliveiras'], 1, 'Monte Nebo'),
        vf('Moises entrou na Terra Prometida.', 'Entrou na terra.', 0, 'Apenas a viu de longe'),
        mc('Quantos anos Moises tinha ao morrer?', ['80','100','120','150'], 2, '120 anos'),
    ]),
    ('Deuteronômio 1-2: Relembrando', 'Moisés relembrando o caminho de Israel: a saída do Egito, a Lei no Sinai, as provas no deserto e a proximidade da Terra Prometida.', 'Deuteronomio 1:1-2:1', 'Reconhecer a fidelidade de Deus ao longo da jornada', 'O Deuteronômio e o discurso final de Moisés, resumindo tudo que Deus fez.', [
        mc('O que Moises faz no Deuteronomio?', ['Reclama','Relembrar tudo que Deus fez','Guarda silencio','Ouve o povo'], 1, 'Relembrar tudo que Deus fez'),
        vf('O Deuteronomio e um livro de louvor.', 'E um livro de louvor.', 0, 'E um discurso de Moises relembrando e instruindo'),
        mc('Onde Israel estava quando Moises falou?', ['No Egito','No deserto, perto da Terra Prometida','Na terra prometida','Na Babilonia'], 1, 'No deserto, perto da terra prometida'),
    ]),
], 50)
print("  Trilha 19 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 20 - Isaias e Jeremias: Profecias
# ═══════════════════════════════════════════════
t20 = mk_trilha('Isaias e Jeremias Profecias', 'As profecias mais profundas do AT sobre o Servo Sofredor, a Nova Alianca, o juizo e o consolo de Deus', 'adulto', 'avancado', 20, 'auto_stories')
add_licoes(t20, [
    ('Isaías 1: A Acusação', 'O Senhor acusa Israel: reconheci filhos, mas me rebelaram. Não há integridade, apenas feridas. Seus sacrifícios me saciaram. Lavai-vos, purificai-vos.', 'Isaias 1:1-20', 'Entender a exigência de justiça e não apenas de rituais', 'Deus rejeita a religiosidade vazia sem justiça e misericórdia.', [
        mc('O que Deus acusa Israel de fazer?', ['Orar muito','Rebelar-se e ter feridas sem integridade','Ser perfeito','Não ter pecados'], 1, 'Rebelaram-se, nao ha integridade'),
        vf('Deus aceita sacrificios de quem pratica injustica.', 'Aceita sacrificios de injustos.', 0, 'Rejeita seus sacrificios como fumaca'),
        mc('O que Deus pede?', ['Mais sacrificios','Lavai-vos e purificai-vos','O silencio','Mais ofertas'], 1, 'Lavai-vos, purificai-vos'),
    ]),
    ('Isaías 6: O Chamado de Isaías', 'Isaías viu o Senhor assentado no trono, com as barbas enchendo o templo. Seráfins clamavam: Santo, Santo, Santo. Isaías disse: Ai de mim! Um seráfim tocou seus lábios com brasa.', 'Isaias 6:1-13', 'Reconhecer a santidade de Deus e a reação do homem pecador', 'A visão da santidade de Deus leva à consciência do pecado e ao chamado profético.', [
        mc('O que os serafins cantavam?', ['Aleluia','Santo, Santo, Santo','Amém','Glória'], 1, 'Santo, Santo, Santo'),
        mc('O que Isaias disse ao ver Deus?', ['Estou seguro','Ai de mim, sou pecador','Sou perfeito','Obrigado'], 1, 'Ai de mim! Perecerei, porque sou homem de labios impuros'),
        vf('Isaias ja era sacerdote quando viu a visao.', 'Ja era sacerdote.', 0, 'Era um homem comum que recebeu o chamado'),
        mc('O que um serafim fez?', ['Abraçou Isaias','Tocou seus labios com brasa','Deu-lhe um livro','Matou-o'], 1, 'Tocou seus labios com brasa do altar'),
    ]),
    ('Isaías 9: O Príncipe da Paz', 'Para nós nasceu uma criança, para nós foi dado um filho; e o principado estará sobre os seus ombros. Conselheiro maravilhoso, Deus fortíssimo, Pai eterno, Príncipe da Paz.', 'Isaias 9:1-7', 'Reconhecer Jesus como o Messias prometido', 'Isaías profetizou a vinda de um governante perfeito cujo reinado seria eterno.', [
        mc('Como sera chamado o filho?', ['Principe da Guerra','Principe da Paz','Principe do Medo','Principe da Treva'], 1, 'Principe da Paz'),
        vf('O governo desse filho sera temporario.', 'Sera temporario.', 0, 'O Seu governo sera eterno - Isaias 9:7'),
        mc('Quantos titulos o filho recebe?', ['2','3','4','6'], 2, 'Conselheiro, Deus Fortissimo, Pai Eterno, Principe da Paz'),
    ]),
    ('Isaías 40: Consolo', 'Consolai, consolai o meu povo, diz o vosso Deus. Fala ao coração de Jerusalém, porque a sua servidão já acabou. Todo ser humano é como a erva.', 'Isaias 40:1-31', 'Receber o consolo de Deus na tribulação', 'Deus consola Seu povo e renova as forças dos que nele esperam.', [
        mc('O que Deus manda fazer?', ['Punir','Consolai o meu povo','Destruir','Esquecer'], 1, 'Consolai, consolai o meu povo'),
        vf('Os fortes nunca se cansam.', 'Os fortes nunca cansam.', 0, 'Todo ser humano e como a erva'),
        mc('Mas aqueles que esperam no Senhor:', ['Cansam-se','Sao renovados em forcas','Desistem','Morrem'], 1, 'Renovam as forcas, sobem com asas como aguias'),
    ]),
    ('Isaías 53: O Servo Sofredor', 'Ele foi desprezado e rejeitado pelos homens, homem de doenças. Foi traspassado pelas nossas transgressões, moído pelas nossas iniquidades. Pela sua chaga fomos sarados.', 'Isaias 53:1-12', 'Reconhecer Jesus como o Servo Sofredor profetizado', 'A profecia mais clara sobre a morte expiatória de Jesus, escrita 700 anos antes da cruz.', [
        mc('O que o Servo Sofredor carregou?', ['O mundo','As nossas doencas e transgressoes','O ouro','Nada'], 1, 'As nossas transgressoes e iniquidades'),
        vf('O servo foi aceito e honrado pelos homens.', 'Foi aceito.', 0, 'Foi desprezado e rejeitado'),
        mc('Pela sua chaga fomos:', ['Destruidos','Mortos','Sarados','Esquecidos'], 2, 'Pela sua chaga fomos sarados'),
    ]),
    ('Isaías 61: Boas Novas', 'O espírito do Senhor está sobre mim, porque o Senhor me ungiu para pregar boas novas aos pobres, para curar os quebrantados de coração, proclamar liberdade aos cativos.', 'Isaias 61:1-3', 'Reconhecer que Jesus cumpriu esta profecia', 'Jesus leu esta passagem na sinagoga e disse: Hoje se cumpriu.', [
        mc('O que o Senhor ungiu o servo para fazer?', ['Destruir','Pregar boas novas e curar','Castigar','Silenciar'], 1, 'Pregar boas novas aos pobres e curar os quebrantados'),
        vf('Jesus se recusou a ler esta passagem na sinagoga.', 'Recusou.', 0, 'Leu e disse: Hoje se cumpriu esta profecia'),
        mc('As boas novas sao para:', ['Apenas ricos','Os pobres e quebrantados','Apenas reis','Os pecadores apenas'], 1, 'Aos pobres e aos quebrantados de coracao'),
    ]),
    ('Jeremias 1: O Chamado', 'Antes de te formar no ventre, eu te conheci e te consagrei. Não digas: sou menino, porque onde eu te enviar, irás, e o que eu te mandar, dirás.', 'Jeremias 1:1-19', 'Entender que Deus chama desde antes do nascimento', 'Jeremias foi chamado jovem, mas Deus o capacitou.', [
        mc('Quando Deus conheceu Jeremias?', ['Apos nascer','Antes de nascer no ventre','Na juventude','Nunca'], 1, 'Antes de te formar no ventre'),
        vf('Jeremias aceitou o chamado imediatamente.', 'Aceitou imediatamente.', 0, 'Disse que era menino e nao sabia falar'),
        mc('O que Deus prometeu?', ['Abandoná-lo','Estou contigo para livrar-te','Ignorá-lo','Castigá-lo'], 1, 'Estou contigo para livrar-te'),
    ]),
    ('Jeremias 29: Planos de Bem', 'Porque eu bem sei os pensamentos que tenho a vosso respeito, pensamentos de paz e não de mal, para vos dar o fim que esperais. Clamai a mim, e responderei.', 'Jeremias 29:11-14', 'Confiar nos planos de Deus mesmo na dificuldade', 'Deus falou ao povo exilado na Babilônia: Ele tinha planos de bem.', [
        mc('O que Deus pensa para o Seu povo?', ['Mal e destruicao','Paz e bem, fim esperado','Silencio','Esquecimento'], 1, 'Pensamentos de paz e nao de mal'),
        vf('Deus planejava destruir o povo para sempre.', 'Planejava destruir.', 0, 'Pensamentos de paz para dar fim esperado'),
        mc('O que Deus diz que devemos fazer?', ['Fugir','Desistir','Clamar a Ele e Ele respondera','Nao fazer nada'], 2, 'Clamai a mim e eu responderei'),
    ]),
    ('Jeremias 31: A Nova Aliança', 'Farei uma aliança nova com Israel. Porei a minha Lei no seu interior e a escreverei nos seus corações. Perdoarei as iniquidades deles.', 'Jeremias 31:31-34', 'Entender o fundamento da nova aliança em Cristo', 'A nova aliança é interior e pessoal, não baseada em tábuas de pedra.', [
        mc('Onde Deus escreveria Sua Lei?', ['Em pedras','No papel','No coracao dos homens','No chao'], 2, 'No coracao dos homens'),
        vf('A nova alianca seria apenas para Israel.', 'Seria apenas para Israel.', 0, 'Estende-se a todos que creem'),
        mc('O que Deus faria com os pecados?', ['Aumentar','Perdoar e nao mais lembrar','Esconder','Ignorar'], 1, 'Perdoarei as iniquidades e nao mais me lembrarei'),
    ]),
    ('Lamentações 3: Misericórdias', 'As misericórdias do Senhor não se esgotam; são novas a cada manhã. Grande é a fidelidade do Senhor. O Senhor não rejeita para sempre.', 'Lamentacoes 3:22-33', 'Renovar a esperança nas misericórdias renovadas de Deus', 'Mesmo na destruição de Jerusalém, há esperança nas misericórdias de Deus.', [
        mc('As misericordias de Deus sao:', ['Velhas e esgotadas','Novas a cada manha','Inexistentes','Limitadas'], 1, 'Novas a cada manha'),
        vf('Deus rejeita para sempre.', 'Rejeita para sempre.', 0, 'O Senhor nao rejeita para sempre'),
        mc('Grande e:', ['O dinheiro','A fidelidade do Senhor','O pecado','O mundo'], 1, 'A fidelidade do Senhor'),
    ]),
], 50)
print("  Trilha 20 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 21 - Criancas: Historias do AT
# ═══════════════════════════════════════════════
t21 = mk_trilha('Criancas: Historias do AT', 'Historias do Antigo Testamento adaptadas para criancas: da Criacao ao Exodo, com lições de fé e obediencia', 'crianca', 'iniciante', 21, 'child_care')
add_licoes(t21, [
    ('Criação: Deus fez tudo', 'Deus criou o céu e a terra, os animais, as estrelas e você também! Tudo que é bonito veio de Deus. Ele é poderoso e bom.', 'Genesis 1:1-31', 'Amar a Deus como criador de todas as coisas', 'Deus fez tudo com amor, inclusive você!', [
        mc('Quem criou tudo?', ['Deus','O homem','A natureza','A sorte'], 0, 'Genesis 1:1 - Deus criou os ceus e a terra'),
        mc('O que Deus criou no quinto dia?', ['Os animais','Os peixes e as aves','O homem','As plantas'], 1, 'Genesis 1:21 - peixes e aves'),
        vf('Deus fez apenas coisas ruins.', 'Fez apenas coisas ruins.', 0, 'Tudo que Deus fez era muito bom'),
    ]),
    ('Noé e a Arca', 'Deus mandou Noé construir uma arca enorme. Noé obedeceu e levou sua família e os animais. Depois veio o dilúvio, mas Deus protegeu a todos.', 'Genesis 6:1-9:17', 'Obedecer a Deus mesmo quando é difícil', 'Noé confiou em Deus e foi salvo junto com sua família.', [
        mc('Por que Noe construiu a arca?', ['Por diversao','Porque Deus mandou','Porque choveu muito','Porque era bom'], 1, 'Genesis 6 - porque Deus mandou'),
        mc('Quantos dias choveu?', ['7','20','30','40'], 3, 'Genesis 7:12 - quarenta dias e quarenta noites'),
        vf('Deus esqueceu de Noe na arca.', 'Esqueceu de Noe.', 0, 'Deus lembrou-se de Noe e de todos os que estavam na arca'),
    ]),
    ('Abraão Viajou', 'Deus disse a Abraão: Vai-te da tua terra! Abraão obedeceu e foi para uma terra desconhecida. Deus prometeu fazer dele um grande povo.', 'Genesis 12:1-9', 'Confiar em Deus quando não sabemos o caminho', 'Abraão seguiu Deus sem saber para onde ia. Essa é fé!', [
        mc('Para onde Deus mandou Abrao?', ['Para o Egito','Para uma terra que Ele mostraria','Para o mar','Para o ceu'], 1, 'Genesis 12:1 - para a terra que eu te mostrarei'),
        vf('Abrao levou um mapa.', 'Levou um mapa.', 0, 'Foi pela fe, sem saber para onde ia'),
        mc('O que Deus prometeu a Abrao?', ['Riqueza apenas','Fazer dele grande povo','Morre cedo','Nada'], 1, 'Fazer dele uma grande nação'),
    ]),
    ('José Sonhou', 'José era o filho favorito do pai Jacó. Seus irmãos tinham inveja porque José contou seus sonhos de que seriam seus servos. Isso fez os irmãos ficarem com raiva.', 'Genesis 37:1-36', 'Não ter inveja e perdoar', 'Mesmo com a injustiça, Deus estava no controle.', [
        mc('Por que os irmaos ficaram com raiva?', ['Jose era feio','Jose era favorito e contou sonhos de grandeza','Jose nao trabalhava','Jose era mau'], 1, 'Jose era favorito e contou seus sonhos'),
        vf('Jose inventou os sonhos.', 'Inventou os sonhos.', 0, 'Deus deu os sonhos a Jose'),
        mc('O que os irmaos fizeram com Jose?', ['Abracaram-no','Venderam-no como escravo','Daram presentes','Levaram-no ao pai'], 1, 'Venderam-no como escravo'),
    ]),
    ('José no Palácio', 'No Egito, José foi preso injustamente, mas Deus o ajudou. Ele interpretou sonhos do faraó e foi tornado governador do Egito inteiro.', 'Genesis 41:1-46', 'Deus está no controle mesmo quando as coisas parecem ruins', 'Deus transformou a prisão em governança.', [
        mc('O que Jose fez no Egito?', ['Serviu sempre como escravo','Interpretou sonhos e foi governador','Morreu','Fugiu'], 1, 'Interpretou sonhos do farao e foi governador'),
        vf('Jose ficou preso para sempre.', 'Ficou preso para sempre.', 0, 'Foi libertado e tornado governador'),
        mc('Quem deu a Jose poder?', ['O farao sozinho','Deus atraves do farao','Os amigos','Ninguem'], 1, 'Deus prepare tudo para Jose'),
    ]),
    ('José Abraçou', 'José revelou sua identidade aos irmãos: Eu sou José! Chorou e os abraçou. Disse: Vocês quiseram me fazer mal, mas Deus transformou em bem.', 'Genesis 45:1-15', 'Perdoar e ver a mão de Deus nas situações ruins', 'O perdão de José é um dos mais lindos exemplos da Bíblia.', [
        mc('Como Jose reagiu aos irmaos?', ['Castigou-os','Perdoou-os e abracou-os','Expulsou-os','Cobrou dinheiro'], 1, 'Perdoou-os e abracou-os'),
        vf('Jose nunca chorou ao ver os irmaos.', 'Nunca chorou.', 0, 'Chorou muito e os abracou'),
        mc('O que Jose disse sobre o que aconteceu?', ['Foi mau','Deus transformou em bem','Voce tem razao','Nao importa'], 1, 'Deus o fez para bem'),
    ]),
    ('José Perdoou', 'Quando o pai Jacó morreu, os irmãos tiveram medo. José disse: Não tenham medo, eu sou de Deus para cuidar de vocês. Perdoou-os totalmente.', 'Genesis 50:15-21', 'O perdão total e o amor que transforma', 'José perdoou de verdade, sem guardar rancor.', [
        mc('O que os irmaos temeram apos a morte do pai?', ['Perder dinheiro','Que Jose se vingasse','Que morressem','Que Jose fugisse'], 1, 'Que Jose se vingasse'),
        vf('Jose guardou rancor dos irmaos.', 'Guardou rancor.', 0, 'Perdoou totalmente sem guardar nada'),
        mc('O que Jose disse?', ['Vou castigar','Nao tenham medo, eu sou de Deus para cuidar de voces','Fujam','Sumam'], 1, 'Nao tenham medo, eu sou de Deus para cuidar de voces'),
    ]),
    ('Moisés Bebê Salvo', 'Uma mãe hebreia escondeu o bebê Moisés num cesto no Nilo. A filha do faraó o encontrou e criou-o no palácio. Deus cuidou de Moisés.', 'Exodo 2:1-10', 'Deus protege seus desde o nascimento', 'A mãe de Moisés confiou em Deus e Ele cuidou do bebê.', [
        mc('Onde a mae escondeu Moises?', ['Em casa','Num cesto no Nilo','No deserto','Na floresta'], 1, 'Num cesto no Nilo'),
        vf('Moises cresceu pobre e sozinho.', 'Cresceu pobre.', 0, 'Foi criado no palacio do farao'),
        mc('Quem encontrou Moises?', ['Uma pastora','A filha do farao','Uma escrava','Um soldado'], 1, 'A filha do farao'),
    ]),
    ('Mar Vermelho', 'Moisés levou Israel pelo deserto. O faraó mandou exército atrás deles. Moisés ergueu a vara e o Mar Vermelho se abriu! Israel passou em seco.', 'Exodo 14:1-31', 'Deus salva o Seu povo dos perigos', 'O Mar Vermelho é o maior milagre de salvação do AT!', [
        mc('Como Israel passou o mar?', ['Nadando','Em barcos','O mar se abriu e passaram em seco','Por ponte'], 2, 'O mar se abriu e passaram em seco'),
        vf('Todos os israelitas se afogaram.', 'Todos se afogaram.', 0, 'Israel passou em salvo'),
        mc('O que aconteceu com o exercito do farao?', ['Fugiu','Foi engolido pelo mar','Venceu','Desistiu'], 1, 'Foi engolido pelas aguas do mar'),
    ]),
    ('Dez Mandamentos', 'Deus deu dez regras para o povo no monte Sinai. A primeira é: Ame a Deus acima de tudo. As outras ensinam a amar o próximo.', 'Exodo 20:1-17', 'Obedecer a Deus e amar ao próximo', 'Os mandamentos são as regras de Deus para nosso bem.', [
        mc('Onde Deus deu os mandamentos?', ['No deserto','No monte Sinai','Na cidade','No mar'], 1, 'No monte Sinai'),
        mc('Qual e o primeiro mandamento?', ['Nao matar','Ame a Deus acima de tudo','Nao furte','Honre os pais'], 1, 'Ame a Deus acima de tudo'),
        vf('Deus deu 10 mandamentos apenas.', 'Deu apenas 10.', 0, 'Deu 10 mandamentos principais'),
    ]),
], 50)
print("  Trilha 21 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 22 - Criancas: Historias de Jesus
# ═══════════════════════════════════════════════
t22 = mk_trilha('Criancas: Historias de Jesus', 'O nascimento, a vida, os milagres, os ensinamentos e a ressurreição de Jesus, contados para criancas', 'crianca', 'iniciante', 22, 'child_friendly')
add_licoes(t22, [
    ('O Nascimento de Jesus', 'Jesus nasceu numa manjedoura em Belém. Anjos anunciaram o nascimento aos pastores. Reis vieram do oriente para adorá-lo. O mundo celebrou o nascimento do Salvador.', 'Mateus 1:18-2:12', 'Celebrar o nascimento de Jesus como presente de Deus', 'Jesus veio ao mundo para salvar todos nós!', [
        mc('Onde Jesus nasceu?', ['Num palacio','Numa manjedoura','Num templo','Na praia'], 1, 'Numa manjedoura em Betlem'),
        mc('Quem primeiro ouviu a noticia?', ['Os reis','Os pastores','Os fariseus','Os romanos'], 1, 'Os pastores no campo'),
        vf('Jesus nasceu num palacio enorme.', 'Nasceu num palacio.', 0, 'Nasceu numa manjedoura, porque nao havia lugar'),
    ]),
    ('O Batismo de Jesus', 'Jesus foi batizado por João Batista no Rio Jordão. Ao subir das águas, o céu se abriu e o Espírito Santo desceu como pomba. Uma voz do céu disse: Este é o Meu Filho amado.', 'Mateus 3:13-17', 'Entender que Jesus é o Filho de Deus', 'Deus confirmou que Jesus é o Seu Filho amado.', [
        mc('Quem baptizou Jesus?', ['Pedro','Joao Batista','Paulo','Moises'], 1, 'Joao Batista'),
        mc('O que desceu do ceu?', ['Chuva','Uma pomba','Uma estrela','Fogo'], 1, 'O Espirito Santo como pomba'),
        vf('Jesus precisava de batismo por ter pecado.', 'Tinha pecado.', 0, 'Jesus era sem pecado, foi para cumprir toda justica'),
    ]),
    ('A Tentação de Jesus', 'Jesus foi ao deserto e o diabo tentou Ele. Jesus resistiu a cada tentação usando a Palavra de Deus. O diabo foi embora.', 'Mateus 4:1-11', 'Usar a Palavra de Deus para resistir ao mal', 'Jesus nos mostra que podemos vencer as tentações.', [
        mc('Quem tentou Jesus?', ['Um fariseu','O diabo','Um soldado','Um amigo'], 1, 'O diabo no deserto'),
        mc('O que Jesus usou para resistir?', ['Uma espada','A Palavra de Deus','Dinheiro','Forca'], 1, 'A Palavra de Deus - esta escrito'),
        vf('Jesus cedeu a tentacao.', 'Cedeu.', 0, 'Jesus resistiu e venceu o diabo'),
    ]),
    ('O Sermão da Montanha', 'Jesus ensinou as pessoas numa montanha. Disse: Bem-aventurados os mansos, os que choram, os que têm fome de justiça. Vocês são a luz do mundo.', 'Mateus 5:1-48', 'Aprender os ensinamentos de Jesus', 'Jesus ensina a viver com amor, humildade e justiça.', [
        mc('Quem sao bem-aventurados?', ['Os ricos','Os mansos e os que choram','Os fortes','Os famosos'], 1, 'Os mansos, os que choram, os que tem fome de justica'),
        vf('Jesus disse para sermos ruins com os outros.', 'Disse para ser ruins.', 0, 'Jesus disse: amai uns aos outros'),
        mc('Voces sao a:', ['Treva','Luz do mundo','Nada','Ouvidores apenas'], 1, 'Luz do mundo'),
    ]),
    ('Jesus Cura', 'Jesus andou por toda parte curando enfermos. Curou cegos, coxos e até levantou mortos. Ele tinha compaixão de todos.', 'Mateus 9:1-38; Lucas 4:40', 'Amar e cuidar dos que precisam', 'Jesus cura porque ama cada pessoa.', [
        mc('O que Jesus fazia com os enfermos?', ['Ignorava','Curava com amor','Brincava','Dormia'], 1, 'Curava com amor e compaixao'),
        vf('Jesus so curava gente importante.', 'So curava gente importante.', 0, 'Curava a todos que pediam'),
        mc('Quem Jesus curou?', ['Cegos, coxos e enfermos','Apenas reis','Apenas sacerdotes','Ninguem'], 0, 'Curou cegos, coxos, enfermos e ate mortos'),
    ]),
    ('As Parábolas', 'Jesus contou histórias para ensinar: o Semeador, a Ovelha Perdida, o Filho Pródigo. Cada parábola ensina algo importante sobre o Reino de Deus.', 'Mateus 13:1-58', 'Prestar atenção nos ensinamentos de Jesus', 'As parábolas são histórias com lições profundas.', [
        mc('O que a semente no Semeador representa?', ['Dinheiro','A Palavra de Deus','Animais','O governo'], 1, 'A Palavra de Deus'),
        mc('Quantas ovelhas o pastor tinha?', ['99','100','50','200'], 1, '100, e procurou a que faltava'),
        vf('As parabolas sao historias verdadeiras.', 'Sao historias verdadeiras.', 0, 'Sao historias que ensinam verdades de Deus'),
    ]),
    ('Pão e Peixes', 'Jesus alimentou 5 mil pessoas com 5 pães e 2 peixes. Ele multiplicou a comida. Todos ficaram satisfeitos e sobrou!', 'Mateus 14:13-21', 'Confiar que Jesus supre todas as nossas necessidades', 'Com Jesus, o pouco se torna muito!', [
        mc('Quantas pessoas Jesus alimentou?', ['100','500','5 mil','10 mil'], 2, 'Cinco mil homens, sem contar mulheres e criancas'),
        mc('Quantos pães e peixes tinham?', ['2 pães 1 peixe','5 pães 2 peixes','3 pães 3 peixes','10 pães 10 peixes'], 1, 'Cinco pães e dois peixes'),
        vf('Jesus nao conseguiu alimentar a todos.', 'Nao conseguiu.', 0, 'Multiplicou e sobrou!',
),
    ]),
    ('Jesus Ressuscitou', 'Jesus morreu na cruz para nos salvar. No terceiro dia, Ele ressuscitou! A tumba ficou vazia. Jesus vive e isso muda tudo!', 'Mateus 28:1-20', 'Celebrar a ressurreição de Jesus e ter esperança', 'Jesus venceu a morte! Isso é a melhor notícia do mundo!', [
        mc('Quando Jesus ressuscitou?', ['No primeiro dia','No terceiro dia','No setimo dia','No quadragésimo dia'], 1, 'No terceiro dia'),
        mc('O que as mulheres encontraram na tumba?', ['O corpo de Jesus','A tumba vazia','Um anjo mau','Nada'], 1, 'A tumba vazia!'),
        vf('Jesus morreu e nao voltou.', 'Nao voltou.', 0, 'Ressuscitou e vive para sempre!'),
    ]),
    ('Pastores Adoraram', 'Pastores estavam no campo quando anjos apareceram e disseram: Nasceu em Belém o Salvador! Os pastores foram adorar o bebê Jesus.', 'Lucas 2:8-20', 'Adorar a Jesus com alegria', 'Os pastores foram os primeiros a adorar Jesus.', [
        mc('Onde os pastores estavam?', ['No templo','No campo','Em casa','No palacio'], 1, 'No campo, cuidando das ovelhas'),
        mc('Quem anunciou o nascimento?', ['Os reis','Os anjos','Os fariseus','O povo'], 1, 'Os anjos do ceu'),
        vf('Os pastores ignoraram a noticia.', 'Ignoraram.', 0, 'Foram rapidamente adorar o bebe'),
    ]),
    ('O Filho Pródigo', 'Um filho pediu sua parte e foi embora. Gastou tudo e ficou com fome. Voltou pedindo perdão. O pai o recebeu com abraços e festa!', 'Lucas 15:11-32', 'Que Deus sempre nos recebe de volta', 'Não importa o que fizemos, Deus nos ama e nos recebe!', [
        mc('O que o filho fez?', ['Ficou em casa','Gastou tudo e voltou pedindo perdao','Morreu','Matou'], 1, 'Gastou tudo e voltou para o pai'),
        vf('O pai ficou com raiva quando o filho voltou.', 'Ficou com raiva.', 0, 'O pai correu e o abracou'),
        mc('O que o pai fez?', ['Expulsou','Festou e recebeu com alegria','Castigou','Ignorou'], 1, 'Fez festa e o recebeu com alegria'),
    ]),
], 50)
print("  Trilha 22 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 23 - Adolescentes: Quem e Jesus?
# ═══════════════════════════════════════════════
t23 = mk_trilha('Adolescentes: Quem e Jesus?', 'Descobrindo Jesus atraves dos evangelhos: sua identidade, poder, ensinamentos e chamado para seguir', 'adolescente', 'iniciante', 23, 'psychology_alt')
add_licoes(t23, [
    ('João 1: Verbo Feito Carne', 'No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus. Tudo foi feito por Ele. E o Verbo se fez carne e habitou entre nós.', 'João 1:1-18', 'Entender que Jesus é eterno e divino', 'Jesus não começou a existir no nascimento. Ele é o Verbo eterno.', [
        mc('O que e o Verbo?', ['Uma pessoa comum','Jesus Cristo, eterno e divino','Um profeta','Um livro'], 1, 'Jesus Cristo, o Verbo eterno'),
        vf('O Verbo comecou a existir quando Jesus nasceu.', 'Comecou a existir no nascimento.', 0, 'No principio era o Verbo - eterno'),
        mc('O que Jesus trouxe ao mundo?', ['Lei nova','Graça e verdade','Castigo','Destruicao'], 1, 'João 1:17 - graça e verdade vieram por Jesus'),
    ]),
    ('João 3: Nascer de Novo', 'Jesus disse a Nicodemos: É necessário nascer de novo para ver o Reino de Deus. Quem crer no Filho não perece, mas tem a vida eterna.', 'João 3:1-36', 'Entender a necessidade do novo nascimento espiritual', 'Nascemos de novo pelo Espírito Santo.', [
        mc('Com quem Jesus conversou?', ['Pedro','Nicodemos','Paulo','Joao'], 1, 'Com Nicodemos, fariseu de noite'),
        vf('Jesus disse que precisamos nascer apenas uma vez.', 'Precisamos nascer uma vez.', 0, 'Precisamos nascer de novo - segundo nascimento'),
        mc('Qual versiculo e o mais conhecido?', ['Mateus 6:33','João 3:16','Romanos 8:28','Salmo 23'], 1, 'João 3:16 - Deus amou o mundo de tal forma'),
    ]),
    ('João 4: A Samaritana', 'Jesus falou com uma mulher samaritana no poço de Jacó. Ela tinha 5 maridos. Jesus revelou que era o Messias. Ela correu e contou tudo.', 'João 4:1-42', 'Jesus não rejeita ninguém', 'Jesus quebrou barreiras de cultura e gênero para falar com ela.', [
        mc('Onde Jesus falou com a samaritana?', ['No templo','No poço de Jaco','Na praia','Numa montanha'], 1, 'No poço de Jaco'),
        vf('Jesus se recusou a falar com ela.', 'Recusou.', 0, 'Falou, bebeu agua e revelou que era o Messias'),
        mc('Quantos maridos a mulher teve?', ['1','3','5','7'], 2, 'Teve 5 maridos'),
    ]),
    ('Marcos 1: O Chamado', 'Jesus chamou seus primeiros discípulos: Venham e segui-me. Eles deixaram tudo e o seguiram. Jesus tinha autoridade diferente dos escribas.', 'Marcos 1:1-20', 'Entender o que significa seguir a Jesus', 'Seguir Jesus e deixar tudo e ir com Ele.', [
        mc('O que Jesus disse aos discipulos?', ['Fiquem ricos','Venham e sigam-me','Fujam','Durmam'], 1, 'Venham e sigam-me'),
        vf('Os discipulos levaram dias para decidir.', 'Levaram dias.', 0, 'Na hora deixaram tudo e o seguiram'),
        mc('O que os discipulos fizeram?', ['Ignoraram','Deixaram tudo e o seguiram','Dormiram','Riram'], 1, 'Deixaram tudo e o seguiram'),
    ]),
    ('Marcos 4: A Tempestade', 'Jesus dormia no barco quando uma tempestade surgiu. Os discípulos o acordaram. Jesus disse: Acalma-te! E o mar se acalmou.', 'Marcos 4:35-41', 'Jesus tem poder sobre tudo', 'Mesmo na tempestade, Jesus está no controle.', [
        mc('O que Jesus fazia quando a tempestade arose?', ['Orava','Dormia','Lutava','Nadava'], 1, 'Dormia no barco'),
        vf('Jesus ficou com medo da tempestade.', 'Ficou com medo.', 0, 'Jesus e Senhor de tudo, inclusive do mar'),
        mc('O que Jesus disse ao mar?', ['Acalma-te','Sai','Morre','Vai embora'], 0, 'Acalma-te, cala-te! E o mar se acalmou'),
    ]),
    ('Marcos 8: O Cego', 'Jesus colocou lama nos olhos de um cego e perguntou: Que vês? O homem disse: Vejo pessoas como árvores. Jesus tocou novamente e ele via perfeitamente.', 'Marcos 8:22-26', 'Jesus cura completamente', 'Jesus não faz nada pela metade. Ele quer curar totalmente.', [
        mc('O que Jesus colocou nos olhos do cego?', ['Agua','Oleo','Lama','Sangue'], 2, 'Lama misturada com saliva'),
        vf('O cego enxergou perfeitamente de primeira.', 'Enxergou de primeira.', 0, 'Jesus tocou duas vezes, ate ver completamente'),
        mc('Jesus perguntou:', ['Quem és?','Que vêes?','Onde vais?','O que fazes?'], 1, 'Que vêes?'),
    ]),
    ('Lucas 9: Discipulado', 'Jesus disse: Se alguém quiser vir após mim, negue a si mesmo, tome a sua cruz e siga-me. De que aproveita ganhar o mundo e perder a si mesmo?', 'Lucas 9:23-25', 'Entender o custo e a alegria de seguir Jesus', 'Seguir Jesus exige dedicação total, mas traz vida eterna.', [
        mc('O que Jesus pede a quem quer segui-lo?', ['Ser rico','Negar a si mesmo e tomar a cruz','Dormir','Viajar'], 1, 'Negue a si mesmo, tome a sua cruz'),
        vf('Jesus quer que sejamos ricos antes de segui-lo.', 'Quer riquezas.', 0, 'Quer que O sigamos acima de tudo'),
        mc('De que aproveita ganhar o mundo?', ['Tudo','Nada se perder a si mesmo','Muito','Apenas um pouco'], 1, 'Lucas 9:25 - nada aproveita se perder a si mesmo'),
    ]),
    ('Lucas 19: Zaqueu', 'Zaqueu era chefe dos publicanos e era rico. Subiu numa árvore para ver Jesus. Jesus disse: Zaqueu, desce, porque hoje preciso ficar em tua casa.', 'Lucas 19:1-10', 'Jesus vem até nós onde estamos', 'Não importa quem você é, Jesus quer estar com você.', [
        mc('Por que Zaqueu subiu na arvore?', ['Para fugir','Para ver Jesus porque era baixo','Para roubar','Para dormir'], 1, 'Era baixo e queria ver Jesus'),
        vf('Jesus ignorou Zaqueu.', 'Ignorou Zaqueu.', 0, 'Jesus disse: preciso ficar em tua casa'),
        mc('O que aconteceu com Zaqueu?', ['Morreu','Foi salvo e mudou de vida','Fugiu','Perdeu tudo'], 1, 'Foi salvo e Zaqueu deu metade dos seus bens'),
    ]),
    ('Mateus 28: A Ressurreição', 'Jesus ressuscitou! Os anjos disseram: Ele não está aqui, pois ressuscitou. Jesus apareceu aos discípulos e disse: Toda autoridade me é dada. Vão e façam discípulos.', 'Mateus 28:1-20', 'A Ressurreição e a base da fé cristã', 'Jesus venceu a morte e tem toda autoridade.', [
        mc('Jesus ressuscitou no:', ['Primeiro dia','Terceiro dia','Setimo dia','Dia seguinte'], 1, 'No terceiro dia'),
        mc('O que Jesus tem?', ['Apenas um pouco de poder','Toda autoridade no ceu e na terra','Nada','Apenas sabedoria'], 1, 'Toda autoridade no ceu e na terra'),
        vf('Jesus nunca mais voltou a aparecer.', 'Nunca mais apareceu.', 0, 'Apareceu por 40 dias antes de ascender'),
    ]),
    ('Apocalipse 1: Jesus Glorificado', 'João viu Jesus glorificado: olhos como chamas de fogo, voz como muitas águas. Jesus disse: Eu sou o Alfa e o Ômega, o que era, que é e que há de vir.', 'Apocalipse 1:9-20', 'Jesus é glorioso e poderoso', 'Jesus é o mesmo de ontem, hoje e sempre.', [
        mc('Como sao os olhos de Jesus na visao?', ['Azuis','Como chamas de fogo','Verdes','Pretos'], 1, 'Olhos como chamas de fogo'),
        mc('Jesus se chama:', ['O primeiro','O ultimo','Alfa e Omega','Todas as anteriores'], 3, 'Alfa e Omega, o primeiro e o ultimo'),
        vf('Jesus e fraco na visao de Joao.', 'E fraco.', 0, 'Poderoso, glorioso, com as chaves da morte e do hades'),
    ]),
], 50)
print("  Trilha 23 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 24 - Adolescentes: Vida Crista
# ═══════════════════════════════════════════════
t24 = mk_trilha('Adolescentes: Vida Crista', 'Ensinamentos praticos para viver a fé no dia a dia: identidade em Cristo, amor, perseveranca e luta espiritual', 'adolescente', 'intermediario', 24, 'school')
add_licoes(t24, [
    ('Efésios 1: Identidade em Cristo', 'Deus nos abençoou com todas as bênçãos espirituais. Nos escolheu antes da fundação do mundo, predestinou para filhos adotivos. Somos aceitos no Amado.', 'Efesios 1:3-14', 'Conhecer sua identidade como filho amado de Deus', 'Você não é acidente. Deus te escolheu antes de tudo.', [
        mc('Onde somos abencoados?', ['Na terra','Nos lugares celestiais em Cristo','Na escola','No trabalho'], 1, 'Efesios 1:3 - nos lugares celestiais em Cristo'),
        vf('Deus nos escolheu depois que nascemos.', 'Escolheu depois.', 0, 'Antes da fundacao do mundo'),
        mc('Somos chamados de:', ['Escravos','Estranhos','Filhos adotivos de Deus','Nada'], 2, 'Filhos adotivos em amor'),
    ]),
    ('Efésios 6: A Armadura de Deus', 'Vesti a armadura de Deus: cinto da verdade, couraça da justiça, escudo da fé, capacete da salvação, espada do Espírito e oração.', 'Efesios 6:10-20', 'Vestir-se espiritualmente todos os dias', 'A guerra espiritual é real, mas Deus fornece toda armadura.', [
        mc('Qual e a espada do Espirito?', ['Uma espada fisica','A Palavra de Deus','O dinheiro','A raiva'], 1, 'A Palavra de Deus'),
        vf('A armadura de Deus e apenas simbolica.', 'E apenas simbolica.', 0, 'E real e necessaria para a guerra espiritual'),
        mc('O que devemos fazer em toda oracao?', ['Cantar','Dormir','Orar sempre no Espirito','Correr'], 2, 'Orar em todo tempo no Espirito'),
    ]),
    ('Filipenses 4: Alegria', 'Alegrai-vos sempre no Senhor. Novamente digo: alegrai-vos. Não vos atristeis por nada. O Deus da paz estará convosco.', 'Filipenses 4:4-13', 'Cultivar alegria que não depende de circunstâncias', 'A alegria cristã é profunda, mesmo nas dificuldades.', [
        mc('Quando devemos nos alegrar?', ['Apenas quando temos dinheiro','Sempre no Senhor','Apenas nos domingos','Nunca'], 1, 'Sempre no Senhor'),
        vf('Paulo disse para ficar triste.', 'Ficar triste.', 0, 'Alegrai-vos sempre, o Senhor esta perto'),
        mc('O que podemos fazer com tudo em oracao?', ['Ignorar','Pedir e agradecer com suplicas','Gritar','Dormir'], 1, 'Com suplicas e agradecimentos, apresentai os vossos pedidos'),
    ]),
    ('Colossenses 2: Completos em Cristo', 'Em Cristo habita toda a plenitude da divindade. Vós estáis completos nele. Não deixem que ninguém os engane com filosofias vazias.', 'Colossenses 2:9-15', 'Viver na certeza de que Cristo nos completa', 'Não precisamos de nada além de Cristo para estar completos.', [
        mc('Onde habita toda a plenitude?', ['No templo','Em Cristo','No dinheiro','Na escola'], 1, 'Em Cristo habita toda a plenitude'),
        vf('Precisamos de coisas extras para ser completos.', 'Precisamos extras.', 0, 'Estamos completos em Cristo'),
        mc('O que nao devemos deixar?', ['Ninguem nos engane com filosofias vazias','Ninguem nos ajude','Ninguem nos veja','Ninguem nos fale'], 0, 'Que ninguem nos engane com filosofias vazias'),
    ]),
    ('Tiago 1: Tribulações', 'Considerai puro gozo quando entrardes em provações de muitas sortes, porque a fé provada produz perseverança. Se falta sabedoria, peça a Deus.', 'Tiago 1:2-12', 'Encontrar alegria nas dificuldades', 'As provações fortalecem a fé e produzem maturidade.', [
        mc('O que devemos fazer nas provacoes?', ['Chorar sempre','Ter puro gozo','Desistir','Odiar'], 1, 'Considerai puro gozo'),
        vf('Deus nao da sabedoria a quem pede.', 'Nao da sabedoria.', 0, 'De a todos simplesmente e sem repreensao'),
        mc('A fe provada produz:', ['Medo','Perseveranca','Pecado','Desespero'], 1, 'Perseveranca e madureza'),
    ]),
    ('Tiago 2: Fé e Obras', 'Se alguém diz que tem fé e não tem obras, que lhe aproveita? A fé sem obras é morta. Mostra-me a tua fé pelas tuas obras.', 'Tiago 2:14-26', 'Viver uma fé que se demonstra em ações', 'Fé genuína se manifesta em obras.', [
        mc('Fe sem obras e:', ['Morta','Boa','Maior','Mais valiosa'], 0, 'A fe, se nao tiver obras, e morta'),
        vf('A fe que nao produz obras e morta.', 'A fe que nao produz obras e morta.', 1, 'Tiago 2:17 - a fe sem obras e morta'),
        mc('Como mostramos nossa fe?', ['Só com palavras','Pelas obras que fazemos','Guardando dinheiro','Dormindo'], 1, 'Pelas obras'),
    ]),
    ('1 Coríntios 13: O Amor', 'Sem amor, nada temos. O amor é paciente, bondoso, não busca seus interesses, não se irrita. A fé, a esperança e o amor permanecem, mas o maior é o amor.', '1 Corintios 13:1-13', 'Amar como Deus ama', 'O amor é o mais excelente caminho.', [
        mc('Qual e a primeira coisa do amor?', ['Paciencia','Bondade','Raiva','Medo'], 0, '1 Corintios 13:4 - o amor e paciente, e bondoso'),
        vf('O amor busca seus proprios interesses.', 'Busca seus interesses.', 0, 'Nao busca seus interesses'),
        mc('Qual dos tres permanece?', ['Fe','Esperanca','Amor','Todas'], 3, '1 Corintios 13:13 - permanecem a fe, a esperanca e o amor; mas o maior e o amor'),
    ]),
    ('1 Pedro 2: Pedras Vivas', 'Vós sois pedras vivas, edificados espiritualmente. Cristo é a pedra angular. Somos uma casa sacerdotal espiritual para oferecer sacrifícios espirituais.', '1 Pedro 2:1-10', 'Ser parte viva da igreja de Cristo', 'Cada crente é uma pedra viva na casa de Deus.', [
        mc('Que somos como pedras?', ['Mortas','Vivas','Pesadas','Frias'], 1, 'Pedras vivas'),
        mc('Quem e a pedra angular?', ['Paulo','Pedro','Cristo','Davi'], 2, 'Cristo e a pedra angular'),
        vf('Somos uma casa material.', 'Somos materiais.', 0, 'Somos uma casa espiritual'),
    ]),
    ('Romanos 8: Sem Condenação', 'Não há condenação para os que estão em Cristo Jesus. Nada pode nos separar do amor de Deus. O Espírito nos ajuda em nossas fraquezas.', 'Romanos 8:1-39', 'Viver livres da culpa e da condenação', 'Em Cristo, não há condenação!', [
        mc('Ha condenacao para quem esta em Cristo?', ['Sim','Nunca','As vezes','Depende'], 1, 'Nao ha nenhuma condenacao'),
        mc('O que pode nos separar do amor de Deus?', ['Pecado','Morte','Nada','O diabo'], 2, 'Nada pode nos separar do amor de Deus'),
        vf('Deus nos condena quando pecamos.', 'Condena.', 0, 'Nao ha condenacao para quem esta em Cristo'),
    ]),
    ('2 Timóteo 4: Perseverança', 'Combate o bom combate da fé. Persiga a justiça. Fui derramado como oferta de libação. Despacho já está feito. Guarda a coroa da justiça.', '2 Timoteo 4:1-8', 'Ser fiel até o fim', 'Paulo encoraja a perseverança até a volta de Cristo.', [
        mc('O que Paulo pede a Timoteo?', ['Desista','Combate o bom combate da fe','Fuja','Durma'], 1, 'Combate o bom combate da fe, persevera na justica'),
        vf('Paulo desanimou no final da vida.', 'Desanimou.', 0, 'Sabe que esta guardada a coroa da justica'),
        mc('O que esta guardado para Paulo?', ['Dinheiro','A coroa da justica','Uma casa','Nada'], 1, 'A coroa da justica'),
    ]),
], 50)
print("  Trilha 24 completa - 10 licoes")

# ═══════════════════════════════════════════════
# TRILHA 25 - Teologia Sistematica
# ═══════════════════════════════════════════════
t25 = mk_trilha('Teologia Sistematica', 'Os grandes temas da teologia cristã: Criacao, Pecado, Justificacao, Eleição, Cristologia, Ressurreição e Escatologia', 'adulto', 'avancado', 25, 'school')
add_licoes(t25, [
    ('Gênesis 1-2: Criação', 'Deus criou tudo por Sua palavra. O homem foi feito à Sua imagem e semelhança, com dignidade e responsabilidade sobre a criação.', 'Genesis 1:1-2:25', 'Compreender os fundamentos da doutrina da criação', 'Deus é o Criador soberano. O homem tem dignidade por ser a imagem de Deus.', [
        mc('Como Deus criou?', ['Apenas pensou','Por Sua palavra','Por acaso','Depois de muito tempo'], 1, 'E disse: haja luz! E houve luz'),
        vf('O homem e apenas um animal.', 'E apenas um animal.', 0, 'Feito a imagem e semelhanca de Deus'),
        mc('Qual e a responsabilidade do homem?', ['Nenhuma','Cuidar da criacao','Dominar os outros','Destruir'], 1, 'Cuidar e governar a criacao'),
    ]),
    ('Gênesis 3: A Queda', 'Adão e Eva desobedeceram a Deus e o pecado entrou no mundo. A consequência foi a morte espiritual, a expulsão do Éden e a maldição sobre a terra.', 'Genesis 3:1-24', 'Entender a doutrina do pecado original', 'A Queda corrompeu toda a humanidade. Todos precisamos de redenção.', [
        mc('Qual foi a primeira desobediencia?', ['Caim matou Abel','Comer da fruta proibida','Mentir','Cobardia'], 1, 'Comer da arvore proibida'),
        vf('A Queda afetou apenas Adao e Eva.', 'Afetou apenas eles.', 0, 'Afetou toda a humanidade'),
        mc('Qual foi a consequencia?', ['Apenas expulsao','Morte espiritual e expulsao do Eden','Nada','Mais poder'], 1, 'Morte espiritual e expulsao do Eden'),
    ]),
    ('Romanos 3-4: Justificação', 'Todos pecaram e faltam da glória de Deus. Mas somos justificados gratuitamente pela graça, mediante a redenção em Cristo Jesus. A fé de Abraão e o modelo.', 'Romanos 3:21-4:25', 'Compreender a doutrina da justificação pela fé', 'A justificação é um ato gratuito de Deus que nos declara justos pela fé.', [
        mc('Quantos pecaram?', ['Apenas os gentios','Apenas os judeus','Todos','Nenhum'], 2, 'Todos pecaram e faltam da gloria de Deus'),
        vf('A justificacao depende de nossas obras.', 'Depende de obras.', 0, 'E pela graça, mediante a fé, nao por obras'),
        mc('Quem e o modelo de justificacao pela fe?', ['Moises','Davi','Abraao','Paulo'], 2, 'Abraao creu em Deus e lhe foi imputada justica'),
    ]),
    ('Romanos 5: Paz com Deus', 'Sendo justificados pela fé, temos paz com Deus. A graça de Deus abunda onde o pecado aumentou. O amor de Deus foi derramado em nossos corações.', 'Romanos 5:1-11', 'Experimentar a paz e o acesso à graça', 'A justificação traz paz com Deus e acesso à Sua graça.', [
        mc('O que temos pela justificacao?', ['Medo','Paz com Deus','Perfeicao','Sabedoria'], 1, 'Paz com Deus atraves de Jesus'),
        vf('A graça de Deus diminui onde o pecado aumenta.', 'Diminui.', 0, 'A graça abunda ainda mais'),
        mc('Onde o amor de Deus foi derramado?', ['No chão','Nos coracoes dos crentes','No templo','No ceu'], 1, 'Foi derramado em nossos coracoes'),
    ]),
    ('Romanos 6: Libertação do Pecado', 'Devemos viver como mortos para o pecado. Fomos batizados com Cristo na morte e ressurreição. O pecado não terá domínio sobre nós, pois estamos debaixo da graça.', 'Romanos 6:1-23', 'Entender que a graça liberta, não autoriza pecar', 'Somos novas criaturas livres do domínio do pecado.', [
        mc('Devemos continuar pecando para que a graça aumente?', ['Sim','Nao, de forma alguma','As vezes','Depende'], 1, 'De forma alguma!'),
        vf('A graça nos dá licenca para pecar.', 'Licença para pecar.', 0, 'A graça liberta do pecado, nao autoriza a viver nele'),
        mc('O que governa o crente?', ['O pecado','A graça e a justica','O mundo','A carne'], 1, 'Debaixo da graça, nao debaixo da Lei'),
    ]),
    ('Romanos 8: Glorificação', 'Não há condenação para quem está em Cristo. O Espírito nos vivifica. Nada pode nos separar do amor de Deus. Todos os que foram predestinados serão chamados e justificados.', 'Romanos 8:1-39', 'Compreender a glorificação como etapa final da salvação', 'Deus completa Sua obra em nós. A glória eterna é certa.', [
        mc('Ha condenacao?', ['Sim','Nunca','As vezes','Depende'], 1, 'Nao ha nenhuma condenacao'),
        mc('O que pode nos separar do amor de Deus?', ['Nada','Pecado','O diabo','A morte'], 0, 'Nada pode nos separar do amor de Deus'),
        vf('Todos que Deus predestinou serao justificados.', 'Todos que Deus predestinou serao justificados.', 1, 'Romanos 8:30 - os predestinados sao chamados, justificados e glorificados'),
    ]),
    ('Efésios 1: Eleição', 'Deus nos escolheu em Cristo antes da fundação do mundo, predestinando-nos para adoção. Tudo segundo o propósito da Sua vontade.', 'Efesios 1:3-14', 'Entender a doutrina da eleição divina', 'Deus é soberano na Sua escolha, por amor e para Sua glória.', [
        mc('Quando Deus nos escolheu?', ['Quando nascemos','Depois de pecar','Antes da fundacao do mundo','Quando aceitamos'], 2, 'Antes da fundacao do mundo'),
        vf('A eleição depende das nossas boas obras.', 'Depende de obras.', 0, 'E pela graça, segundo o proposito de Sua vontade'),
        mc('Para que fomos predestinados?', ['Para condenacao','Para adocao como filhos','Para sofrer','Para nada'], 1, 'Para adocao como filhos em Cristo'),
    ]),
    ('Hebreus 1-2: Cristologia', 'Cristo é a imagem do Deus invisível, superior a todos os anjos. Por Ele foram criadas todas as coisas. Tornou-se um pouco menor que os anjos para sofrer a morte.', 'Hebreus 1:1-2:18', 'Compreender a natureza divina e humana de Cristo', 'Cristo é plenamente Deus e plenamente homem. A encarnação é o mistério central da fé.', [
        mc('Cristo e:', ['Inferior aos anjos','Superior a todos os anjos','Igual aos anjos','Igual aos homens'], 1, 'Superior a todo anjo'),
        vf('Cristo nao sofreu verdadeiramente.', 'Nao sofreu.', 0, 'Sofreu verdadeiramente para ser nosso sumo sacerdote'),
        mc('Cristo e sumo sacerdote:', ['Temporario','Segundo a Lei de Aaron','Misericordioso e fiel','Nao e sacerdote'], 2, 'Misericordioso e fiel, para sempre'),
    ]),
    ('1 Coríntios 15: Ressurreição', 'Se Cristo não ressuscitou, a fé é vã. Mas Cristo ressuscitou e é a primícia dos que dormem. Seremos transformados em corpos gloriosos.', '1 Corintios 15:1-58', 'Firmar a fé na ressurreição corporal', 'A ressurreição de Cristo é o fundamento da fé cristã.', [
        mc('Se Cristo nao ressuscitou:', ['A fé e valida','A fé e va','O mundo mudou','Nao importa'], 1, 'A fé seria vã'),
        mc('Cristo e a primicia dos:', ['Vivos','Anjos','Que dormem','Mortos'], 2, 'Primicia dos que dormem (mortos)'),
        vf('Nao haverá ressurreição dos mortos.', 'Nao ha ressurreição.', 0, 'Haverá: seremos transformados em corpos gloriosos'),
    ]),
    ('Apocalipse 21: Escatologia', 'Vi os novos céus e a nova terra. A Nova Jerusalém desce do céu. Não haverá mais lágrimas, nem morte, nem dor. O Senhor será o seu Deus, e eles serão o Seu povo.', 'Apocalipse 21:1-22:21', 'Esperar a consumação de todas as coisas', 'A esperança final é a nova criação, onde Deus habita com o Seu povo.', [
        mc('O que nao haverá na nova criacao?', ['Louvor','Alegría','Larmas, morte e dor','Amor'], 2, 'Nao haverá mais larmas, nem morte, nem dor'),
        vf('O ceu e apenas um lugar mental.', 'E apenas mental.', 0, 'E a Nova Jerusalem real, que desce do ceu'),
        mc('Quem esta no centro?', ['O homem','Deus e o Cordeiro','Os anjos','O diabo'], 1, 'Deus e o Cordeiro'),
    ]),
], 50)
print("  Trilha 25 completa - 10 licoes")

print("\nSeed v2 completo! Trilhas 1-25 criadas com sucesso.")

# ═══════════════════════════════════════════════
# SERIES OURO - Desafios avancados por trilha
# ═══════════════════════════════════════════════
from gamification.models import SerieOuroDesafio, SerieOuroExercicio

def mk_serie_ouro(trilha, titulo, desc, faixa, nivel, xp, exercicios):
    serie, _ = SerieOuroDesafio.objects.get_or_create(
        titulo=titulo, defaults=dict(
            descricao=desc, trilha=trilha, faixa_etaria=faixa,
            nivel=nivel, xp_recompensa=xp, ativo=True, ordem=1
        ))
    for i, e in enumerate(exercicios, 1):
        SerieOuroExercicio.objects.get_or_create(
            desafio_ouro=serie, enunciado=e[1][:200],
            defaults=dict(tipo=e[0], dados=e[2], peso_dificuldade=3))
    return serie

# Serie Ouro - Trilha 1 (Criacao e Patriarcas)
mk_serie_ouro(t1, 'Ouro: Patriarcas - Dominio Total', 'Prove que conhece toda a historia dos patriarcas', 'adulto', 'avancado', 350, [
    mc('Quantos filhos teve Jacó?', ['10','11','12','13'], 2, 'Doze tribos'),
    vf('Jose foi vendido por 30 pecas de prata.', 'Jose foi vendido por 30 pecas de prata.', 0, 'Foi por 20 pecas de prata'),
    mc('Quem era a mae de Isaque?', ['Sara','Rebeca','Raquel','Leia'], 0, 'Genesis 21:2'),
    vf('Abraao deixou Ur por causa de Deus.', 'Abraao deixou Ur por causa de Deus.', 1, 'Genesis 12:1'),
])

# Serie Ouro - Trilha 3 (Davi)
mk_serie_ouro(t3, 'Ouro: Davi - Conhecimento Profundo', 'Dominio total sobre a vida de Davi', 'adulto', 'avancado', 400, [
    mc('Quantos filhos de Davi sao nomeados na Biblia?', ['6','19','22','40'], 1, '1 Cronicas 3 - seis em Hebron e treze em Jerusalem'),
    vf('Salmo 23 foi escrito por Salomao.', 'Salmo 23 foi escrito por Salomao.', 0, 'Foi escrito por Davi'),
    mc('Qual cidade Davi conquistou para ser capital?', ['Betlehem','Jerusalem','Hebron','Ninive'], 1, '2 Samuel 5'),
    vf('Davi nunca cometeu pecado.', 'Davi nunca cometeu pecado.', 0, 'Cometeu adultério e assassinato'),
])

# Serie Ouro - Trilha 6 (Jesus)
mk_serie_ouro(t6, 'Ouro: Jesus - Detalhes da Vida', 'Mostre que conhece cada detalhe da vida de Jesus', 'adulto', 'avancado', 450, [
    mc('Primeiro milagre de Jesus:', ['Cegos','Agua em vinho','Morto ressuscitado','Tempestade calada'], 1, 'Jo 2:1-11'),
    vf('Jesus nasceu em Jerusalem.', 'Jesus nasceu em Jerusalem.', 0, 'Nasceu em Betlehem'),
    mc('Quantos apóstolos Jesus escolheu?', ['10','11','12','13'], 2, 'Mateus 10:1-4'),
    vf('Jesus foi batizado por Pedro.', 'Jesus foi batizado por Pedro.', 0, 'Foi batizado por Joao Batista'),
])

# Serie Ouro - Trilha 8 (Romanos)
mk_serie_ouro(t8, 'Ouro: Romanos - Teologia Reformada', 'Dominio da teologia paulina', 'adulto', 'avancado', 450, [
    mc('Justificacao significa:', ['Tornado santo','Declarado justo pela fe','Sentir remorso','Fazer obras'], 1, 'Rm 3:28'),
    vf('Salvacao depende de obras.', 'Salvacao depende de obras.', 0, 'E pela fe - Ef 2:8'),
    mc('Rm 8:28 diz:', ['Deus nao se importa','Todas coisas cooperam para o bem','Nada acontece','Deus e mau'], 1, 'Rm 8:28'),
    vf('Paulo foi discipulo direto de Jesus.', 'Paulo foi discipulo direto de Jesus.', 0, 'Paulo converteu-se depois da ascensao'),
])

# Serie Ouro - Trilha 12 (Hebreus)
mk_serie_ouro(t12, 'Ouro: Hebreus - Cristo Superior', 'Dominio da teologia da carta aos Hebreus', 'adulto', 'avancado', 450, [
    mc('Cristo e superior porque:', ['E mais bonito','E Filho de Deus eterno','E mais forte','Nao e'], 1, 'Hebreus 1:3'),
    vf('Hebreus ensina que podemos perder a salvacao.', 'Hebreus ensina que podemos perder a salvacao.', 0, 'Ensina a perseveranca ate o fim'),
    mc('Hb 11 descreve:', ['Heróis da fé','Reis de Israel','Profetas maus','Nada'], 0, 'Capitulo da fe'),
])

# Serie Ouro - Trilha 15 (Apocalipse)
mk_serie_ouro(t15, 'Ouro: Apocalipse - Profecias', 'Dominio das profecias finais', 'adulto', 'avancado', 500, [
    mc('Alfa e Omega:', ['Satanas','Cristo','Joao','Ninguem'], 1, 'Ap 1:8'),
    vf('Apocalipse e so destruicao.', 'Apocalipse e so destruicao.', 0, 'E tambem esperanca e renovacao'),
    mc('Vencemos pelo:', ['Exercito','Sangue do Cordeiro','Dinheiro','Inteligencia'], 1, 'Ap 12:11'),
])

print("  Series Ouro criadas")

# ═══════════════════════════════════════════════
# DESAFIOS DIARIOS - Uma semana completa
# ═══════════════════════════════════════════════
base = date.today()
semana = [
    ('Versiculo do Dia', 'Leia Jo 3:16 e medite', 'Jo 3:16', 'Qual a mensagem central deste versiculo?'),
    ('Oração e Gratidão', 'Agradeça a Deus por 5 coisas', '1 Ts 5:18', 'Como a gratidao transforma sua perspectiva?'),
    ('Perdão', 'Perdoe alguem que te ofendeu', 'Cl 3:13', 'O que impede voce de perdoar?'),
    ('Amor', 'Fac uma boa acao sem ser pedido', '1 Jo 4:19', 'Como demonstrar amor ao proximo?'),
    ('Fe', 'Leia Hb 11:1 e ore', 'Hb 11:1', 'O que significa ter fe?'),
    ('Descanso', 'Leia Salmo 23 e descanse', 'Sl 23', 'O que significa ser pastor da sua vida?'),
    ('Palavra', 'Memorize Jo 3:16', 'Sl 119:11', 'Como a Palavra guarda nosso coracao?'),
]
for i, (tit, desc, ver, perg) in enumerate(semana):
    DesafioDiario.objects.get_or_create(
        data=base + timedelta(days=i),
        defaults=dict(titulo=tit, descricao=desc, versiculo=ver, pergunta=perg, xp_recompensa=30, ativo=True))
print("  Desafios diarios criados")

# ═══════════════════════════════════════════════
# RECOMPENSAS
# ═══════════════════════════════════════════════
from gamification.models import Recompensa

def mk_recomp(tipo, titulo, desc, icone, xp, **kw):
    Recompensa.objects.get_or_create(titulo=titulo, defaults=dict(descricao=desc, tipo=tipo, icone=icone, xp_recompensa=xp, **kw))

mk_recomp('medalha', 'Heroi da Fe', 'Complete a trilha Criacao e Patriarcas', 'Globe', 300)
mk_recomp('medalha', 'Estudioso', 'Complete a trilha Romanos', 'Book', 500)
mk_recomp('medalha', 'Discipulo', 'Complete Jesus: Vida e Ministerio', 'Cross', 400)
mk_recomp('medalha', 'Louvador', 'Complete a trilha Salmos', 'Music', 300)
mk_recomp('medalha', 'Mensageiro', 'Complete a trilha Atos', 'Fire', 300)
mk_recomp('medalha', 'Teologo', 'Complete Hebreus', 'ArrowUp', 400)
mk_recomp('medalha', 'Profeta', 'Complete Profetas', 'Warning', 300)
mk_recomp('medalha', 'Colecionador', '30 dias de streak', 'Star', 1000)
mk_recomp('versiculo', 'Joao 3:16', 'O amor de Deus em versiculo', 'Scroll', 50)
mk_recomp('xp_bonus', 'Bonus 10 Licoes', 'Complete 10 licoes', 'Target', 400)
mk_recomp('xp_bonus', 'Bonus 25 Licoes', 'Complete 25 licoes', 'Zap', 800)
mk_recomp('xp_bonus', 'Bonus 50 Licoes', 'Complete 50 licoes', 'Zap', 1500)
mk_recomp('xp_bonus', 'Bonus 100 Licoes', 'Complete 100 licoes', 'Zap', 3000)
print("  Recompensas criadas")

print("\n=== SEED V2 COMPLETO ===")
print(f"  Trilhas: {Trilha.objects.count()}")
print(f"  Licoes: {LicaoBiblica.objects.count()}")
print(f"  Exercicios: {Exercicio.objects.count()}")
print(f"  Series Ouro: {SerieOuroDesafio.objects.count()}")
print(f"  Desafios Diarios: {DesafioDiario.objects.count()}")
print(f"  Recompensas: {Recompensa.objects.count()}")
