"""Indicadores da seção 2.3, sempre com números agregados e sem identificar ninguém."""
from collections import Counter
from datetime import date

from app.extensoes import db
from app.modelos import ContadorAcesso, ProgramaCessacao, RegistroRecaida, Usuario
from app.opcoes import CANAIS_APOIO

CHAVE_ACESSO_ANONIMO = "acesso_informativo_anonimo"


def chave_clique(canal):
    return f"clique_apoio_{canal}"


def incrementar(chave):
    contador = db.session.get(ContadorAcesso, chave)
    if contador is None:
        contador = ContadorAcesso(chave=chave, total=0)
        db.session.add(contador)
    contador.total += 1
    db.session.commit()


def valor(chave):
    contador = db.session.get(ContadorAcesso, chave)
    return contador.total if contador else 0


def _percentual(parte, total):
    return round(parte / total * 100, 1) if total else 0.0


def _continuou_ate(programa, dias, hoje):
    """None se o programa ainda não chegou nesse dia, senão True/False."""
    if (hoje - programa.data_inicio).days < dias:
        return None
    if programa.data_fim is None:
        return True
    return (programa.data_fim - programa.data_inicio).days >= dias


def _retencao(programas, dias, hoje):
    resultados = [r for r in (_continuou_ate(p, dias, hoje) for p in programas) if r is not None]
    ativos = sum(1 for r in resultados if r)
    return {"elegiveis": len(resultados), "ativos": ativos, "percentual": _percentual(ativos, len(resultados))}


def calcular_indicadores(hoje=None):
    hoje = hoje or date.today()

    total_usuarios = db.session.scalar(db.select(db.func.count()).select_from(Usuario))
    programas = db.session.scalars(db.select(ProgramaCessacao)).all()
    concluiram_dia_um = sum(1 for p in programas if p.concluiu_missao_dia_um())

    gatilhos = Counter(r.gatilho for r in db.session.scalars(db.select(RegistroRecaida))).most_common(5)
    cliques = [(dados["nome"], valor(chave_clique(chave))) for chave, dados in CANAIS_APOIO.items()]

    return {
        "total_usuarios": total_usuarios,
        "total_programas": len(programas),
        "programas_ativos": sum(1 for p in programas if p.status == ProgramaCessacao.ATIVO),
        "dia_um": {"quantidade": concluiram_dia_um, "percentual": _percentual(concluiram_dia_um, len(programas))},
        "dia_7": _retencao(programas, 7, hoje),
        "dia_30": _retencao(programas, 30, hoje),
        "acessos_anonimos": valor(CHAVE_ACESSO_ANONIMO),
        "cliques_apoio": cliques,
        "total_cliques": sum(qtd for _, qtd in cliques),
        "gatilhos": gatilhos,
    }
