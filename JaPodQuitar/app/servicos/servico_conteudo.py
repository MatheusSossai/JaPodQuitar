"""Publicacao e leitura do conteudo informativo (RF02, RF11, RN10, RNF05)."""

from app.repositorios.repositorio_conteudo import RepositorioConteudo


class ServicoConteudo:
    def __init__(self, repositorio: RepositorioConteudo | None = None) -> None:
        self.repositorio = repositorio or RepositorioConteudo()

    def publicar(self, id_moderador: int, dados: dict):
        """TODO (Sprint 2): recusar publicacao sem o campo fonte (RN10/RNF05)."""
        raise NotImplementedError

    def listar_abertos(self, categoria: str | None = None) -> list:
        """TODO (Sprint 2): leitura livre, sem cadastro (RF02)."""
        raise NotImplementedError
