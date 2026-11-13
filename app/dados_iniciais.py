"""Dados que o sistema precisa para funcionar: moderador, conteúdos e catálogo de missões."""
from datetime import date, datetime, time, timedelta

from app.extensoes import db
from app.modelos import (
    ConteudoInformativo,
    MissaoEducativa,
    MissaoPratica,
    MissaoReflexiva,
    Moderador,
    Pessoa,
)

EMAIL_MODERADOR = "moderador@japodquitar.com"
SENHA_MODERADOR = "Moderador@123"
EMAIL_DEMO = "demo@japodquitar.com"
SENHA_DEMO = "Demo@1234"

FONTE_INCA_2016 = (
    "INSTITUTO NACIONAL DE CÂNCER (INCA). Cigarros eletrônicos: o que sabemos? Estudo sobre a "
    "composição do vapor e danos à saúde, o papel na redução de danos e no tratamento da dependência "
    "de nicotina. Rio de Janeiro: INCA, 2016."
)
FONTE_OMS = "WORLD HEALTH ORGANIZATION (WHO). Tobacco: E-cigarettes (perguntas e respostas). Genebra: WHO, 2024."
FONTE_INCA_MANUAL = "INSTITUTO NACIONAL DE CÂNCER (INCA). Deixando de fumar sem mistérios: manual do participante. Rio de Janeiro: INCA."

