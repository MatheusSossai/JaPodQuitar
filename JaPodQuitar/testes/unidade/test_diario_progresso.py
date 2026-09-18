"""Pilha do diario: ordem LIFO e regra RN04."""

import pytest

from app.dominio.estruturas.diario_progresso import DiarioProgresso


def test_diario_novo_esta_vazio():
    assert DiarioProgresso().esta_vazio()


def test_registro_mais_recente_fica_no_topo():
    diario = DiarioProgresso()
    diario.empilhar("sintoma")
    diario.empilhar("conquista")
    assert diario.consultar_topo() == "conquista"


def test_listar_recentes_vem_do_mais_novo_para_o_mais_antigo():
    diario = DiarioProgresso(["a", "b", "c"])
    assert diario.listar_recentes(2) == ["c", "b"]


def test_desempilhar_diario_vazio_levanta_erro():
    with pytest.raises(IndexError):
        DiarioProgresso().desempilhar()
