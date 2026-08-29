import logging
from decouple import config

logger = logging.getLogger(__name__)

LLM_API_KEY = config('LLM_API_KEY', default='')
LLM_MODEL = config('LLM_MODEL', default='gemini-2.5-flash')

# ═══════════════════════════════════════════════════════════
# BASE DE RESPOSTAS POR TOPICO (Reforma)
# ═══════════════════════════════════════════════════════════
RESPOSTAS_POR_TOPICO = {
    'fe': {
        'respostas': [
            'A fé é o fundamento da vida cristã. O autor de Hebreus a define: "A fé é a certeza do que esperamos e a prova do que não vemos" (Hb 11:1). Não se trata de um sentimento vago, mas de uma confiança concreta nas promessas de Deus.\n\nCalvino ensinava que a fé é "um conhecimento firme e certo da benevolência de Deus em relação a nós, porque Ele nos confirmou pelo Seu evangelho." A fé não é obra nossa, mas dom de Deus (Ef 2:8).\n\nComo você pode exercitar sua fé hoje? Leia Hebreus 11 e veja como os heróis da fé viveram.\n\n📖 *Referências*: Hb 11:1, Ef 2:8, Rm 10:17',
            'A fé cristã não é cega, mas fundamentada na Palavra de Deus. "A fé vem pelo ouvir, e o ouvir pela palavra de Deus" (Rm 10:17). Cada vez que lemos a Bíblia, estamos fortalecendo nossa fé.\n\nLutero dizia: "A fé é um trabalho ativo e poderoso que não tolera não fazer nada." A fé verdadeira sempre se manifesta em ação, em obediência ao que Deus ordena.\n\nSe sua fé está fraca, não desanime. Ore pedindo fé, e Deus aumentará sua confiança Nele.\n\n📖 *Referências*: Rm 10:17, Tg 2:17, Mc 9:24',
        ],
        'passagens': ['Hb 11:1', 'Rm 10:17', 'Ef 2:8', 'Tg 2:17', 'Mc 9:24'],
    },
    'graça': {
        'respostas': [
            'A graça de Deus é o fundamento da salvação. "Porque pela graça sois salvos, por meio da fé; e isso não vem de vós, é dom de Deus" (Ef 2:8). A graça é o favor imerecido de Deus para com os pecadores.\n\nAgostinho ensinava que a graça precede toda obra boa em nós. Não é porque somos bons que Deus nos ama, mas porque Deus nos ama é que nos torna bons. A graça é o motor da santificação.\n\nHoje, agradeça a Deus pela Sua graça que não depende dos seus méritos, mas do Seu amor infinito.\n\n📖 *Referências*: Ef 2:8-9, Tt 3:5, Rm 3:24',
            'Somos salvos pela graça, não por obras. Paulo é claro: "Não pelas obras de justiça que tivéssemos feito, mas segundo a Sua misericórdia" (Tt 3:5). A graça é o que distingue o cristianismo de todas as religiões do mundo.\n\nSpurgeon dizia: "A graça é o início, o meio e o fim da nossa salvação." Não começou com nós, não depende de nós, e não terminará connosco. É Deus quem faz tudo.\n\nReconheça hoje que você não precisa merecer o amor de Deus — Ele já o ama perfeitamente em Cristo.\n\n📖 *Referências*: Tt 3:5, Rm 3:24, Ef 2:8-9',
        ],
        'passagens': ['Ef 2:8-9', 'Tt 3:5', 'Rm 3:24', 'Rm 5:8', 'Rm 6:14'],
    },
    'pecado': {
        'respostas': [
            'Todos pecaram e estão destituídos da glória de Deus (Rm 3:23). O pecado é a realidade mais triste da condição humana. Ninguém está isento — nem o melhor de nós.\n\nCalvino ensinava que o pecado corrompe todas as faculdades humanas: a mente, a vontade e as emoções. Não somos apenas pecadores por ação, mas por natureza.\n\nMas a boa notícia é: "Onde o pecado aumentou, a graça superabundou" (Rm 5:20). Cristo veio para salvar pecadores, dos quais eu sou o principal (1 Tm 1:15).\n\n📖 *Referências*: Rm 3:23, Rm 5:20, 1 Tm 1:15',
            'O pecado é mais grave do que imaginamos. Ele não é apenas "erros" ou "falhas", mas rebelião consciente contra o Criador. Por isso, o julgamento é inevitável sem Cristo.\n\nMas em Cristo, o pecado foi julgado na cruz. "Deus o que não conheceu pecado, fez pecado por nós" (2 Co 5:21). Jesus tomou sobre Si o castigo que merecíamos.\n\nNão minimizes teu pecado, mas não desanimes da graça de Deus. Ele é mais forte que o teu pecado.\n\n📖 *Referências*: Rm 3:23, 2 Co 5:21, 1 Jo 1:9',
        ],
        'passagens': ['Rm 3:23', 'Rm 5:20', '2 Co 5:21', '1 Jo 1:9', 'Rm 6:23'],
    },
    'amor': {
        'respostas': [
            'Deus é amor (1 Jo 4:8). Esta é a declaração mais profunda da Bíblia sobre o caráter divino. O amor de Deus não é um sentimento passageiro, mas a essência de Sua natureza.\n\nO maior mandamento resume tudo: "Amarás o Senhor teu Deus de todo o teu coração, de toda a tua alma e de todo o teu entendimento" (Mt 22:37). O segundo é semelhante: amarás o teu próximo como a ti mesmo.\n\nO amor cristão é sacrificial. "Nisto conhecemos o amor: que Ele deu a Sua vida por nós" (1 Jo 3:16). Amar como Cristo amou é o chamado de todo crente.\n\n📖 *Referências*: 1 Jo 4:8, Mt 22:37-39, 1 Jo 3:16',
            'O amor de Deus é o maior mistério da fé. Paulo escreveu um hino ao amor em 1 Coríntios 13: "Ainda que eu falasse as línguas dos homens e dos anjos, e não tivesse amor, seria como o metal que soa ou como o sino que tine."\n\nTozer dizia: "Deus não ama porque somos valiosos; somos valiosos porque Ele nos ama." O amor divino é a origem e o fundamento de tudo o que somos.\n\nEscolha hoje amar alguém que é difícil de amar — isso reflete o amor de Cristo por nós.\n\n📖 *Referências*: 1 Co 13, 1 Jo 4:19, Rm 5:8',
        ],
        'passagens': ['1 Jo 4:8', '1 Co 13', 'Mt 22:37-39', 'Rm 5:8', '1 Jo 3:16'],
    },
    'oracao': {
        'respostas': [
            'A oração é a respiração da alma cristã. "Em tudo pela oração e súplica, com ações de graças, apresentai os vossos pedidos a Deus" (Fp 4:6). Não há situação que não possa ser levada a Deus em oração.\n\nCalvino dizia que a oração é "a conversa íntima e espontânea que temos com Deus sobre tudo o que nos aflige." Não precisa ser elaborada — Deus quer autenticidade.\n\nJesus nos ensinou a orar com o "Pai Nosso" (Mt 6:9-13), que contém tudo o que precisamos: adoração, pedido, perdão e proteção.\n\n📖 *Referências*: Fp 4:6-7, Mt 6:9-13, 1 Ts 5:17',
            'Ore sem cessar (1 Ts 5:17). Isso não significa repetir palavras o dia todo, mas manter uma atitude constante de dependência de Deus. Cada pensamento pode ser levado a Ele.\n\nSpurgeon dizia: "Oração é a chave do dia e a tranca da noite." Comece o dia em oração, e você verá a diferença em tudo.\n\nQue tal reservar 10 minutos hoje para orar com atenção? Deus ouve e responde de acordo com Sua vontade.\n\n📖 *Referências*: 1 Ts 5:17, Fp 4:6, Mt 7:7',
        ],
        'passagens': ['Fp 4:6-7', 'Mt 6:9-13', '1 Ts 5:17', 'Mt 7:7', 'Tg 5:16'],
    },
    'esperanca': {
        'respostas': [
            'Temos uma esperança viva em Cristo. "Bendito seja o Deus e Pai de nosso Senhor Jesus Cristo, que segundo a Sua grande misericórdia nos regenerou para uma viva esperança" (1 Pe 1:3). Nossa esperança não é wishful thinking, mas certeza baseada na ressurreição.\n\nLutero dizia: "Mesmo que eu soubesse que amanhã o mundo acabaria, eu ainda plantaria minha macieira." A esperança cristã nos faz viver com propósito, mesmo diante da incerteza.\n\nO que mais te dá esperança hoje? Lembre-se: Cristo ressuscitou, e por isso o amanhã pertence a Deus.\n\n📖 *Referências*: 1 Pe 1:3, Rm 8:28, Rm 15:13',
            'Nossa esperança não está nas circunstâncias, mas na pessoa de Cristo. "Se Cristo não ressuscitou, vã é a vossa fé" (1 Co 15:17). Mas Ele ressuscitou! E por isso temos esperança viva.\n\nBonhoeffer escreveu: "A esperança é quando Deus nos dá o que não pedimos." Ela vai além das nossas expectativas humanas.\n\nNão olhe apenas para o que você vê — olhe para Cristo, que é a esperança da glória (Cl 1:27).\n\n📖 *Referências*: 1 Co 15:17, Cl 1:27, Rm 8:28',
        ],
        'passagens': ['1 Pe 1:3', 'Rm 8:28', '1 Co 15:17', 'Cl 1:27', 'Rm 15:13'],
    },
    'cristo': {
        'respostas': [
            'Jesus Cristo é o centro de tudo na Bíblia e na história. "Nele habita corporalmente toda a plenitude da Deidade" (Cl 2:9). Não é apenas um bom professor ou profeta — é Deus encarnado.\n\nA Cristologia reformada enfatiza que Cristo é verdadeiro Deus e verdadeiro homem, perfeito em Sua natureza dupla. Ele é o Mediador único entre Deus e os homens (1 Tm 2:5).\n\nSe você não conhece Cristo, hoje é o dia da salvação. Ele é o Caminho, a Verdade e a Vida (Jo 14:6).\n\n📖 *Referências*: Cl 2:9, 1 Tm 2:5, Jo 14:6',
            'Cristo é o tema de toda a Bíblia. Do Gênesis ao Apocalipse, cada livro aponta para Ele. Ele é a semente da mulher (Gn 3:15), o cordeiro pascal (Ex 12), o profeta como Moisés (Dt 18:18), e o sumo sacerdote eterno (Hb 7).\n\nLewis dizia: "Ou Jesus era um lunático, ou era o Filho de Deus. Não podemos ignorá-lo." Cada um de nós precisa decidir quem é Jesus.\n\nQue Cristo seja o centro da sua vida hoje e sempre.\n\n📖 *Referências*: Cl 2:9, Jo 14:6, Hb 7:25',
        ],
        'passagens': ['Cl 2:9', 'Jo 14:6', '1 Tm 2:5', 'Hb 7:25', 'Fp 2:5-11'],
    },
    'espirito': {
        'respostas': [
            'O Espírito Santo é a pessoa da Trindade que habita no crente. "Não extingais o Espírito" (1 Ts 5:19). Ele convence do pecado, regenera, santifica e concede dons.\n\nCalvino ensinava que o Espírito é "o sentido espiritual" que nos permite compreender as Escrituras. Sem Ele, a Bíblia é letra morta.\n\nNão viva sem a direção do Espírito. Peça-Lhe que guie seus passos e renove sua mente cada dia.\n\n📖 *Referências*: 1 Ts 5:19, Jo 16:13, Rm 8:9',
            'O Espírito Santo é o consolador prometido por Jesus. "Outro Consolador, para que fique convosco para sempre" (Jo 14:16). Ele não é uma força impessoal, mas uma pessoa que habita em nós.\n\nTozer dizia: "O Espírito Santo não é apenas um invitado, mas o Senhor da casa." Devemos dar-Lhe controle total da nossa vida.\n\nPeça ao Espírito que lhe mostre verdades da Palavra hoje.\n\n📖 *Referências*: Jo 14:16, Jo 16:13, 1 Co 6:19',
        ],
        'passagens': ['Jo 14:16', 'Jo 16:13', 'Rm 8:9', 'Gl 5:22-23', 'Ef 5:18'],
    },
    'comunidade': {
        'respostas': [
            'A igreja é o corpo de Cristo na terra. "Vós sois o corpo de Cristo, e membros em particular" (1 Co 12:27). Ninguém pode viver a fé cristã isoladamente.\n\nA teologia reformada enfatiza que a salvação é individual, mas não é privada. Fomos salvos para ser parte do povo de Deus, da igreja visível.\n\nVocê tem uma comunidade de fé? Se não, busque uma igreja fiel à Palavra de Deus. Precisamos uns dos outros.\n\n📖 *Referências*: 1 Co 12:27, Hb 10:24-25, At 2:42',
            'O cristianismo é relacional. "Não nos esqueçamos de congregar-nos" (Hb 10:25). A comunhão dos santos é essencial para a vida cristã.\n\nBonhoeffer escreveu: "O cristão precisa de outro cristão que fale a Palavra de Deus." Sozinhos, somos frágeis. Juntos, somos fortes.\n\nParticipe de um grupo de estudo, um culto, ou uma comunhão de fé. Crescemos juntos em Cristo.\n\n📖 *Referências*: Hb 10:24-25, At 2:42-47, Ef 4:11-16',
        ],
        'passagens': ['1 Co 12:27', 'Hb 10:24-25', 'At 2:42', 'Ef 4:11-16', 'Mt 18:20'],
    },
    'biblia': {
        'respostas': [
            'A Bíblia é a Palavra inspirada de Deus. "Toda Escritura é inspirada por Deus e proveitosa para ensinar, para redarguir, para corrigir, para instruir em justiça" (2 Tm 3:16).\n\nLutero dizia: "A Escritura é a verdadeira Palavra de Deus, autoridade suprema em fé e prática." Ela é a autoridade suprema em assuntos de fé e prática.\n\nLeia a Bíblia todos os dias. Comece pelo Evangelho de João, depois seguindo um plano de leitura. A Palavra transforma quem a lê.\n\n📖 *Referências*: 2 Tm 3:16, Sl 119:105, Jo 5:39',
            'A Escritura é mais preciosa que o ouro. "Tua Palavra é lâmpada para os meus pés e luz para o meu caminho" (Sl 119:105). Ela nos guia em meio às trevas da vida.\n\nA infalibilidade da Bíblia é um pilar da fé reformada. Não erra em nada, pois Deus é seu autor. Podemos confiar em cada palavra.\n\nEstude a Bíblia com humildade e oração. O Espírito Santo ilumina a mente para compreender as verdades divinas.\n\n📖 *Referências*: Sl 119:105, 2 Tm 3:16, Jo 5:39',
        ],
        'passagens': ['2 Tm 3:16', 'Sl 119:105', 'Jo 5:39', '1 Pe 1:25', 'Is 40:8'],
    },
    'justica': {
        'respostas': [
            'Deus é justo e ama a justiça. "O Senhor é justo em todos os Seus caminhos" (Sl 145:17). A justiça de Deus é o padrão contra o qual somos medidos.\n\nA justificação pela fé é o artigo por qual a igreja se sustenta ou cai (Lutero). Somos declarados justos diante de Deus não por nossas obras, mas pela fé em Cristo.\n\nBusque a justiça social e pessoal. "Praticai a justiça, amai a misericórdia, e andai humildemente com o vosso Deus" (Mq 6:8).\n\n📖 *Referências*: Sl 145:17, Rm 3:26, Mq 6:8',
            'A justiça de Deus se revela no evangelho. "A justiça de Deus se manifesta pela fé em Jesus Cristo para todos os que crêem" (Rm 3:22). Não somos justos por mérito próprio, mas pela imputação da justiça de Cristo.\n\nA teologia reformada ensina que Cristo tornou-se pecado por nós para que nós tornássemos justiça de Deus Nele (2 Co 5:21). É a grande troca da salvação.\n\nViva como justo diante de Deus, não por medo, mas por gratidão.\n\n📖 *Referências*: Rm 3:22, 2 Co 5:21, Mq 6:8',
        ],
        'passagens': ['Rm 3:22', '2 Co 5:21', 'Mq 6:8', 'Sl 145:17', 'Ef 2:8-10'],
    },
    'tristeza': {
        'respostas': [
            'A tristeza é parte da vida humana, mas não é o fim. "Alegrai-vos sempre no Senhor" (Fp 4:4) — Paulo escreveu isso da prisão, mostrando que a alegria cristã transcende as circunstâncias.\n\nJesus chorou (Jo 11:35), chorou sobre Jerusalém (Lc 19:41). Ele entende nossa dor. Não temas sentir tristeza — mas não fiques nela.\n\nOre a Deus com sua dor. "De perto está o Senhor dos que têm o coração quebrantado" (Sl 34:18).\n\n📖 *Referências*: Fp 4:4, Sl 34:18, Jo 11:35',
            'Não tenha vergonha de estar triste. Jesus disse: "Neste mundo tereis aflições; mas tende bom ânimo, eu venci o mundo" (Jo 16:33).\n\nKeller dizia: "O evangelho não é apenas o começo da vida cristã; é o meio de tudo." Mesmo na tristeza, Cristo é suficiente.\n\nEntregue sua tristeza a Deus. Ele não a despreza, mas a recebe com compaixão.\n\n📖 *Referências*: Jo 16:33, Sl 42:1-3, 1 Pe 5:7',
        ],
        'passagens': ['Fp 4:4', 'Sl 34:18', 'Jo 16:33', 'Sl 42:1-3', '1 Pe 5:7'],
    },
    'medo': {
        'respostas': [
            'Deus não nos deu espírito de timidez, mas de fortaleza (2 Tm 1:7). O medo é natural, mas não deve nos governar. Em Cristo, somos mais que vencedores.\n\n"Não temas, porque eu sou contigo" é a frase mais repetida na Bíblia. Deus sabe que temos medo, e nos assegura de Sua presença.\n\nQuando o medo vier, lembre-se: Deus é maior que qualquer ameaça e não permite que sejamos provados além do que podemos suportar (1 Co 10:13).\n\n📖 *Referências*: 2 Tm 1:7, Js 1:9, 1 Co 10:13',
            'O medo paralisa, mas a fé move. Pedro andou sobre as águas enquanto olhava para Jesus (Mt 14:29). Quando olhou para as ondas, afundou. Olhe para Cristo, não para as circunstâncias.\n\nBonhoeffer: "Quando Cristo chama um homem, ele vem e morre." Isso inclui morrer para o medo.\n\nEntregue seus medos a Deus em oração. Ele é o nosso refúgio e fortaleza (Sl 46:1).\n\n📖 *Referências*: Mt 14:29-31, Sl 46:1, Is 41:10',
        ],
        'passagens': ['2 Tm 1:7', 'Js 1:9', 'Sl 46:1', 'Mt 14:29-31', 'Is 41:10'],
    },
    'duvida': {
        'respostas': [
            'A dúvida não é pecado — é oportunidade de fé crescer. Jesus disse ao pai do menino epiléptico: "Crede, e nada será impossível" (Mc 9:23). O homem respondeu: "Creio, mas ajuda a minha incredulidade."\n\nAté grandes homens de Deus tiveram dúvidas: Tomé, Jó e até João Batista. O importante é trazer as dúvidas a Cristo, não guardá-las para si.\n\nLeia a Bíblia, ore, converse com cristãos maduros. A fé cresce pelo estudo e pela comunidade.\n\n📖 *Referências*: Mc 9:23-24, Rm 10:17, Hb 11:1',
            'Dúvida intelectual pode ser resolvida com estudo. "Provai todas as coisas; retende o que é bom" (1 Ts 5:21). A fé reformada não pede para abandonar a razão, mas submetê-la à Palavra.\n\nLewis passou de ateu a cristão pela razão. C.S. Lewis dizia: "Eu creio no cristianismo assim como creio que o sol nasceu: não apenas porque o vejo, mas porque por ele vejo tudo."\n\nEstude as Escrituras e encontre respostas. A fé não é cega.\n\n📖 *Referências*: 1 Ts 5:21, Rm 10:17, Is 1:18',
        ],
        'passagens': ['Mc 9:23-24', 'Rm 10:17', 'Hb 11:1', '1 Ts 5:21', 'Is 1:18'],
    },
    'perdao': {
        'respostas': [
            'Assim como Cristo nos perdoou, somos chamados a perdoar. "Perdoai-vos uns aos outros, como também Deus vos perdoou em Cristo" (Ef 4:32). O perdão não é opcional para o cristão.\n\nSpurgeon dizia: "Perdoar é a maior semelhança com Deus a que um homem pode aspirar." O perdão é um ato de obediência a Deus que liberta o coração da amargura.\n\nSe alguém te ofendeu, ore por essa pessoa. Isso não significa concordar com o erro, mas libertar o coração da amargura.\n\n📖 *Referências*: Ef 4:32, Cl 3:13, Mt 6:14',
            'O perdão de Cristo na cruz é o modelo supremo. "Pai, perdoa-lhes, porque não sabem o que fazem" (Lc 23:34). Jesus perdoou Seus assassinos. Quem somos nós para guardar rancor?\n\nA parábola do servo impiedoso (Mt 18:21-35) nos mostra que quem recebeu tanto perdão não pode recusar perdoar aos outros.\n\nPerdoe hoje, antes que o ódio crie raízes. O perdão é um ato de obediência, não de sentimento.\n\n📖 *Referências*: Lc 23:34, Mt 18:21-35, Ef 4:32',
        ],
        'passagens': ['Ef 4:32', 'Cl 3:13', 'Lc 23:34', 'Mt 6:14-15', 'Mt 18:21-35'],
    },
    'proposito': {
        'respostas': [
            'Deus tem um propósito para sua vida. "Antes de te formar no ventre, eu te conheci" (Jr 1:5). Você não é acidental — é criado por Deus, para Deus, com um propósito eterno.\n\nA glória de Deus é o propósito supremo de toda a criação. Calvino dizia: "A glória de Deus é o objetivo último da criação e da redenção."\n\nPergunte a Deus: "Qual é o Teu propósito para minha vida?" Ele revela Sua vontade pela Palavra, pela oração e pela comunidade.\n\n📖 *Referências*: Jr 1:5, Ef 2:10, Rm 8:28',
            'Somos "obra-prima de Deus, criados em Cristo Jesus para boas obras, que Deus preparou de antemão" (Ef 2:10). O propósito cristão não é ser feliz, mas glorificar a Deus.\n\nKeller dizia: "Deus não nos deu um propósito para nossa vida; Ele é o propósito da nossa vida." Cristo é o centro, e tudo mais gira em torno Dele.\n\nDescubra seus dons, sirva na igreja, e viva para a glória de Deus.\n\n📖 *Referências*: Ef 2:10, 1 Co 10:31, Cl 3:23',
        ],
        'passagens': ['Ef 2:10', 'Jr 1:5', '1 Co 10:31', 'Rm 8:28', 'Cl 3:23'],
    },
    'familia': {
        'respostas': [
            'A família é instituição divina. "Honra teu pai e tua mãe" é o primeiro mandamento com promessa (Ef 6:2). Deus se importa com as famílias.\n\nPaulo ensina que o casamento é imagem da relação entre Cristo e a igreja (Ef 5:22-33). O amor do marido deve ser sacrificial como o de Cristo.\n\nInvista em sua família. Ore por eles, ensine-os a Palavra, e viva o evangelho no lar.\n\n📖 *Referências*: Ef 6:1-4, Ef 5:22-33, Dt 6:6-7',
            'O lar cristão é a primeira igreja. Pais, "criai-os na disciplina e admoestação do Senhor" (Ef 6:4). Isso não é opcional, mas mandamento.\n\nA família reformada prioriza a Palavra. "Estas palavras que hoje te ordeno, estarão no teu coração; e as ensinarás a teus filhos" (Dt 6:6-7).\n\nSe sua família está em crise, não desanime. Deus pode restaurar o que foi destruído. Ore sem cessar.\n\n📖 *Referências*: Ef 6:1-4, Dt 6:6-7, Sl 127:3',
        ],
        'passagens': ['Ef 6:1-4', 'Ef 5:22-33', 'Dt 6:6-7', 'Sl 127:3', 'Is 54:13'],
    },
    'sabedoria': {
        'respostas': [
            'O temor do Senhor é o princípio da sabedoria (Pv 1:7). A verdadeira sabedoria não vem da experiência humana, mas do reconhecimento da soberania de Deus.\n\nSalomão pediu sabedoria e Deus lhe deu um coração entendido. Se você pedir, Deus dará generosamente (Tg 1:5).\n\nLeia Proverbios todos os dias. É o manual de sabedoria prática para a vida.\n\n📖 *Referências*: Pv 1:7, Tg 1:5, Pv 4:7',
            'A sabedoria bíblica é aplicação do temor de Deus à vida cotidiana. Não é inteligência, mas discernimento espiritual.\n\n"A sabedoria lá de cima é, primeiramente pura, depois pacífica, moderada, persuasiva" (Tg 3:17). Note que a sabedoria divina começa com pureza.\n\nBusque sabedoria como quem busca ouro. Ela é mais preciosa que as riquezas deste mundo.\n\n📖 *Referências*: Tg 3:17, Pv 3:13-15, Pv 2:1-6',
        ],
        'passagens': ['Pv 1:7', 'Tg 1:5', 'Tg 3:17', 'Pv 3:13-15', 'Pv 2:1-6'],
    },
}

