from datetime import date, timedelta

import pytest

from app.excecoes import RegraNegocioErro
from app.servicos import conta_servico, programa_servico


def test_rn01_so_um_programa_ativo(usuario, programa):
    with pytest.raises(RegraNegocioErro):
        programa_servico.criar_programa(usuario, 30)


def test_rn01_novo_programa_depois_de_encerrar(usuario, programa):
    programa_servico.encerrar_programa(programa, "interrompido")
    novo = programa_servico.criar_programa(usuario, 15)

    assert novo.status == "ativo"
    assert programa.status == "interrompido"
    assert len(usuario.programas) == 2


def test_rn02_primeira_missao_e_o_mapeamento_de_gatilhos(programa):
    atual = programa.missao_atual()
    assert atual.missao.ordem_dia == 1
    assert atual.missao.pode_ser_dia_um()
    assert atual.posicao_fila == 1


def test_rn02_fila_segue_a_ordem_dos_dias(programa):
    dias = [item.missao.ordem_dia for item in programa.montar_fila().listar()]
    assert dias == sorted(dias)
    assert dias[0] == 2


def test_rn03_so_uma_missao_em_andamento(programa):
    programa_servico.concluir_missao_atual(programa, "estudando e em festa")
    programa_servico.concluir_missao_atual(programa)

    em_andamento = [i for i in programa.itens_fila if i.status == "em_andamento"]
    assert len(em_andamento) == 1
    assert em_andamento[0].missao.ordem_dia == 3


def test_missao_reflexiva_precisa_de_resposta(programa):
    with pytest.raises(RegraNegocioErro):
        programa_servico.concluir_missao_atual(programa, "   ")
    assert programa.missao_atual().missao.ordem_dia == 1


def test_adiar_manda_a_missao_para_o_fim_da_fila(programa):
    programa_servico.concluir_missao_atual(programa, "ao acordar")
    adiada = programa.missao_atual()

    programa_servico.adiar_missao_atual(programa)

    assert programa.montar_fila().listar()[-1] is adiada
    assert programa.missao_atual().missao.ordem_dia == 3


def test_concluido_so_depois_da_meta(programa):
    with pytest.raises(RegraNegocioErro):
        programa_servico.encerrar_programa(programa, "concluido")

    depois_da_meta = programa.data_inicio + timedelta(days=30)
    programa_servico.encerrar_programa(programa, "concluido", hoje=depois_da_meta)
    assert programa.status == "concluido"
    assert programa.data_fim == depois_da_meta


def test_programa_precisa_do_perfil_de_consumo(ctx):
    sem_perfil = conta_servico.cadastrar_usuario("Sem perfil", "sem@email.com", "senha1234", "senha1234", True)
    with pytest.raises(RegraNegocioErro):
        programa_servico.criar_programa(sem_perfil, 30)


@pytest.mark.parametrize("meta", ["3", "500", "abc"])
def test_meta_de_dias_invalida(usuario, meta):
    with pytest.raises(RegraNegocioErro):
        programa_servico.criar_programa(usuario, meta)


def test_data_de_inicio_no_futuro(usuario):
    amanha = date.today() + timedelta(days=1)
    with pytest.raises(RegraNegocioErro):
        programa_servico.criar_programa(usuario, 30, amanha.isoformat())
