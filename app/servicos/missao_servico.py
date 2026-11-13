"""CRUD do catálogo de missões, feito pelo moderador."""
from app.excecoes import RegraNegocioErro
from app.extensoes import db
from app.modelos import Missao, MissaoEducativa, MissaoPratica, MissaoReflexiva, ProgramaMissao
from app.servicos import programa_servico

TIPOS_MISSAO = {
    "reflexiva": MissaoReflexiva,
    "pratica": MissaoPratica,
    "educativa": MissaoEducativa,
}


def listar_catalogo():
    """Lista de (missao, quantidade de programas que usam a missão)."""
    usos = dict(
        db.session.execute(
            db.select(ProgramaMissao.id_missao, db.func.count()).group_by(ProgramaMissao.id_missao)
        ).all()
    )
    return [(missao, usos.get(missao.id_missao, 0)) for missao in programa_servico.catalogo_de_missoes()]


def _existe_outra_missao_dia_um(missao):
    consulta = db.select(Missao).where(Missao.ordem_dia == 1, Missao.id_missao != missao.id_missao)
    return any(m.pode_ser_dia_um() for m in db.session.scalars(consulta))


def salvar_missao(dados, missao=None):
    nova = missao is None
    if nova:
        classe = TIPOS_MISSAO.get(dados.get("tipo_missao"))
        if classe is None:
            raise RegraNegocioErro("Escolha um tipo de missão válido.")
        missao = classe()
    era_dia_um = not nova and missao.ordem_dia == 1

    try:
        missao.preencher(dados)  # cada tipo valida os seus campos
        # RN02: o dia 1 é sempre o mapeamento de gatilhos
        if missao.ordem_dia == 1 and not missao.pode_ser_dia_um():
            raise RegraNegocioErro(
                "A missão do dia 1 precisa ser reflexiva, porque é nela que a pessoa mapeia os gatilhos (RN02)."
            )
        if era_dia_um and missao.ordem_dia != 1 and not _existe_outra_missao_dia_um(missao):
            raise RegraNegocioErro(
                "Essa é a única missão do dia 1. Crie outra missão reflexiva para o dia 1 antes de mudar esta."
            )
    except RegraNegocioErro:
        db.session.rollback()
        raise

    if nova:
        db.session.add(missao)
    db.session.commit()
    return missao


def excluir_missao(missao):
    usos = db.session.scalar(
        db.select(db.func.count(ProgramaMissao.id_programa_missao)).where(ProgramaMissao.id_missao == missao.id_missao)
    )
    if usos:
        raise RegraNegocioErro(
            f"Essa missão já faz parte de {usos} programa(s) e não pode ser excluída, senão o histórico "
            "dessas pessoas quebra. Ainda dá para editar o texto dela."
        )
    if missao.ordem_dia == 1 and not _existe_outra_missao_dia_um(missao):
        raise RegraNegocioErro("Não dá para excluir a única missão do dia 1 (RN02).")
    db.session.delete(missao)
    db.session.commit()
