"""Regras do diário de progresso (RN04 a RN07, RN09, RF06, RF08)."""
from collections import Counter, defaultdict
from datetime import datetime, timedelta

from app.excecoes import RegraNegocioErro
from app.extensoes import db
from app.modelos import ProgramaCessacao, RegistroConquista, RegistroDiario, RegistroRecaida, RegistroSintoma
from app.servicos import programa_servico

TIPOS_REGISTRO = {
    "sintoma": RegistroSintoma,
    "recaida": RegistroRecaida,
    "conquista": RegistroConquista,
}

# RN07: 3 recaídas em 7 dias mostram os canais de apoio em destaque
LIMITE_RECAIDAS = 3
JANELA_DIAS_RECAIDAS = 7

PERIODOS_DO_DIA = [
    ("Madrugada (0h às 6h)", 0, 6),
    ("Manhã (6h às 12h)", 6, 12),
    ("Tarde (12h às 18h)", 12, 18),
    ("Noite (18h à 0h)", 18, 24),
]


def registrar_ocorrencia(usuario, tipo, dados, agora=None):
    programa = usuario.programa_ativo()
    if programa is None:
        raise RegraNegocioErro("Você precisa ter um programa ativo para registrar no diário.")
    classe = TIPOS_REGISTRO.get(tipo)
    if classe is None:
        raise RegraNegocioErro("Tipo de registro inválido.")

    # cada subclasse sabe validar os próprios campos
    registro = classe.criar_de_dados(dados)
    registro.data_hora = agora or datetime.now()
    programa.registrar(registro)  # RN04: entra no topo da pilha

    # RN06 / RF09: recaída zera o contador atual, mas o histórico e o recorde ficam
    if registro.impacto() < 0:
        usuario.data_inicio_abstinencia = registro.data_hora.date()
        programa_servico.reposicionar_apos_recaida(programa)

    db.session.commit()
    return registro


def obter_registro_do_usuario(usuario, id_registro):
    """RNF03: o diário só é visível para o próprio dono."""
    registro = db.session.get(RegistroDiario, id_registro)
    if registro is None or registro.programa.id_pessoa_usuario != usuario.id_pessoa:
        return None
    return registro


def complementar_registro(usuario, id_registro, texto, agora=None):
    registro = obter_registro_do_usuario(usuario, id_registro)
    if registro is None:
        raise RegraNegocioErro("Registro não encontrado.")
    registro.complementar(texto, agora)
    db.session.commit()
    return registro


def contar_recaidas_recentes(usuario, agora=None, dias=JANELA_DIAS_RECAIDAS):
    agora = agora or datetime.now()
    limite = agora - timedelta(days=dias)
    return sum(
        1
        for programa in usuario.programas
        for registro in programa.registros
        if registro.impacto() < 0 and limite <= registro.data_hora <= agora
    )


def precisa_alerta_apoio(usuario, agora=None):
    return contar_recaidas_recentes(usuario, agora) >= LIMITE_RECAIDAS


def _registros_do_usuario(usuario, classe):
    consulta = (
        db.select(classe)
        .join(classe.programa)
        .where(ProgramaCessacao.id_pessoa_usuario == usuario.id_pessoa)
        .order_by(classe.data_hora)
    )
    return db.session.scalars(consulta).all()


def _com_percentual(contagem, total):
    return [
        {"nome": nome, "quantidade": qtd, "percentual": round(qtd / total * 100) if total else 0}
        for nome, qtd in contagem
    ]


def _mapeamento_inicial(usuario):
    """Resposta da missão do dia 1 no programa mais recente."""
    for programa in reversed(usuario.programas):
        for item in programa.itens_fila:
            if item.missao.ordem_dia == 1 and item.resposta:
                return item.resposta
    return None


def resumo_padroes(usuario):
    """RF08: gatilhos, horários e sintomas que mais aparecem no diário."""
    todos = _registros_do_usuario(usuario, RegistroDiario)
    recaidas = _registros_do_usuario(usuario, RegistroRecaida)
    sintomas = _registros_do_usuario(usuario, RegistroSintoma)

    gatilhos = Counter(r.gatilho for r in recaidas).most_common()

    periodos = []
    for nome, inicio, fim in PERIODOS_DO_DIA:
        periodos.append((nome, sum(1 for r in recaidas if inicio <= r.data_hora.hour < fim)))

    intensidades = defaultdict(list)
    for registro in sintomas:
        intensidades[registro.sintoma].append(registro.intensidade)
    lista_sintomas = [
        {"nome": nome, "quantidade": len(valores), "media": round(sum(valores) / len(valores), 1)}
        for nome, valores in intensidades.items()
    ]
    lista_sintomas.sort(key=lambda s: (-s["quantidade"], -s["media"]))

    return {
        "total_registros": len(todos),
        "por_tipo": Counter(r.rotulo() for r in todos),
        "total_recaidas": len(recaidas),
        "gatilhos": _com_percentual(gatilhos, len(recaidas)),
        "periodos": _com_percentual(periodos, len(recaidas)),
        "sintomas": lista_sintomas,
        "mapeamento_inicial": _mapeamento_inicial(usuario),
    }
