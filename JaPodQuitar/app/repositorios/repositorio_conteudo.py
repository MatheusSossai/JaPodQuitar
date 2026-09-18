"""Consultas de CONTEUDO_INFORMATIVO (RF02, RF11)."""

from app.modelos import ConteudoInformativoModelo
from app.repositorios.repositorio_base import RepositorioBase


class RepositorioConteudo(RepositorioBase):
    modelo = ConteudoInformativoModelo

    def listar_publicados(self, categoria: str | None = None) -> list:
        """TODO (Sprint 2): listagem aberta, sem exigencia de cadastro (RF02)."""
        raise NotImplementedError
