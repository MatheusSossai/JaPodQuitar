"""Cobertura das regras RN01 a RN11 (RNF06).

Cada regra ganha um teste quando a funcionalidade correspondente entra na
sprint. Os testes abaixo estao marcados para nao quebrar a integracao continua
enquanto a implementacao nao existe.
"""

import pytest

from app.utils.validadores import intensidade_valida


def test_rn09_intensidade_do_sintoma_entre_1_e_5():
    assert intensidade_valida(1)
    assert intensidade_valida(5)
    assert not intensidade_valida(0)
    assert not intensidade_valida(6)


@pytest.mark.skip(reason="Sprint 1")
def test_rn01_apenas_um_programa_ativo_por_usuario():
    ...


@pytest.mark.skip(reason="Sprint 2")
def test_rn02_missao_do_dia_1_e_o_mapeamento_de_gatilhos():
    ...


@pytest.mark.skip(reason="Sprint 2")
def test_rn03_proxima_missao_so_apos_conclusao_ou_adiamento():
    ...


@pytest.mark.skip(reason="Sprint 3")
def test_rn05_registro_do_diario_nao_pode_ser_apagado_individualmente():
    ...


@pytest.mark.skip(reason="Sprint 4")
def test_rn06_recaida_zera_o_contador_mas_preserva_o_recorde():
    ...


@pytest.mark.skip(reason="Sprint 4")
def test_rn07_tres_recaidas_em_sete_dias_destacam_canais_de_apoio():
    ...


@pytest.mark.skip(reason="Sprint 4")
def test_rn08_economia_e_dias_dividido_por_sete_vezes_custo_semanal():
    ...


@pytest.mark.skip(reason="Sprint 2")
def test_rn10_conteudo_sem_fonte_nao_e_publicado():
    ...
