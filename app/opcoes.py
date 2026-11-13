"""Listas fixas usadas nos formulários e nas telas."""

NIVEIS_DEPENDENCIA = ["Baixo", "Moderado", "Alto", "Muito alto"]

SINTOMAS = [
    "Ansiedade",
    "Irritação",
    "Dificuldade de concentração",
    "Fissura (vontade forte de usar)",
    "Insônia ou sono ruim",
    "Aumento do apetite",
    "Dor de cabeça",
    "Tosse",
    "Desânimo",
    "Outro",
]

GATILHOS = [
    "Ansiedade ou estresse",
    "Estudo ou trabalho",
    "Festa ou rolê com amigos",
    "Bebida alcoólica",
    "Depois de comer",
    "Ao acordar",
    "Tédio",
    "Ver alguém usando",
    "Outro",
]

CATEGORIAS_CONTEUDO = [
    "O que tem no pod",
    "Dependência",
    "Pulmões",
    "Coração",
    "Boca e dentes",
    "Câncer",
    "Jovens",
    "Acidentes",
    "Mitos e verdades",
    "Parar de usar",
    "Legislação",
]

# ícones do Bootstrap Icons usados nas matérias de cada categoria
ICONES_CATEGORIA = {
    "O que tem no pod": "bi-droplet-half",
    "Dependência": "bi-arrow-repeat",
    "Pulmões": "bi-lungs",
    "Coração": "bi-heart-pulse",
    "Boca e dentes": "bi-bandaid",
    "Câncer": "bi-clipboard2-pulse",
    "Jovens": "bi-people",
    "Acidentes": "bi-exclamation-triangle",
    "Mitos e verdades": "bi-question-circle",
    "Parar de usar": "bi-flag",
    "Legislação": "bi-bank",
}

STATUS_PROGRAMA = {
    "ativo": "Ativo",
    "concluido": "Concluído",
    "interrompido": "Interrompido",
}

STATUS_MISSAO = {
    "pendente": "Na fila",
    "em_andamento": "Em andamento",
    "concluida": "Concluída",
}

# RF10: canais oficiais de apoio. A chave também é usada para contar os cliques (seção 2.3)
CANAIS_APOIO = {
    "ubs": {
        "nome": "Unidade Básica de Saúde (UBS)",
        "descricao": (
            "O SUS oferece tratamento gratuito para quem quer parar de usar nicotina, com "
            "acompanhamento de profissionais de saúde e, quando indicado, medicamentos. "
            "Quem usa cigarro eletrônico também pode procurar esse atendimento. Vá até a UBS "
            "mais perto de você e pergunte sobre o tratamento do tabagismo."
        ),
        "link": "https://www.google.com/maps/search/UBS+perto+de+mim",
        "texto_link": "Procurar UBS no mapa",
        "icone": "bi-hospital",
    },
    "disque136": {
        "nome": "Disque Saúde 136",
        "descricao": (
            "Central de atendimento do Ministério da Saúde. A ligação é gratuita e dá para "
            "tirar dúvidas e descobrir onde fazer o tratamento na sua cidade."
        ),
        "link": "tel:136",
        "texto_link": "Ligar para 136",
        "icone": "bi-telephone",
    },
    "cvv": {
        "nome": "CVV - Centro de Valorização da Vida",
        "descricao": (
            "Se a ansiedade, a tristeza ou a vontade de desistir estiverem pesadas, o CVV "
            "conversa com você de graça, 24 horas por dia, pelo telefone 188, chat ou e-mail."
        ),
        "link": "https://cvv.org.br",
        "texto_link": "Abrir site do CVV",
        "icone": "bi-chat-heart",
    },
    "inca": {
        "nome": "INCA - Instituto Nacional de Câncer",
        "descricao": (
            "Órgão do Ministério da Saúde que coordena o Programa Nacional de Controle do "
            "Tabagismo. No site tem material sobre tratamento e sobre cigarro eletrônico."
        ),
        "link": "https://www.gov.br/inca/pt-br",
        "texto_link": "Abrir site do INCA",
        "icone": "bi-building",
    },
}
