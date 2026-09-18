"""Consultas de PROGRAMA_CESSACAO (RN01)."""

from app.modelos import ProgramaCessacaoModelo
from app.repositorios.repositorio_base import RepositorioBase


class RepositorioPrograma(RepositorioBase):
    modelo = ProgramaCessacaoModelo

    def buscar_programa_ativo(self, id_usuario: int):
        """TODO (Sprint 1): ha no maximo um programa ativo por usuario (RN01)."""
        raise NotImplementedError

    def listar_historico(self, id_usuario: int) -> list:
        """TODO (Sprint 1): programas concluidos ou interrompidos."""
        raise NotImplementedError
