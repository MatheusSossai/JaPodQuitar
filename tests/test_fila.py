import pytest

from app.estruturas import FilaMissoes


def test_fila_respeita_ordem_de_entrada():
    fila = FilaMissoes()
    for item in ["dia 1", "dia 2", "dia 3"]:
        fila.enfileirar(item)

    assert fila.desenfileirar() == "dia 1"
    assert fila.desenfileirar() == "dia 2"
    assert len(fila) == 1


def test_consultar_proxima_nao_tira_da_fila():
    fila = FilaMissoes()
    fila.enfileirar("a")
    fila.enfileirar("b")

    assert fila.consultar_proxima() == "a"
    assert fila.tamanho() == 2


def test_fila_vazia():
    fila = FilaMissoes()
    assert fila.esta_vazia()
    assert fila.consultar_proxima() is None
    with pytest.raises(IndexError):
        fila.desenfileirar()


def test_listar_da_fila_devolve_copia():
    fila = FilaMissoes()
    fila.enfileirar("a")
    fila.enfileirar("b")

    copia = fila.listar()
    copia.clear()

    assert fila.tamanho() == 2
