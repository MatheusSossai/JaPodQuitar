from datetime import date, datetime, time, timedelta

import pytest

from app.excecoes import RegraNegocioErro
from app.servicos import diario_servico, programa_servico


def registrar_recaida(usuario, agora=None, gatilho="Tédio"):
    return diario_servico.registrar_ocorrencia(
        usuario, "recaida", {"quantidade_puffs": "10", "gatilho": gatilho}, agora=agora
    )


def test_rn04_registro_mais_recente_no_topo(usuario, programa):
    for marco in ["primeiro", "segundo", "terceiro"]:
        diario_servico.registrar_ocorrencia(usuario, "conquista", {"marco": marco})

    recentes = programa.montar_diario().listar_recentes()
    assert [r.marco for r in recentes] == ["terceiro", "segundo", "primeiro"]
    assert [r.posicao_pilha for r in recentes] == [3, 2, 1]


def test_rn05_complemento_mantem_o_texto_original(usuario, programa):
    registro = diario_servico.registrar_ocorrencia(
        usuario, "sintoma", {"sintoma": "Ansiedade", "intensidade": "4", "observacao": "texto original"}
    )
    diario_servico.complementar_registro(usuario, registro.id_registro, "melhorou de noite")

    assert registro.observacao.startswith("texto original")
    assert "melhorou de noite" in registro.observacao


def test_rn05_nao_existe_rota_para_apagar_registro(app):
    rotas = [str(regra) for regra in app.url_map.iter_rules()]
    assert not any(r.startswith("/diario") and "excluir" in r for r in rotas)


def test_rn06_recaida_zera_contador_mas_guarda_recorde(usuario):
    hoje = date.today()
    inicio = hoje - timedelta(days=10)
    programa = programa_servico.criar_programa(usuario, 30, inicio.isoformat(), hoje=hoje)

    registrar_recaida(usuario, agora=datetime.combine(hoje - timedelta(days=3), time(22, 0)))

    assert usuario.dias_sem_nicotina(hoje) == 3
    assert programa.recorde_dias(hoje) == 7
    assert programa.dias_de_programa(hoje) == 10


def test_rn07_tres_recaidas_em_sete_dias_ativam_alerta(usuario, programa):
    agora = datetime.now()
    registrar_recaida(usuario, agora - timedelta(hours=5))
    registrar_recaida(usuario, agora - timedelta(hours=3))
    assert not diario_servico.precisa_alerta_apoio(usuario, agora)

    registrar_recaida(usuario, agora - timedelta(hours=1))
    assert diario_servico.precisa_alerta_apoio(usuario, agora)


def test_rn07_recaidas_espalhadas_nao_ativam_alerta(usuario):
    hoje = date.today()
    programa_servico.criar_programa(usuario, 30, (hoje - timedelta(days=20)).isoformat(), hoje=hoje)
    agora = datetime.now()
    for dias_atras in (18, 10, 1):
        registrar_recaida(usuario, agora - timedelta(days=dias_atras))

    assert not diario_servico.precisa_alerta_apoio(usuario, agora)


def test_rf09_recaida_reposiciona_missao_sem_apagar_progresso(usuario, programa):
    programa_servico.concluir_missao_atual(programa, "estudando")
    estava_em_andamento = programa.missao_atual()

    registrar_recaida(usuario, gatilho="Ansiedade ou estresse")

    assert len(programa.missoes_concluidas()) == 1
    assert programa.montar_fila().listar()[-1] is estava_em_andamento
    assert programa.missao_atual() is not estava_em_andamento


def test_rn09_intensidade_invalida_nao_salva(usuario, programa):
    with pytest.raises(RegraNegocioErro):
        diario_servico.registrar_ocorrencia(usuario, "sintoma", {"sintoma": "Tosse", "intensidade": "7"})
    assert programa.montar_diario().esta_vazio()


def test_campo_outro_no_gatilho(usuario, programa):
    registro = diario_servico.registrar_ocorrencia(
        usuario, "recaida", {"gatilho": "Outro", "gatilho_outro": "Discussão em casa"}
    )
    assert registro.gatilho == "Discussão em casa"
    assert registro.quantidade_puffs is None


def test_rf08_resumo_de_padroes(usuario, programa):
    registrar_recaida(usuario, gatilho="Tédio")
    registrar_recaida(usuario, gatilho="Tédio")
    registrar_recaida(usuario, gatilho="Ansiedade ou estresse")
    diario_servico.registrar_ocorrencia(usuario, "sintoma", {"sintoma": "Ansiedade", "intensidade": "4"})
    diario_servico.registrar_ocorrencia(usuario, "sintoma", {"sintoma": "Ansiedade", "intensidade": "2"})

    resumo = diario_servico.resumo_padroes(usuario)

    assert resumo["total_registros"] == 5
    assert resumo["gatilhos"][0] == {"nome": "Tédio", "quantidade": 2, "percentual": 67}
    assert resumo["sintomas"][0] == {"nome": "Ansiedade", "quantidade": 2, "media": 3.0}
    assert sum(p["quantidade"] for p in resumo["periodos"]) == 3