# Resposta genérica quando o tópico não é detectado
RESPOSTA_GENERICA = (
    "Que pergunta interessante! A Bíblia é rica em ensinamentos sobre muitos assuntos. "
    "Gostaria de compartilhar mais sobre o que está em seu coração? Estou aqui para estudar a Palavra com você.\n\n"
    "Enquanto isso, lembre-se: \"Buscai primeiro o reino de Deus e a Sua justiça, e todas estas coisas vos serão acrescentadas\" (Mt 6:33).\n\n"
    "📖 *Referências sugeridas*: Mt 6:33, Tg 1:5, Sl 119:105"
)


def _call_llm(prompt, temperature=0.3):
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(
        google_api_key=LLM_API_KEY,
        model=LLM_MODEL,
        temperature=temperature,
        request_timeout=15,
    )
    return llm.invoke(prompt).content.strip()


def gerar_dica_exercicio(exercicio, resposta_usuario=None):
    if not LLM_API_KEY:
        return gerar_dica_fallback(exercicio)
    try:
        prompt = f"""Você é um tutor bíblico reformado. Dê uma dica curta e pastoral:
Pergunta: {exercicio.enunciado}
Resposta: {resposta_usuario or 'N/A'}
Dica (max 2 frases):"""
        return _call_llm(prompt, temperature=0.3)
    except Exception as e:
        logger.warning(f'Erro ao gerar dica: {e}')
        return gerar_dica_fallback(exercicio)


