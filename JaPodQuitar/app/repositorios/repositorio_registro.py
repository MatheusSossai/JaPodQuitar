"""Consultas de REGISTRO_DIARIO; reconstroi a pilha em memoria."""

from app.modelos import RegistroDiarioModelo
from app.repositorios.repositorio_base import RepositorioBase


class RepositorioRegistro(RepositorioBase):
    modelo = RegistroDiarioModelo

    def carregar_pilha(self, id_programa: int):
        """TODO (Sprint 3): le por posicao_pilha, com data_hora como desempate,
        e devolve um DiarioProgresso preenchido (secao 3.4)."""
        raise NotImplementedError

    def proxima_posicao(self, id_programa: int) -> int:
        """TODO (Sprint 3): topo atual + 1."""
        raise NotImplementedError

    def contar_recaidas_recentes(self, id_programa: int, dias: int = 7) -> int:
        """TODO (Sprint 4): insumo do alerta de tres recaidas em sete dias (RN07)."""
        raise NotImplementedError