# chave -> dados do conteúdo. A chave é usada para ligar as missões educativas.
CONTEUDOS = {
    "composicao": {
        "titulo": "O que tem dentro de um pod",
        "categoria": "O que tem no pod",
        "corpo": (
            "O líquido do pod normalmente tem nicotina, propilenoglicol, glicerina vegetal e aromatizantes. "
            "Quando o aparelho aquece esse líquido ele vira um aerossol, que muita gente chama de vapor, mas "
            "que na verdade é uma mistura de gotículas e partículas bem finas que vão direto para o pulmão.\n\n"
            "Além do que já vem no líquido, estudos encontraram no aerossol substâncias que se formam com o "
            "aquecimento, como formaldeído e acroleína, e também partículas de metais que saem da resistência "
            "do próprio aparelho, como níquel, chumbo e cromo.\n\n"
            "Muitos pods usam sais de nicotina, que deixam a tragada menos áspera na garganta. Isso faz a "
            "pessoa conseguir inalar bastante nicotina sem perceber. Em alguns modelos, um único refil tem "
            "uma quantidade de nicotina parecida com a de um maço inteiro de cigarros.\n\n"
            "Como a venda é proibida no Brasil, ninguém fiscaliza o que vai dentro de cada aparelho. O que "
            "está escrito na embalagem pode não ser o que tem de verdade no líquido."
        ),
        "fonte": f"{FONTE_INCA_2016}\n{FONTE_OMS}",
    },
    "dependencia": {
        "titulo": "Nicotina e dependência",
        "categoria": "Dependência",
        "corpo": (
            "A nicotina é a substância que causa a dependência, tanto no cigarro comum quanto no eletrônico. "
            "Ela chega ao cérebro em poucos segundos e libera dopamina, que dá aquela sensação rápida de alívio. "
            "Com o tempo o cérebro se acostuma e passa a pedir nicotina para a pessoa se sentir normal.\n\n"
            "Por isso, quando a pessoa fica um tempo sem usar, aparecem sintomas como irritação, ansiedade, "
            "dificuldade de concentração e uma vontade forte de usar, a chamada fissura. Isso não é falta de "
            "força de vontade, é uma resposta do corpo.\n\n"
            "Em adolescentes e jovens a atenção precisa ser maior, porque o cérebro continua em formação até "
            "por volta dos 25 anos. A nicotina nessa fase pode afetar atenção, memória e controle dos impulsos, "
            "além de aumentar a chance de dependência.\n\n"
            "Um detalhe do pod é que ele não tem um fim claro como o cigarro. Não tem maço, não tem bituca. "
            "A pessoa usa várias vezes ao longo do dia sem perceber quanto consumiu, e é por isso que anotar "
            "o uso no diário ajuda tanto."
        ),
        "fonte": (
            f"{FONTE_OMS}\n{FONTE_INCA_2016}\nU.S. DEPARTMENT OF HEALTH AND HUMAN SERVICES. E-Cigarette Use "
            "Among Youth and Young Adults: A Report of the Surgeon General. Atlanta, 2016."
        ),
    },
    "pulmoes": {
        "titulo": "O que acontece nos pulmões",
        "categoria": "Pulmões",
        "corpo": (
            "O aerossol do pod é inalado fundo e entra em contato direto com as vias respiratórias. Ele pode "
            "irritar e inflamar os brônquios, e muitos usuários contam que sentem tosse, chiado e falta de ar "
            "quando fazem exercício.\n\n"
            "Em 2019 os Estados Unidos tiveram um surto de lesão pulmonar ligada ao uso de cigarro eletrônico, "
            "que ficou conhecido como EVALI. Foram mais de 2.800 internações e 68 mortes confirmadas. A maior "
            "parte dos casos teve relação com líquidos que continham THC e acetato de vitamina E, mas o caso "
            "mostrou como um produto sem controle pode causar dano grave e rápido.\n\n"
            "Os efeitos de longo prazo ainda estão sendo estudados, porque esses aparelhos são relativamente "
            "novos. Ainda não ter todos os dados não quer dizer que o produto é seguro."
        ),
        "fonte": (
            "CENTERS FOR DISEASE CONTROL AND PREVENTION (CDC). Outbreak of Lung Injury Associated with the "
            f"Use of E-Cigarette, or Vaping, Products. Atlanta: CDC, 2020.\n{FONTE_INCA_2016}"
        ),
    },
    "coracao": {
        "titulo": "Coração e circulação",
        "categoria": "Coração",
        "corpo": (
            "A nicotina é estimulante: ela acelera os batimentos e aumenta a pressão arterial logo depois do uso. "
            "Ela também faz os vasos sanguíneos se contraírem. Quando isso acontece várias vezes por dia, todo "
            "dia, o sistema cardiovascular fica trabalhando sob esforço o tempo todo.\n\n"
            "As partículas finas do aerossol também chegam na corrente sanguínea e estão associadas a inflamação "
            "e a uma piora no funcionamento dos vasos.\n\n"
            "A parte boa é que o corpo começa a responder rápido quando a nicotina sai da rotina. Os batimentos e "
            "a pressão tendem a voltar ao normal e a circulação melhora já nas primeiras semanas sem uso."
        ),
        "fonte": f"{FONTE_OMS}\n{FONTE_INCA_2016}",
    },
    "troca": {
        "titulo": "Trocar o cigarro pelo pod não é parar",
        "categoria": "Parar de usar",
        "corpo": (
            "Muita gente começa no pod achando que é um jeito de largar o cigarro comum. Na prática, o que "
            "acontece com frequência é trocar uma forma de nicotina por outra, ou pior, usar os dois ao mesmo "
            "tempo (o chamado uso dual).\n\n"
            "A Organização Mundial da Saúde afirma que não há comprovação de que o cigarro eletrônico funcione "
            "como método para parar de fumar na população, e pede que os governos regulem esses produtos para "
            "proteger principalmente crianças e jovens.\n\n"
            "Os tratamentos que têm eficácia comprovada são o acompanhamento com profissional de saúde, que pode "
            "incluir terapia comportamental e, quando necessário, medicamentos como a reposição de nicotina. "
            "No Brasil esse tratamento é oferecido de graça pelo SUS. Na página Onde buscar ajuda tem mais detalhes."
        ),
        "fonte": f"{FONTE_OMS}\n{FONTE_INCA_2016}",
    },
    "abstinencia": {
        "titulo": "Abstinência: o que esperar nos primeiros dias",
        "categoria": "Parar de usar",
        "corpo": (
            "Quando a nicotina sai da rotina o corpo precisa de um tempo para se ajustar. Os sintomas mais comuns "
            "são vontade forte de usar, irritação, ansiedade, dificuldade de concentração, sono alterado e mais "
            "fome que o normal.\n\n"
            "Esses sintomas costumam ser mais fortes nos primeiros dias e vão diminuindo ao longo das semanas. "
            "A vontade intensa normalmente dura poucos minutos e passa, mesmo que você não use. Por isso as "
            "missões práticas do programa têm cronômetro: a ideia é atravessar esses minutos fazendo outra coisa.\n\n"
            "Algumas coisas ajudam: beber água, evitar exagerar no café, fazer alguma atividade física leve, "
            "dormir bem e avisar as pessoas próximas que você está passando por isso.\n\n"
            "Se os sintomas estiverem muito fortes, ou se aparecer uma tristeza que não passa, procure um "
            "profissional de saúde. Existe tratamento que alivia a abstinência."
        ),
        "fonte": FONTE_INCA_MANUAL,
    },
    "lei": {
        "titulo": "Pod é proibido no Brasil?",
        "categoria": "Legislação",
        "corpo": (
            "Sim. Desde 2009 a Anvisa proíbe a venda, a importação e a propaganda de dispositivos eletrônicos "
            "para fumar no Brasil. Em abril de 2024 a agência revisou o assunto e decidiu manter a proibição, "
            "publicando a RDC nº 855/2024, que também proíbe fabricar, armazenar, transportar e distribuir "
            "esses produtos.\n\n"
            "Isso quer dizer que todo pod vendido no país vem do mercado irregular. Não tem controle de "
            "qualidade, de origem nem da quantidade real de nicotina no líquido.\n\n"
            "A proibição é voltada principalmente para quem vende e distribui. Mesmo assim, quem usa fica "
            "exposto a um produto sem nenhuma fiscalização. E, assim como o cigarro comum, usar em ambiente "
            "coletivo fechado também não é permitido."
        ),
        "fonte": (
            "AGÊNCIA NACIONAL DE VIGILÂNCIA SANITÁRIA (ANVISA). Resolução da Diretoria Colegiada RDC nº 855, "
            "de 23 de abril de 2024.\nAGÊNCIA NACIONAL DE VIGILÂNCIA SANITÁRIA (ANVISA). Resolução da Diretoria "
            "Colegiada RDC nº 46, de 28 de agosto de 2009."
        ),
    },
    "recaida": {
        "titulo": "Recaída faz parte do caminho de muita gente",
        "categoria": "Parar de usar",
        "corpo": (
            "Muitas pessoas precisam de mais de uma tentativa até parar de vez. Usar de novo depois de alguns "
            "dias sem nicotina não apaga o que você já conseguiu: o seu corpo teve dias de descanso e você "
            "aprendeu alguma coisa sobre os seus gatilhos.\n\n"
            "O que costuma ajudar depois de uma recaída:\n"
            "- registrar no diário o que aconteceu e qual foi o gatilho, sem se culpar;\n"
            "- olhar o seu recorde de dias, porque ele mostra que você consegue;\n"
            "- pensar no que fazer diferente quando a mesma situação aparecer;\n"
            "- se as recaídas estiverem frequentes, procurar apoio profissional.\n\n"
            "Para família e amigos: cobrança e bronca costumam afastar a pessoa. Perguntar como ela está e "
            "oferecer companhia nos momentos difíceis ajuda bem mais."
        ),
        "fonte": f"{FONTE_INCA_MANUAL}\n{FONTE_OMS}",
    },
    # ---- matérias sobre os malefícios, cada uma baseada em um estudo publicado ----
    "diacetil": {
        "titulo": "Pulmão de pipoca: o diacetil escondido nos sabores",
        "categoria": "Pulmões",
        "corpo": (
            "Pesquisadores da Escola de Saúde Pública de Harvard analisaram 51 cigarros eletrônicos com sabor, "
            "incluindo sabores de fruta, doce e drinks, de marcas conhecidas e escolhidos por serem atraentes "
            "para jovens. Eles procuraram no aerossol três substâncias usadas para dar gosto amanteigado ou "
            "cremoso: diacetil, 2,3-pentanodiona e acetoína.\n\n"
            "## O que encontraram\n"
            "- o diacetil apareceu em 39 dos 51 sabores;\n"
            "- a acetoína apareceu em 46 e a 2,3-pentanodiona em 23;\n"
            "- 47 dos 51 sabores tinham pelo menos uma das três substâncias.\n\n"
            "## Por que isso preocupa\n"
            "O diacetil ficou conhecido no começo dos anos 2000, quando trabalhadores de fábricas de pipoca de "
            "micro-ondas, que respiravam esse aroma todos os dias, desenvolveram bronquiolite obliterante. É uma "
            "doença que cicatriza e fecha os bronquíolos, os menores canais de ar do pulmão, e por isso ganhou o "
            "apelido de pulmão de pipoca. O dano é irreversível e causa tosse e falta de ar.\n\n"
            "## O que ainda não se sabe\n"
            "O estudo mediu o que tinha no aerossol, e não quanto cada pessoa realmente inala nem se ela vai "
            "ficar doente. Até hoje não há casos confirmados de pulmão de pipoca causados por cigarro eletrônico. "
            "Mesmo assim, um aroma ser seguro para comer não quer dizer que ele seja seguro para inalar: o "
            "pulmão não tem as mesmas defesas do estômago."
        ),
        "fonte": (
            "ALLEN, J. G. et al. Flavoring chemicals in e-cigarettes: diacetyl, 2,3-pentanedione, and acetoin in "
            "a sample of 51 products, including fruit-, candy-, and cocktail-flavored e-cigarettes. "
            "Environmental Health Perspectives, v. 124, n. 6, p. 733-739, 2016."
        ),
    },
    "metais": {
        "titulo": "Chumbo, níquel e cromo: os metais que saem da resistência",
        "categoria": "O que tem no pod",
        "corpo": (
            "Pesquisadores da Universidade Johns Hopkins, nos Estados Unidos, recolheram os aparelhos de 56 "
            "pessoas que usavam cigarro eletrônico todos os dias e testaram 15 metais em três lugares: no frasco "
            "de refil, no líquido que já estava dentro do aparelho (em contato com a resistência) e no aerossol.\n\n"
            "## O que encontraram\n"
            "- o líquido do frasco quase não tinha metais;\n"
            "- depois de passar pela resistência aquecida, o líquido e o aerossol tinham bem mais;\n"
            "- a quantidade mediana de chumbo no aerossol foi mais de 25 vezes maior que no frasco de refil;\n"
            "- quase metade das amostras de aerossol tinha chumbo acima dos limites de saúde da agência "
            "ambiental americana (EPA);\n"
            "- níquel, cromo e manganês também chegaram perto ou passaram dos limites considerados seguros.\n\n"
            "## O que isso quer dizer\n"
            "A conclusão dos autores é que a própria resistência, a pecinha de metal que esquenta o líquido, "
            "solta metais que acabam indo para o pulmão. O chumbo afeta o sistema nervoso, e compostos de níquel "
            "e cromo inalados por muito tempo estão ligados a problemas respiratórios e a câncer.\n\n"
            "O estudo usou aparelhos de tanque, um pouco diferentes dos pods descartáveis, mas a ideia é a mesma "
            "em todos: uma resistência de metal aquecendo um líquido. E no Brasil, como a venda é proibida, "
            "ninguém controla a qualidade dos materiais usados nos aparelhos."
        ),
        "fonte": (
            "OLMEDO, P. et al. Metal concentrations in e-cigarette liquid and aerosol samples: the contribution "
            "of metallic coils. Environmental Health Perspectives, v. 126, n. 2, 2018."
        ),
    },
    "bronquite": {
        "titulo": "Tosse e bronquite em adolescentes que usam pod",
        "categoria": "Pulmões",
        "corpo": (
            "Um estudo feito no sul da Califórnia, com mais de 2 mil jovens com idade média de 17 anos, comparou "
            "quem nunca tinha usado cigarro eletrônico com quem usava ou já tinha usado.\n\n"
            "## Resultado\n"
            "Quem usava cigarro eletrônico tinha cerca de duas vezes mais chance de ter sintomas de bronquite, "
            "como tosse que não passa e catarro, do que quem nunca usou. Quem já tinha usado e parado também "
            "tinha chance maior (1,85 vez). E quanto mais dias no mês a pessoa usava, maior era o risco.\n\n"
            "## Mesmo sem nunca ter fumado cigarro\n"
            "O aumento dos sintomas apareceu também entre os jovens que nunca tinham fumado cigarro comum. Ou "
            "seja, o efeito não vem só de quem usa as duas coisas.\n\n"
            "## Cuidados na leitura\n"
            "Esse tipo de estudo mostra uma associação e não prova sozinho que o pod causou a bronquite. Os "
            "próprios autores pedem mais pesquisas sobre os efeitos de longo prazo. Mas o resultado combina com "
            "o que já se sabe sobre o aerossol irritar as vias aéreas."
        ),
        "fonte": (
            "McCONNELL, R. et al. Electronic cigarette use and respiratory symptoms in adolescents. American "
            "Journal of Respiratory and Critical Care Medicine, v. 195, n. 8, p. 1043-1049, 2017."
        ),
    },
    "coracao_estudo": {
        "titulo": "O que o pod faz com o coração de quem usa todo dia",
        "categoria": "Coração",
        "corpo": (
            "Pesquisadores da Universidade da Califórnia em Los Angeles (UCLA) compararam 23 adultos saudáveis, "
            "de 21 a 45 anos, que usavam cigarro eletrônico na maioria dos dias havia pelo menos um ano, com 19 "
            "pessoas que não usavam.\n\n"
            "## O que mediram\n"
            "- a variabilidade dos batimentos, que mostra se o corpo está em modo de alerta (o lado da "
            "adrenalina) ou em modo de descanso;\n"
            "- o estresse oxidativo, um tipo de desgaste das células ligado ao entupimento das artérias.\n\n"
            "## Resultado\n"
            "Em quem usava cigarro eletrônico, o coração estava mais puxado para o modo de alerta e o colesterol "
            "LDL (o chamado colesterol ruim) oxidava com mais facilidade. Em fumantes de cigarro comum, essas "
            "duas alterações são conhecidas por aumentar o risco de infarto.\n\n"
            "## Cuidados na leitura\n"
            "Foi um estudo pequeno e os autores dizem que ele não prova causa e efeito. Mas ele mostra que o uso "
            "diário não é neutro para o coração, e soma com o que já se sabe sobre a nicotina acelerar os "
            "batimentos e subir a pressão."
        ),
        "fonte": (
            "MOHEIMANI, R. S. et al. Increased cardiac sympathetic activity and oxidative stress in habitual "
            "electronic cigarette users: implications for cardiovascular risk. JAMA Cardiology, v. 2, n. 3, 2017."
        ),
    },
    "caries": {
        "titulo": "Cáries: o pod também deixa marca na boca",
        "categoria": "Boca e dentes",
        "corpo": (
            "Pesquisadores da faculdade de odontologia da Universidade Tufts, nos Estados Unidos, analisaram os "
            "prontuários de mais de 13 mil pacientes atendidos entre 2019 e 2022. Cada paciente tinha sido "
            "classificado pelo dentista como risco baixo, moderado ou alto de ter cárie.\n\n"
            "## Resultado\n"
            "Entre os pacientes que usavam cigarro eletrônico, cerca de 79% estavam no grupo de risco alto de "
            "cárie. Entre os que não usavam, eram cerca de 60%.\n\n"
            "## Por que pode acontecer\n"
            "Os autores lembram que o líquido do pod é viscoso e muitas vezes tem açúcares e aromas doces. "
            "Quando a pessoa puxa pela boca, essa mistura gruda nos dentes e pode alimentar as bactérias que "
            "causam a cárie.\n\n"
            "## Cuidados na leitura\n"
            "Só 136 pacientes do estudo usavam cigarro eletrônico, e não foi perguntado se o líquido tinha "
            "nicotina ou THC. A própria pesquisadora disse que o resultado é preliminar e precisa ser confirmado "
            "em estudos que acompanhem as pessoas por mais tempo. Mesmo assim, os autores recomendam que quem "
            "usa pod conte isso ao dentista, para ele reforçar a prevenção com flúor e consultas mais frequentes."
        ),
        "fonte": (
            "IRUSA, K. F. et al. A comparison of the caries risk between patients who use vapes or electronic "
            "cigarettes and those who do not: a cross-sectional study. Journal of the American Dental "
            "Association, v. 153, n. 12, p. 1179-1183, 2022."
        ),
    },
    "cancer": {
        "titulo": "Pod causa câncer? O que já se sabe e o que ainda não",
        "categoria": "Câncer",
        "corpo": (
            "Essa é uma das perguntas mais comuns, e a resposta honesta é que ainda não dá para dizer com "
            "certeza. O câncer costuma levar décadas para aparecer e o pod é um produto recente. Mas já existem "
            "sinais de alerta.\n\n"
            "## Em laboratório\n"
            "Em 2019, pesquisadores da Universidade de Nova York expuseram camundongos ao aerossol de cigarro "
            "eletrônico com nicotina por 54 semanas. 9 dos 40 animais (22,5%) desenvolveram câncer de pulmão e "
            "mais da metade teve alterações nas células da bexiga. Nenhum dos camundongos expostos ao aerossol "
            "sem nicotina teve câncer de pulmão.\n\n"
            "O estudo tem limites importantes: usou poucos animais, de uma linhagem que já tem tendência a ter "
            "câncer de pulmão, e os autores avisam que o resultado não pode ser passado direto para pessoas.\n\n"
            "## No aerossol\n"
            "Outros estudos já encontraram no aerossol substâncias que causam câncer, como o formaldeído, que se "
            "forma quando o líquido é aquecido, e metais como níquel e cromo, que saem da resistência (veja a "
            "matéria sobre os metais). Em geral as quantidades são menores do que na fumaça do cigarro comum, "
            "mas menor não quer dizer seguro.\n\n"
            "## O que fazer com essa informação\n"
            "Ainda vai levar anos até os estudos com pessoas darem uma resposta definitiva. Não é preciso esperar "
            "essa confirmação para decidir cuidar da saúde."
        ),
        "fonte": (
            "TANG, M. S. et al. Electronic-cigarette smoke induces lung adenocarcinoma and bladder urothelial "
            "hyperplasia in mice. Proceedings of the National Academy of Sciences, v. 116, n. 43, 2019.\n"
            "OLMEDO, P. et al. Metal concentrations in e-cigarette liquid and aerosol samples: the contribution "
            f"of metallic coils. Environmental Health Perspectives, v. 126, n. 2, 2018.\n{FONTE_INCA_2016}"
        ),
    },
    "porta_entrada": {
        "titulo": "Quem começa no pod tem mais chance de fumar cigarro depois",
        "categoria": "Jovens",
        "corpo": (
            "Uma dúvida comum é se o pod funciona como porta de entrada para o cigarro comum. Em 2017, uma "
            "revisão publicada na revista JAMA Pediatrics juntou 9 estudos que acompanharam ao longo do tempo "
            "17.389 adolescentes e jovens adultos que nunca tinham fumado.\n\n"
            "## Resultado\n"
            "- entre quem já tinha usado cigarro eletrônico, 30,4% começaram a fumar cigarro comum depois;\n"
            "- entre quem nunca tinha usado, foram 7,9%;\n"
            "- mesmo levando em conta outros fatores de risco, quem já tinha usado cigarro eletrônico teve "
            "cerca de 3,6 vezes mais chance de começar a fumar.\n\n"
            "## Cuidados na leitura\n"
            "Estudos desse tipo mostram uma associação e não provam sozinhos que um causa o outro. Alguns "
            "críticos dizem que jovens que gostam de experimentar coisas novas usariam os dois de qualquer jeito. "
            "Ainda assim, é um sinal que preocupa pesquisadores e órgãos de saúde.\n\n"
            "## Por que faz sentido\n"
            "O pod entrega nicotina, a substância que causa a dependência. Depois que o corpo se acostuma com "
            "ela, a pessoa pode passar a buscar nicotina em outras formas, inclusive no cigarro comum."
        ),
        "fonte": (
            "SONEJI, S. et al. Association between initial use of e-cigarettes and subsequent cigarette smoking "
            "among adolescents and young adults: a systematic review and meta-analysis. JAMA Pediatrics, "
            "v. 171, n. 8, 2017."
        ),
    },
    "sabores": {
        "titulo": "Sabor de fruta e de bala: a isca para atrair jovens",
        "categoria": "Jovens",
        "corpo": (
            "Menta, morango, melancia, algodão-doce, chiclete. Os pods têm sabores que parecem feitos para quem "
            "nunca fumou, e as pesquisas mostram que isso funciona.\n\n"
            "## O que dizem os números\n"
            "Na pesquisa nacional sobre tabaco entre jovens dos Estados Unidos (National Youth Tobacco Survey), "
            "feita em 2024 com estudantes do ensino fundamental e médio, 87,6% dos que usavam cigarro eletrônico "
            "usavam algum sabor que não era de tabaco. Os preferidos foram fruta (62,8%), doce ou bala (33,3%) e "
            "menta (25,1%).\n\n"
            "## Por que o sabor importa\n"
            "- o gosto doce disfarça a aspereza da nicotina e facilita a primeira tragada;\n"
            "- passa a impressão de que o produto é leve ou inofensivo;\n"
            "- aromas liberados para alimentos não foram testados para serem inalados (veja a matéria sobre o "
            "diacetil).\n\n"
            "## E no Brasil?\n"
            "Aqui a venda de qualquer cigarro eletrônico é proibida pela Anvisa, mas os pods com sabor continuam "
            "chegando aos jovens pelo comércio irregular, inclusive pela internet."
        ),
        "fonte": (
            "CENTERS FOR DISEASE CONTROL AND PREVENTION (CDC). Notes from the field: e-cigarette and nicotine "
            "pouch use among middle and high school students, United States, 2024. Morbidity and Mortality "
            "Weekly Report, v. 73, n. 35, 2024."
        ),
    },
    "brasil_jovens": {
        "titulo": "Uso de pod entre adolescentes quase dobrou no Brasil",
        "categoria": "Jovens",
        "corpo": (
            "A Pesquisa Nacional de Saúde do Escolar (PeNSE), feita pelo IBGE com estudantes de 13 a 17 anos, "
            "mostrou um crescimento grande na experimentação de cigarro eletrônico.\n\n"
            "## Os números\n"
            "- em 2019, 16,8% dos estudantes já tinham experimentado cigarro eletrônico;\n"
            "- na edição de 2024, divulgada em março de 2026, esse número subiu para 29,6%;\n"
            "- entre as meninas a experimentação foi maior: 31,7%, contra 27,4% entre os meninos;\n"
            "- no mesmo período, a experimentação do cigarro comum caiu de 22,6% para 18,5%.\n\n"
            "Entre os jovens adultos o cenário é parecido. O inquérito Covitel 2023 estimou que cerca de 24% das "
            "pessoas de 18 a 24 anos já tinham usado cigarro eletrônico.\n\n"
            "## O que isso mostra\n"
            "Depois de décadas de queda no tabagismo, a nicotina está voltando para a vida dos jovens por outro "
            "caminho. E isso acontece mesmo com a venda proibida desde 2009, o que mostra como o comércio "
            "irregular facilita o acesso.\n\n"
            "Se você faz parte desses números, saiba que não está sozinho e que dá para parar."
        ),
        "fonte": (
            "INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). Pesquisa Nacional de Saúde do Escolar: "
            "2019. Rio de Janeiro: IBGE, 2021.\n"
            "INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). Pesquisa Nacional de Saúde do Escolar: "
            "2024. Rio de Janeiro: IBGE, 2026.\n"
            "VITAL STRATEGIES; UNIVERSIDADE FEDERAL DE PELOTAS. Covitel: Inquérito Telefônico de Fatores de "
            "Risco para Doenças Crônicas não Transmissíveis em Tempos de Pandemia. Relatório 2023."
        ),
    },
    "bateria": {
        "titulo": "Explosões e queimaduras: o risco que vem da bateria",
        "categoria": "Acidentes",
        "corpo": (
            "Todo pod tem uma bateria de lítio. Quando ela tem defeito, é carregada do jeito errado ou entra em "
            "curto, pode esquentar demais, pegar fogo ou até explodir, muitas vezes no bolso ou na mão de quem "
            "está usando.\n\n"
            "## Quantos casos?\n"
            "Um estudo publicado na revista Tobacco Control usou registros de pronto-socorros dos Estados Unidos "
            "e estimou 2.035 atendimentos por explosões e queimaduras com cigarro eletrônico entre 2015 e 2017. "
            "Os autores avisam que o número real deve ser maior, porque nem todo mundo que se queima vai ao "
            "pronto-socorro. Em uma atualização com dados até 2018, a estimativa passou de 2.600 casos, e muitos "
            "acidentes aconteceram na hora de trocar ou mexer na bateria.\n\n"
            "## Como diminuir o risco\n"
            "- não carregar baterias soltas no bolso junto com moedas ou chaves;\n"
            "- usar só o carregador do próprio aparelho e não deixar carregando sem ninguém olhando;\n"
            "- não usar aparelho com bateria estufada, molhada ou danificada;\n"
            "- descartar pods e baterias em ponto de coleta de lixo eletrônico, nunca no lixo comum.\n\n"
            "No Brasil a situação é ainda mais arriscada, porque todos os aparelhos vêm do mercado irregular, "
            "sem nenhum teste de segurança."
        ),
        "fonte": (
            "ROSSHEIM, M. E. et al. Electronic cigarette explosion and burn injuries, US Emergency Departments "
            "2015-2017. Tobacco Control, v. 28, n. 4, 2019.\n"
            "U.S. FOOD AND DRUG ADMINISTRATION (FDA). Tips to help avoid vape battery explosions."
        ),
    },
    "intoxicacao": {
        "titulo": "Refil perto de criança é perigo: intoxicação por nicotina",
        "categoria": "Acidentes",
        "corpo": (
            "O líquido do pod tem nicotina concentrada, cheiro doce e, muitas vezes, embalagem colorida. Para uma "
            "criança pequena, isso parece bala ou suco.\n\n"
            "## O que mostram os dados\n"
            "Um estudo publicado na revista Pediatrics analisou os chamados aos centros de intoxicação dos Estados "
            "Unidos entre 2012 e abril de 2017 e encontrou 8.269 casos de exposição à nicotina líquida em "
            "crianças com menos de 6 anos.\n"
            "- 92,5% das crianças engoliram o líquido;\n"
            "- 83,9% tinham menos de 3 anos;\n"
            "- cerca de 35% precisaram ser atendidas em um serviço de saúde e 1,4% foram internadas;\n"
            "- houve uma morte.\n\n"
            "## Sinais de intoxicação\n"
            "Vômito, salivação, suor, tontura, coração acelerado e, nos casos graves, convulsão. Em criança "
            "pequena, pouca quantidade de líquido já pode ser perigosa.\n\n"
            "## O que fazer\n"
            "- guardar pods e refis fora do alcance e da vista das crianças;\n"
            "- nunca deixar refil aberto ou aparelho largado na mesa ou no sofá;\n"
            "- se uma criança engolir ou derramar o líquido na pele, ligar para o Disque-Intoxicação "
            "(0800 722 6001) ou procurar atendimento na hora."
        ),
        "fonte": (
            "GOVINDARAJAN, P. et al. E-cigarette and liquid nicotine exposures among young children. Pediatrics, "
            "v. 141, n. 5, e20173361, 2018.\n"
            "AGÊNCIA NACIONAL DE VIGILÂNCIA SANITÁRIA (ANVISA). Disque-Intoxicação: 0800 722 6001."
        ),
    },
    "mitos": {
        "titulo": "Mitos e verdades sobre o pod",
        "categoria": "Mitos e verdades",
        "corpo": (
            "Muita coisa que circula sobre o pod em grupo de amigos e em rede social não bate com o que as "
            "pesquisas mostram. Separamos as frases mais comuns.\n\n"
            "## Mito: é só vapor de água\n"
            "O que sai do pod é um aerossol com nicotina, propilenoglicol, glicerina, aromas e partículas finas. "
            "Estudos já encontraram metais como chumbo e níquel (Olmedo et al., 2018) e aromas como o diacetil "
            "(Allen et al., 2016).\n\n"
            "## Mito: não causa dependência como o cigarro\n"
            "A nicotina é a mesma substância que causa dependência no cigarro comum. Com os sais de nicotina, "
            "alguns refis entregam quase tanta nicotina quanto um maço inteiro.\n\n"
            "## Mito: usar só de vez em quando não faz mal\n"
            "Em adolescentes da Califórnia, até quem já tinha parado de usar tinha mais sintomas de bronquite do "
            "que quem nunca usou (McConnell et al., 2017).\n\n"
            "## Mito: é um bom jeito de parar de fumar\n"
            "A OMS afirma que não há comprovação de que o cigarro eletrônico funcione para parar de fumar na "
            "população. O que tem eficácia comprovada é o tratamento com profissional de saúde, que o SUS oferece "
            "de graça.\n\n"
            "## Mito: se não tem cheiro, não incomoda ninguém\n"
            "O aerossol que a pessoa solta também tem nicotina e partículas finas, e quem está perto acaba "
            "respirando. Por isso o uso em ambiente coletivo fechado não é permitido.\n\n"
            "## Verdade: parar traz benefícios rápidos\n"
            "Os batimentos e a pressão começam a melhorar pouco tempo depois que a nicotina sai da rotina, e os "
            "sintomas de abstinência costumam diminuir ao longo das semanas."
        ),
        "fonte": (
            f"{FONTE_OMS}\n"
            "OLMEDO, P. et al. Environmental Health Perspectives, v. 126, n. 2, 2018.\n"
            "ALLEN, J. G. et al. Environmental Health Perspectives, v. 124, n. 6, p. 733-739, 2016.\n"
            "McCONNELL, R. et al. American Journal of Respiratory and Critical Care Medicine, v. 195, n. 8, "
            f"p. 1043-1049, 2017.\n{FONTE_INCA_MANUAL}"
        ),
    },
}