def gerar_explicacao_licao(licao):
    if not LLM_API_KEY:
        return f'{licao.titulo}: {licao.resumo or licao.descricao}'
    try:
        prompt = f"""Explique esta lição bíblica de forma simples e pastoral (máx 4 frases):
Titulo: {licao.titulo}
Texto Base: {licao.texto_base}
Objetivo: {licao.objetivo}
Explicacao centrada em Cristo:"""
        return _call_llm(prompt, temperature=0.4)
    except Exception as e:
        logger.warning(f'Erro ao gerar explicacao: {e}')
        return f'{licao.titulo}: {licao.resumo or licao.descricao}'


def _detectar_topicos_da_mensagem(mensagem):
    """Detecta tópicos na mensagem do usuário."""
    msg_lower = mensagem.lower()
    topicos = []
    keywords_map = {
        'fe': ['fe', 'crença', 'crer', 'confiança', 'confiar', 'duvid', 'credulidade'],
        'graça': ['graça', 'graca', 'misericord', 'perdao', 'perdão', 'indigno', 'merecer'],
        'pecado': ['pecado', 'pecar', 'culpa', 'err', 'fracass', 'maldade', 'mal'],
        'amor': ['amor', 'amar', 'carinho', 'afeto', 'querer bem'],
        'oracao': ['orar', 'oração', 'oracao', 'pedir a deus', 'rezar', 'interceder'],
        'esperanca': ['esperan', 'esperar', 'futuro', 'amanhã', 'amanha'],
        'cristo': ['jesus', 'cristo', 'messias', 'salvador', 'filho de deus'],
        'espirito': ['espirito', 'espírito', 'santo', 'carismas', 'dons'],
        'comunidade': ['igreja', 'comunidade', 'irmaos', 'irmãos', 'congregação', 'culto'],
        'biblia': ['biblia', 'bíblia', 'escritura', 'palavra de deus', 'bíblico'],
        'justica': ['justiça', 'justica', 'igualdade', 'opressão', 'opressao'],
        'tristeza': ['triste', 'tristeza', 'chorar', 'choro', 'luto', 'dor', 'sofrimento'],
        'medo': ['medo', 'temor', 'receio', 'ansiedade', 'ansioso', 'preocupação', 'preocupacao'],
        'duvida': ['duvida', 'dúvida', 'não sei', 'nao sei', 'incerteza'],
        'perdao': ['perdoar', 'perdoa', 'perdão', 'perdao', 'rancor', 'mágoa', 'magoa'],
        'proposito': ['proposito', 'propósito', 'propósito', 'chamado', 'vocação', 'vocacao', 'sentido da vida'],
        'familia': ['familia', 'família', 'pai', 'mãe', 'mae', 'filhos', 'casamento', 'esposo', 'esposa'],
        'sabedoria': ['sabedoria', 'sábio', 'sabio', 'entendimento', 'discernimento'],
    }
    for topico, palavras in keywords_map.items():
        for p in palavras:
            if p in msg_lower:
                topicos.append(topico)
                break
    if not topicos:
        topicos = ['fe', 'esperanca']
    return topicos[:3]


