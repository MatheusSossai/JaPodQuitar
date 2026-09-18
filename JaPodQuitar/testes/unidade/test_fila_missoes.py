"""Fila de missoes: ordem FIFO e regra RN02."""

import pytest

from app.dominio.estruturas.fila_missoes import FilaMissoes


def test_fila_nova_esta_vazia():
    assert FilaMissoes().esta_vazia()


def test_primeiro_a_entrar_e_o_primeiro_a_sair():
    fila = FilaMissoes()
    fila.enfileirar("gatilhos")
    fila.enfileirar("substituicao")
    assert fila.desenfileirar() == "gatilhos"


def test_consultar_proxima_nao_remove():
    fila = FilaMissoes(["gatilhos"])
    fila.consultar_proxima()
    assert fila.tamanho() == 1


def test_desenfileirar_fila_vazia_levanta_erro():
    with pytest.raises(IndexError):
        FilaMissoes().desenfileirar()
