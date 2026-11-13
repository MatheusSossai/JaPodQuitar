import pytest

from app.estruturas import DiarioProgresso


def test_pilha_deixa_o_mais_recente_no_topo():
    diario = DiarioProgresso()
    for registro in ["segunda", "terça", "quarta"]:
        diario.empilhar(registro)

    assert diario.consultar_topo() == "quarta"
    assert diario.desempilhar() == "quarta"
    assert diario.consultar_topo() == "terça"


def test_listar_recentes_vai_do_topo_para_a_base():
    diario = DiarioProgresso()
    for registro in ["a", "b", "c"]:
        diario.empilhar(registro)

    assert diario.listar_recentes() == ["c", "b", "a"]
    assert diario.listar_recentes(2) == ["c", "b"]


def test_pilha_vazia():
    diario = DiarioProgresso()
    assert diario.esta_vazio()
    assert diario.consultar_topo() is None
    with pytest.raises(IndexError):
        diario.desempilhar()
