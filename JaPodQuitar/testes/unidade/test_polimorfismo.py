"""Polimorfismo das hierarquias Missao e RegistroDiario (secao 5.1)."""

from datetime import datetime

from app.dominio.registro_diario import (
    RegistroConquista,
    RegistroRecaida,
    RegistroSintoma,
)


def test_impacto_varia_por_subtipo_de_registro():
    agora = datetime.now()
    sintoma = RegistroSintoma(None, agora, sintoma="irritabilidade", intensidade=3)
    recaida = RegistroRecaida(None, agora, puffs=5, gatilho="ansiedade")
    conquista = RegistroConquista(None, agora, marco="primeira semana")

    assert (sintoma.impacto(), recaida.impacto(), conquista.impacto()) == (0, -1, 1)


# TODO (Sprint 2): testar executar() e orientacao() dos tres tipos de missao.