# catálogo inicial: 21 missões, uma por dia, alternando os três tipos
MISSOES = [
    (MissaoReflexiva, {
        "ordem_dia": 1,
        "titulo": "Mapeie seus gatilhos",
        "descricao": "Antes de mudar qualquer coisa, a ideia é entender em que momentos o pod aparece no seu dia. "
                     "O resto do programa usa esse mapeamento.",
        "pergunta_gatilho": "Em quais situações você costuma usar o pod? Pense em lugares, horários, pessoas e "
                            "sentimentos (por exemplo: ao acordar, estudando, ansioso, em festa, depois de comer). "
                            "Escreva as que mais acontecem com você e qual delas é a mais forte.",
    }),
    (MissaoEducativa, {
        "ordem_dia": 2,
        "titulo": "O que você está inalando",
        "descricao": "Entender o que tem no aerossol ajuda a desmontar a ideia de que é só vapor com sabor.",
        "conteudo": "composicao",
    }),
    (MissaoPratica, {
        "ordem_dia": 3,
        "titulo": "Adie o primeiro uso do dia",
        "descricao": "O primeiro uso do dia costuma ser o mais automático. Hoje você vai empurrar ele um pouco.",
        "acao_substituta": "Quando sentir vontade de usar pela primeira vez hoje, espere 15 minutos antes. "
                           "Nesse tempo, beba um copo de água.",
        "duracao_min": 15,
    }),
    (MissaoReflexiva, {
        "ordem_dia": 4,
        "titulo": "Seus motivos",
        "descricao": "Nos dias difíceis ajuda muito lembrar por que você começou.",
        "pergunta_gatilho": "Por que você quer parar? Escreva pelo menos três motivos que fazem sentido para "
                            "você, não para os outros.",
    }),
    (MissaoPratica, {
        "ordem_dia": 5,
        "titulo": "Respiração quadrada",
        "descricao": "Uma técnica simples para usar no momento da vontade, em qualquer lugar.",
        "acao_substituta": "Na próxima vontade, respire contando: puxa o ar em 4 segundos, segura 4, solta em 4, "
                           "segura 4. Repita até o cronômetro acabar.",
        "duracao_min": 3,
    }),
    (MissaoEducativa, {
        "ordem_dia": 6,
        "titulo": "Por que é tão difícil parar",
        "descricao": "Saber como a nicotina age no cérebro tira o peso de achar que é só falta de força de vontade.",
        "conteudo": "dependencia",
    }),
    (MissaoPratica, {
        "ordem_dia": 7,
        "titulo": "Pod longe de você",
        "descricao": "Muito do uso acontece só porque o aparelho está ali, na mão ou no bolso.",
        "acao_substituta": "Deixe o pod em outro cômodo ou dentro da mochila fechada, longe do alcance, e fique "
                           "esse tempo sem pegar nele.",
        "duracao_min": 60,
    }),
    (MissaoReflexiva, {
        "ordem_dia": 8,
        "titulo": "Sua rede de apoio",
        "descricao": "Parar sozinho é mais pesado. Pensar em quem pode ajudar já é um passo.",
        "pergunta_gatilho": "Quem pode te apoiar nesse processo? Escreva o nome de uma ou duas pessoas e como você "
                            "pretende contar para elas.",
    }),
    (MissaoEducativa, {
        "ordem_dia": 9,
        "titulo": "Trocar não é parar",
        "descricao": "Para quem saiu do cigarro comum e foi para o pod, ou pensa em fazer isso.",
        "conteudo": "troca",
    }),
    (MissaoPratica, {
        "ordem_dia": 10,
        "titulo": "Caminhada na hora da vontade",
        "descricao": "Movimentar o corpo ajuda a vontade a passar mais rápido.",
        "acao_substituta": "Quando a vontade vier, saia para uma caminhada curta, mesmo que seja dentro de casa "
                           "ou no corredor da faculdade.",
        "duracao_min": 10,
    }),
    (MissaoReflexiva, {
        "ordem_dia": 11,
        "titulo": "Olhe para o seu diário",
        "descricao": "Depois de alguns dias de registros já dá para enxergar padrões.",
        "pergunta_gatilho": "Abra o seu diário e a página de padrões. Em que horário ou situação a vontade aparece "
                            "mais? O que você pode mudar nessa situação?",
    }),
    (MissaoEducativa, {
        "ordem_dia": 12,
        "titulo": "Abstinência tem começo, meio e fim",
        "descricao": "Os sintomas assustam menos quando você sabe o que esperar.",
        "conteudo": "abstinencia",
    }),
    (MissaoPratica, {
        "ordem_dia": 13,
        "titulo": "Ocupe a boca e as mãos",
        "descricao": "Parte do hábito é o gesto. Dá para trocar o gesto por outro.",
        "acao_substituta": "Na próxima vontade, troque o pod por algo para mastigar ou segurar: chiclete sem "
                           "açúcar, cenoura, uma garrafinha de água, uma caneta.",
        "duracao_min": 5,
    }),
    (MissaoReflexiva, {
        "ordem_dia": 14,
        "titulo": "Plano para o rolê",
        "descricao": "Festa e encontro com amigos são gatilhos muito comuns. Melhor chegar com um plano.",
        "pergunta_gatilho": "Pense na próxima festa, bar ou encontro com amigos que usam pod. O que você vai "
                            "responder quando oferecerem? O que você vai fazer no lugar?",
    }),
    (MissaoEducativa, {
        "ordem_dia": 15,
        "titulo": "Seu coração agradece",
        "descricao": "O que a nicotina faz com a pressão e com os batimentos.",
        "conteudo": "coracao",
    }),
    (MissaoPratica, {
        "ordem_dia": 16,
        "titulo": "Três horas sem pod",
        "descricao": "Um desafio maior, usando o que você aprendeu nas missões anteriores.",
        "acao_substituta": "Escolha um período em que você está acordado e fique três horas seguidas sem usar. "
                           "Se a vontade apertar, use a respiração ou a caminhada.",
        "duracao_min": 180,
    }),
    (MissaoReflexiva, {
        "ordem_dia": 17,
        "titulo": "O que já mudou",
        "descricao": "Às vezes a gente não percebe o quanto já avançou.",
        "pergunta_gatilho": "Compare como você está hoje com o primeiro dia do programa. Mudou alguma coisa no "
                            "fôlego, no sono, no dinheiro ou no jeito de lidar com a vontade?",
    }),
    (MissaoEducativa, {
        "ordem_dia": 18,
        "titulo": "Pulmões e aerossol",
        "descricao": "O que se sabe até agora sobre o efeito do pod no sistema respiratório.",
        "conteudo": "pulmoes",
    }),
    (MissaoPratica, {
        "ordem_dia": 19,
        "titulo": "Desapego dos acessórios",
        "descricao": "Ter refil e carregador por perto deixa a recaída a um passo.",
        "acao_substituta": "Separe pods, refis e carregadores que ainda estiverem com você e leve a um ponto de "
                           "coleta de lixo eletrônico (o aparelho tem bateria de lítio e não deve ir para o lixo "
                           "comum). Aproveite para apagar o contato de quem vende.",
        "duracao_min": 20,
    }),
    (MissaoReflexiva, {
        "ordem_dia": 20,
        "titulo": "Plano para uma recaída",
        "descricao": "Ter um plano pronto evita que um deslize vire desistência.",
        "pergunta_gatilho": "Se você usar de novo em algum momento, o que vai fazer logo depois? Escreva um plano "
                            "curto para voltar ao programa sem desistir.",
    }),
    (MissaoEducativa, {
        "ordem_dia": 21,
        "titulo": "Pod e a lei no Brasil",
        "descricao": "Entender por que todo pod vendido aqui vem do mercado irregular.",
        "conteudo": "lei",
    }),
]


