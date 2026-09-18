"""Contadores, economia e resumo de padroes (RF07, RF08, RN06, RN08)."""

from app.repositorios.repositorio_registro import RepositorioRegistro


class ServicoMetricas:
    def __init__(self, repositorio: RepositorioRegistro | None = None) -> None:
        self.repositorio = repositorio or RepositorioRegistro()

    def dias_consecutivos_sem_nicotina(self, id_programa: int) -> int:
        """TODO (Sprint 4): zerado por uma recaida, mas o total acumulado e o
        recorde anterior sao preservados (RN06)."""
        raise NotImplementedError

    def economia_estimada(self, id_programa: int) -> float:
        """TODO (Sprint 4): (dias sem nicotina / 7) x custo semanal (RN08)."""
        raise NotImplementedError

    def resumo_de_padroes(self, id_programa: int) -> dict:
        """TODO (Sprint 4): gatilhos mais frequentes, horarios e sintomas mais
        relatados (RF08)."""
        raise NotImplementedError

    def deve_destacar_canais_de_apoio(self, id_programa: int) -> bool:
        """TODO (Sprint 4): tres recaidas em sete dias (RN07 -> RF10)."""
        raise NotImplementedError
