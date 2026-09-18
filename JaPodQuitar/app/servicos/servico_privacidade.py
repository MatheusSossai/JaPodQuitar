"""Direitos do titular dos dados (RF12, RNF04 - LGPD)."""

from app.repositorios.repositorio_usuario import RepositorioUsuario


class ServicoPrivacidade:
    def __init__(self, repositorio: RepositorioUsuario | None = None) -> None:
        self.repositorio = repositorio or RepositorioUsuario()

    def exportar_dados(self, id_usuario: int) -> dict:
        """TODO (Sprint 4): devolve perfil, programas, missoes e diario em JSON."""
        raise NotImplementedError

    def excluir_conta(self, id_usuario: int) -> None:
        """TODO (Sprint 4): unica forma de apagar registros do diario (RN05)."""
        raise NotImplementedError

    def anonimizar_para_indicadores(self, id_usuario: int) -> dict:
        """TODO (Sprint 4): dados agregados dos indicadores da secao 2.3."""
        raise NotImplementedError