def popular_banco():
    """Cria os dados iniciais. Se já existir moderador, entende que já foi feito e não faz nada."""
    if db.session.scalars(db.select(Moderador)).first() is not None:
        return False

    moderador = Moderador(
        nome="Equipe de moderação",
        email=EMAIL_MODERADOR,
        registro_profissional="Projeto acadêmico",
        area_atuacao="Educação em saúde",
    )
    moderador.definir_senha(SENHA_MODERADOR)
    db.session.add(moderador)

    conteudos = {}
    for chave, dados in CONTEUDOS.items():
        conteudo = ConteudoInformativo(**dados)
        moderador.publicar(conteudo)
        db.session.add(conteudo)
        conteudos[chave] = conteudo

    for classe, dados in MISSOES:
        dados = dict(dados)
        if "conteudo" in dados:
            dados["conteudo"] = conteudos[dados["conteudo"]]
        db.session.add(classe(**dados))

    db.session.commit()
    return True


def adicionar_conteudos_novos():
    """Coloca no banco as matérias da lista CONTEUDOS que ainda não existem (compara pelo título).

    Serve para quem já tinha o banco criado antes de novas matérias serem escritas.
    Só roda quando alguém executa o seed.py, para não recriar algo que o moderador apagou de propósito.
    """
    moderador = db.session.scalars(db.select(Moderador)).first()
    if moderador is None:
        return 0
    existentes = set(db.session.scalars(db.select(ConteudoInformativo.titulo)))
    novos = 0
    for dados in CONTEUDOS.values():
        if dados["titulo"] in existentes:
            continue
        conteudo = ConteudoInformativo(**dados)
        moderador.publicar(conteudo)
        db.session.add(conteudo)
        novos += 1
    db.session.commit()
    return novos


