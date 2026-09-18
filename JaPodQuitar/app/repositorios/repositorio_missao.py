"""Consultas de MISSAO e PROGRAMA_MISSAO; reconstroi a fila em memoria."""

from app.modelos import MissaoModelo, ProgramaMissaoModelo
from app.repositorios.repositorio_base import RepositorioBase


class RepositorioMissao(RepositorioBase):
    modelo = MissaoModelo

    def carregar_fila(self, id_programa: int):
        """TODO (Sprint 2): le PROGRAMA_MISSAO ordenado por posicao_fila e
        devolve uma FilaMissoes preenchida (secao 3.4)."""
        raise NotImplementedError

    def persistir_posicoes(self, id_programa: int, fila) -> None:
        """TODO (Sprint 2): grava a ordem atual da fila em posicao_fila."""
        raise NotImplementedError

    def marcar_concluida(self, id_programa_missao: int) -> None:
        """TODO (Sprint 2): atualiza status e data_conclusao (RN03)."""
        raise NotImplementedError
