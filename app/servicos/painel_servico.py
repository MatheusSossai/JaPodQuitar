"""Junta os números que aparecem no painel do usuário (RF07)."""
from datetime import datetime

from app.servicos import diario_servico


def resumo_progresso(usuario, agora=None):
    agora = agora or datetime.now()
    hoje = agora.date()
    programa = usuario.programa_ativo()
    if programa is None:
        return {"programa": None, "qtd_programas": len(usuario.programas)}

    dias_programa = programa.dias_de_programa(hoje)
    recaidas = diario_servico.contar_recaidas_recentes(usuario, agora)

    return {
        "programa": programa,
        "dias_sem_nicotina": usuario.dias_sem_nicotina(hoje),
        "recorde": programa.recorde_dias(hoje),
        "dias_programa": dias_programa,
        "economia": usuario.calcular_economia(hoje),
        "percentual": programa.percentual_conclusao(hoje),
        "meta_atingida": dias_programa >= programa.meta_dias,
        "missao_atual": programa.missao_atual(),
        "missoes_concluidas": len(programa.missoes_concluidas()),
        "total_missoes": len(programa.itens_fila),
        "pontos": programa.pontos(),
        "ultimos_registros": programa.montar_diario().listar_recentes(5),
        "recaidas_7_dias": recaidas,
        "alerta_apoio": recaidas >= diario_servico.LIMITE_RECAIDAS,
    }
