"""Regras do programa de cessação e da fila de missões (RN01, RN02, RN03, RF04, RF05, RF09)."""
from datetime import date

from app.excecoes import RegraNegocioErro
from app.extensoes import db
from app.modelos import Missao, ProgramaCessacao, ProgramaMissao
from app.validacao import data_iso, inteiro

META_MINIMA = 7
META_MAXIMA = 365
DIAS_MAXIMOS_RETROATIVOS = 90


def catalogo_de_missoes():
    consulta = db.select(Missao).order_by(Missao.ordem_dia, Missao.id_missao)
    return db.session.scalars(consulta).all()


def total_missoes_catalogo():
    return db.session.scalar(db.select(db.func.count(Missao.id_missao)))


def obter_programa_do_usuario(usuario, id_programa):
    programa = db.session.get(ProgramaCessacao, id_programa)
    if programa is None or programa.id_pessoa_usuario != usuario.id_pessoa:
        return None
    return programa


def criar_programa(usuario, meta_dias, data_inicio=None, hoje=None):
    hoje = hoje or date.today()

    if not usuario.tem_perfil_consumo():
        raise RegraNegocioErro("Preencha o seu perfil de consumo antes de começar um programa.")
    # RN01
    if usuario.programa_ativo() is not None:
        raise RegraNegocioErro("Você já tem um programa ativo. Encerre o atual para começar outro.")

    meta = inteiro(meta_dias, "meta de dias", META_MINIMA, META_MAXIMA)
    inicio = data_iso(data_inicio, "data de início") if data_inicio else hoje
    if inicio > hoje:
        raise RegraNegocioErro("A data de início não pode ser no futuro.")
    if (hoje - inicio).days > DIAS_MAXIMOS_RETROATIVOS:
        raise RegraNegocioErro(f"A data de início pode ser no máximo {DIAS_MAXIMOS_RETROATIVOS} dias atrás.")

    missoes = catalogo_de_missoes()
    # RN02: o programa sempre começa pelo mapeamento dos gatilhos
    if not missoes or missoes[0].ordem_dia != 1 or not missoes[0].pode_ser_dia_um():
        raise RegraNegocioErro("O catálogo não tem a missão do dia 1 (mapeamento de gatilhos). Avise a moderação.")

    programa = ProgramaCessacao(
        usuario=usuario, data_inicio=inicio, meta_dias=meta, status=ProgramaCessacao.ATIVO
    )
    for posicao, missao in enumerate(missoes, start=1):
        programa.itens_fila.append(
            ProgramaMissao(missao=missao, posicao_fila=posicao, status=ProgramaMissao.PENDENTE)
        )

    usuario.data_inicio_abstinencia = inicio
    db.session.add(programa)
    liberar_proxima(programa)
    db.session.commit()
    return programa


def _garantir_ativo(programa):
    if programa.status != ProgramaCessacao.ATIVO:
        raise RegraNegocioErro("Esse programa já foi encerrado.")


def liberar_proxima(programa):
    """RN03: só tira uma missão da fila se não tiver outra em andamento."""
    atual = programa.missao_atual()
    if atual is not None:
        return atual
    fila = programa.montar_fila()
    if fila.esta_vazia():
        return None
    proxima = fila.desenfileirar()
    proxima.status = ProgramaMissao.EM_ANDAMENTO
    return proxima


def _mandar_para_o_fim(programa, item):
    ultima_posicao = max(i.posicao_fila for i in programa.itens_fila)
    item.status = ProgramaMissao.PENDENTE
    item.posicao_fila = ultima_posicao + 1


def concluir_missao_atual(programa, resposta=None, agora=None):
    _garantir_ativo(programa)
    programa.concluir_missao(resposta, agora)
    proxima = liberar_proxima(programa)
    db.session.commit()
    return proxima


def adiar_missao_atual(programa):
    """RN03: adiar de forma explícita também libera a próxima. A adiada vai para o fim da fila."""
    _garantir_ativo(programa)
    atual = programa.missao_atual()
    if atual is None:
        raise RegraNegocioErro("Não existe missão em andamento para adiar.")
    if programa.montar_fila().esta_vazia():
        raise RegraNegocioErro("Essa é a última missão da fila, então não dá para adiar.")
    _mandar_para_o_fim(programa, atual)
    proxima = liberar_proxima(programa)
    db.session.commit()
    return proxima


def reposicionar_apos_recaida(programa):
    """RF09: a recaída não zera o programa.

    A missão que estava em andamento volta para o fim da fila para ser tentada de novo
    mais tarde, e as missões concluídas continuam concluídas. Não faz commit, quem chama
    (o diário) é que fecha a transação.
    """
    atual = programa.missao_atual()
    if atual is None or programa.montar_fila().esta_vazia():
        return atual
    _mandar_para_o_fim(programa, atual)
    return liberar_proxima(programa)


def encerrar_programa(programa, motivo, hoje=None):
    _garantir_ativo(programa)
    hoje = hoje or date.today()
    if motivo == ProgramaCessacao.CONCLUIDO:
        if not programa.pode_ser_concluido(hoje):
            raise RegraNegocioErro(
                "O programa só pode ser marcado como concluído quando você chegar na meta de dias "
                "ou terminar todas as missões. Se quiser parar agora, use a opção de interromper."
            )
    elif motivo != ProgramaCessacao.INTERROMPIDO:
        raise RegraNegocioErro("Opção de encerramento inválida.")

    # RN01: o programa não é apagado, só muda de status e fica no histórico
    programa.status = motivo
    programa.data_fim = hoje
    db.session.commit()