def gerar_resposta_chat(mensagem, historico=None, tema='fe', categoria='devocional', faixa_etaria='adulto', nivel='iniciante'):
    """Gera resposta do chat devocional — respostas locais por tópico, respeitando tema e categoria."""
    try:
        topicos = _detectar_topicos_da_mensagem(mensagem)

        # Priorizar o tema selecionado se não detectado nenhum tópico específico
        if tema and tema not in topicos:
            topicos.insert(0, tema)

        # Adaptar resposta conforme categoria
        resposta = _gerar_resposta_fallback(mensagem, topicos)

        # Adicionar contextualização da categoria
        prefixo_categoria = _prefixo_por_categoria(categoria)
        if prefixo_categoria:
            resposta = prefixo_categoria + "\n\n" + resposta

        return resposta
    except Exception as e:
        logger.error(f'Erro no chat fallback: {e}')
        return (
            "Que pergunta interessante! A Bíblia é rica em ensinamentos sobre muitos assuntos. "
            "Gostaria de compartilhar mais sobre o que está em seu coração? Estou aqui para estudar a Palavra com você.\n\n"
            "📖 *Referências sugeridas*: Mt 6:33, Tg 1:5, Sl 119:105"
        )


def _prefixo_por_categoria(categoria):
    """Retorna um prefixo contextual conforme a categoria selecionada."""
    prefixos = {
        'devocional': None,  # Sem prefixo, resposta direta
        'estudo': "Vamos aprofundar esse estudo bíblico:",
        'oracao': "Vamos orientar sua oração sobre esse tema:",
        'conselho': "Com compaixão e baseado na Palavra:",
        'teologia': "Do ponto de vista da teologia reformada:",
    }
    return prefixos.get(categoria)