def criar_usuario_demo():
    """Usuário com uns 12 dias de programa, para mostrar o sistema funcionando."""
    from app.servicos import conta_servico, diario_servico, programa_servico

    if db.session.scalar(db.select(Pessoa).where(Pessoa.email == EMAIL_DEMO)) is not None:
        return False

    hoje = date.today()
    inicio = hoje - timedelta(days=12)

    def momento(dia, hora, minuto=0):
        return datetime.combine(inicio + timedelta(days=dia), time(hora, minuto))

    usuario = conta_servico.cadastrar_usuario("Demo", EMAIL_DEMO, SENHA_DEMO, SENHA_DEMO, True)
    conta_servico.salvar_perfil_consumo(usuario, {
        "consumo_diario_anterior": "300",
        "custo_semanal_anterior": "60",
        "nivel_dependencia": "Alto",
        "tempo_uso_meses": "18",
    })
    programa = programa_servico.criar_programa(usuario, 30, inicio.isoformat(), hoje=hoje)

    # a ordem das chamadas segue a ordem do tempo, igual aconteceria de verdade
    diario_servico.registrar_ocorrencia(usuario, "sintoma", {
        "sintoma": "Ansiedade", "intensidade": "4",
        "observacao": "Primeira tarde sem o pod, fiquei inquieto na aula.",
    }, agora=momento(0, 16, 30))
    programa_servico.concluir_missao_atual(
        programa,
        "Ao acordar, quando estou estudando para prova e quando saio com o pessoal da sala. "
        "O mais forte é estudando, fico ansioso e pego o pod sem nem pensar.",
        agora=momento(0, 21),
    )
    programa_servico.concluir_missao_atual(programa, agora=momento(1, 10))
    diario_servico.registrar_ocorrencia(usuario, "sintoma", {
        "sintoma": "Insônia ou sono ruim", "intensidade": "3",
    }, agora=momento(1, 23, 10))
    diario_servico.registrar_ocorrencia(usuario, "conquista", {
        "marco": "Fiquei o dia inteiro sem usar",
    }, agora=momento(2, 20))
    programa_servico.concluir_missao_atual(programa, agora=momento(2, 20, 5))
    programa_servico.concluir_missao_atual(
        programa,
        "Quero voltar a correr sem ficar sem fôlego, parar de gastar dinheiro com isso e não depender "
        "do pod para conseguir estudar.",
        agora=momento(3, 19),
    )
    diario_servico.registrar_ocorrencia(usuario, "recaida", {
        "quantidade_puffs": "25", "gatilho": "Festa ou rolê com amigos",
        "observacao": "Aniversário de um amigo, todo mundo usando.",
    }, agora=momento(5, 23, 40))
    diario_servico.registrar_ocorrencia(usuario, "conquista", {
        "marco": "Voltei para o programa no dia seguinte",
    }, agora=momento(6, 9))
    programa_servico.concluir_missao_atual(programa, agora=momento(6, 12))
    diario_servico.registrar_ocorrencia(usuario, "sintoma", {
        "sintoma": "Fissura (vontade forte de usar)", "intensidade": "3",
    }, agora=momento(8, 15))
    programa_servico.concluir_missao_atual(programa, agora=momento(8, 15, 20))
    diario_servico.registrar_ocorrencia(usuario, "conquista", {
        "marco": "Recusei quando me ofereceram no intervalo da faculdade",
    }, agora=momento(10, 18))
    diario_servico.registrar_ocorrencia(usuario, "sintoma", {
        "sintoma": "Irritação", "intensidade": "2",
    }, agora=momento(11, 8, 30))
    return True
