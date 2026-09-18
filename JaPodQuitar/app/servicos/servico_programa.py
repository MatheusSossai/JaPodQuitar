"""Ciclo de vida do programa de cessacao (RN01)."""

from app.repositorios.repositorio_programa import RepositorioPrograma


class ServicoPrograma:
    def __init__(self, repositorio: RepositorioPrograma | None = None) -> None:
        self.repositorio = repositorio or RepositorioPrograma()

    def iniciar_programa(self, id_usuario: int, meta_dias: int):
        """TODO (Sprint 1): impedir dois programas ativos simultaneos (RN01) e
        montar a fila inicial com a missao de gatilhos no dia 1 (RN02)."""
        raise NotImplementedError

    def interromper(self, id_programa: int) -> None:
        """TODO (Sprint 1): move o programa para o historico, sem apagar dados."""
        raise NotImplementedError

    def registrar_perfil_consumo(self, id_usuario: int, dados: dict) -> None:
        """TODO (Sprint 1): frequencia, tempo de uso, gasto semanal e nivel de
        dependencia autodeclarado (RF03)."""
        raise NotImplementedError
