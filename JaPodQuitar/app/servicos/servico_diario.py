"""Diario de progresso: opera a pilha de registros (RN04, RN05, RN09)."""

from app.repositorios.repositorio_registro import RepositorioRegistro


class ServicoDiario:
    def __init__(self, repositorio: RepositorioRegistro | None = None) -> None:
        self.repositorio = repositorio or RepositorioRegistro()

    def registrar_sintoma(self, id_programa: int, sintoma: str, intensidade: int):
        """TODO (Sprint 3): validar intensidade inteira entre 1 e 5 (RN09)."""
        raise NotImplementedError

    def registrar_recaida(self, id_programa: int, puffs: int, gatilho: str):
        """TODO (Sprint 3): empilhar o registro e acionar a verificacao do RN07."""
        raise NotImplementedError

    def registrar_conquista(self, id_programa: int, marco: str):
        """TODO (Sprint 3): empilhar o marco alcancado."""
        raise NotImplementedError

    def listar(self, id_programa: int, quantidade: int = 20) -> list:
        """TODO (Sprint 3): do mais recente para o mais antigo (RN04)."""
        raise NotImplementedError