def _gerar_resposta_fallback(mensagem, topicos):
    """Gera resposta rica usando a base de dados por topico."""
    import hashlib

    msg_hash = int(hashlib.md5(mensagem.encode()).hexdigest()[:8], 16)

    resposta = ""
    for i, topico in enumerate(topicos[:2]):
        dados_topico = RESPOSTAS_POR_TOPICO.get(topico, None)
        if dados_topico and isinstance(dados_topico, dict):
            resp_list = dados_topico.get('respostas', [])
            if resp_list:
                idx = (msg_hash + i) % len(resp_list)
                resposta += resp_list[idx] + "\n\n---\n\n"

    if not resposta:
        resposta = RESPOSTA_GENERICA if isinstance(RESPOSTA_GENERICA, str) else str(RESPOSTA_GENERICA)

    try:
        from .theologians import formatar_resposta_teologos
        citacoes = formatar_resposta_teologos(topicos)
        if citacoes:
            resposta += "\n\n" + citacoes
    except Exception:
        pass

    return resposta.strip()


def gerar_devocional(tema, faixa_etaria='adulto', nivel='iniciante'):
    """Gera devocional usando o sistema de devocionais diarios."""
    from .devocionais import get_devocional_do_dia

    dev = get_devocional_do_dia()

    if LLM_API_KEY:
        try:
            prompt = f"""Crie um devocional bíblico completo (5-7 frases) para {faixa_etaria} sobre "{tema}".
Inclua: título, referência bíblica, reflexão e oração.
Tom pastoral reformado, centrado em Cristo.
Devocional:"""
            return _call_llm(prompt, temperature=0.5)
        except Exception as e:
            logger.warning(f'Erro LLM devocional: {e}')

    # Fallback com devocional do dia
    texto = f"**📖 {dev['titulo']}**\n\n"
    texto += f"*{dev['passagem']}*\n\n"
    if dev.get('texto'):
        texto += f"*\"{dev['texto']}\"*\n\n"
    texto += f"{dev['reflexao']}\n\n"
    texto += f"🙏 **Oração:** {dev['oracao']}"
    return texto


def gerar_dica_fallback(exercicio):
    dados = exercicio.dados
    if exercicio.tipo == 'MULTIPLA_ESCOLHA' and 'dica' in dados:
        return dados['dica']
    return 'Leia o texto base com atenção e procure a resposta que melhor reflete o que a Bíblia ensina.'
