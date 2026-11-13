"""Testes dos pilares de POO: classes abstratas, herança e polimorfismo."""
from datetime import date

import pytest

from app.excecoes import RegraNegocioErro
from app.extensoes import db
from app.modelos import (
    Missao,
    Moderador,
    Pessoa,
    RegistroConquista,
    RegistroDiario,
    RegistroRecaida,
    RegistroSintoma,
    Usuario,
)


def test_classes_abstratas_nao_podem_ser_instanciadas(ctx):
    with pytest.raises(TypeError):
        Pessoa(nome="x", email="x@x.com")
    with pytest.raises(TypeError):
        Missao(titulo="x")
    with pytest.raises(TypeError):
        RegistroDiario()


def test_heranca_de_pessoa(ctx):
    assert issubclass(Usuario, Pessoa)
    assert issubclass(Moderador, Pessoa)


def test_polimorfismo_no_painel(ctx):
    pessoas = [Usuario(nome="a", email="a@a.com"), Moderador(nome="b", email="b@b.com")]
    assert [p.exibir_painel() for p in pessoas] == ["painel.usuario", "painel.moderador"]
    assert [p.perfil_acesso() for p in pessoas] == ["usuario", "moderador"]


def test_polimorfismo_nas_missoes(ctx):
    missoes = db.session.scalars(db.select(Missao).order_by(Missao.ordem_dia)).all()

    assert {m.rotulo() for m in missoes} == {"Reflexiva", "Prática", "Educativa"}
    for missao in missoes:
        assert missao.executar()
        assert missao.orientacao()

    primeira = missoes[0]
    assert primeira.executar() == primeira.pergunta_gatilho
    assert primeira.exige_resposta()


def test_impacto_de_cada_registro(ctx):
    registros = [
        RegistroSintoma(sintoma="Ansiedade", intensidade=3),
        RegistroRecaida(quantidade_puffs=10, gatilho="Tédio"),
        RegistroConquista(marco="Uma semana"),
    ]
    assert [r.impacto() for r in registros] == [0, -1, 1]
    assert [r.rotulo() for r in registros] == ["Sintoma", "Recaída", "Conquista"]


@pytest.mark.parametrize("valor", [0, 6, -1])
def test_rn09_intensidade_fora_da_escala(ctx, valor):
    with pytest.raises(RegraNegocioErro):
        RegistroSintoma(sintoma="Tosse", intensidade=valor)


def test_rnf03_senha_guardada_como_hash(usuario):
    assert usuario.senha_hash != "senha1234"
    assert usuario.autenticar("senha1234")
    assert not usuario.autenticar("senha errada")


def test_rn08_calculo_da_economia(usuario):
    usuario.data_inicio_abstinencia = date(2026, 1, 1)
    # 14 dias / 7 x R$ 70 = R$ 140
    assert usuario.calcular_economia(hoje=date(2026, 1, 15)) == 140.0


def test_rn10_moderador_nao_publica_sem_fonte(ctx):
    from app.modelos import ConteudoInformativo

    moderador = db.session.scalars(db.select(Moderador)).first()
    with pytest.raises(RegraNegocioErro):
        moderador.publicar(ConteudoInformativo(titulo="x", corpo="y", categoria="Pulmões", fonte="  "))
