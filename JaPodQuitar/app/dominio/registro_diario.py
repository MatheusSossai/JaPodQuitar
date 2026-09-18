"""Hierarquia RegistroDiario -> Sintoma / Recaida / Conquista.

impacto() devolve o efeito do registro sobre o contador de dias sem nicotina:
negativo na recaida, neutro no sintoma e positivo na conquista (RN06).
"""

from abc import ABC, abstractmethod
from datetime import datetime


class RegistroDiario(ABC):
    """Ocorrencia empilhada no diario de progresso (RN04, RN05)."""

    def __init__(self, id: int | None, data_hora: datetime, observacao: str = "") -> None:
        self.id = id
        self.data_hora = data_hora
        self.observacao = observacao

    @abstractmethod
    def resumo(self) -> str:
        """Linha exibida na listagem do diario."""

    @abstractmethod
    def impacto(self) -> int:
        """Efeito sobre o contador de dias consecutivos sem nicotina."""


class RegistroSintoma(RegistroDiario):
    """Sintoma de abstinencia, com intensidade inteira de 1 a 5 (RN09)."""

    def __init__(self, id, data_hora, observacao="", sintoma: str = "", intensidade: int = 1) -> None:
        super().__init__(id, data_hora, observacao)
        self.sintoma = sintoma
        self.intensidade = intensidade

    def resumo(self) -> str:
        raise NotImplementedError  # TODO (Sprint 3)

    def impacto(self) -> int:
        return 0


class RegistroRecaida(RegistroDiario):
    """Recaida: evento previsto no processo, nunca tratado como fracasso (RF09)."""

    def __init__(self, id, data_hora, observacao="", puffs: int = 0, gatilho: str = "") -> None:
        super().__init__(id, data_hora, observacao)
        self.puffs = puffs
        self.gatilho = gatilho

    def resumo(self) -> str:
        raise NotImplementedError  # TODO (Sprint 3)

    def impacto(self) -> int:
        return -1


class RegistroConquista(RegistroDiario):
    """Marco alcancado pelo usuario (primeira semana, primeiro mes, etc.)."""

    def __init__(self, id, data_hora, observacao="", marco: str = "") -> None:
        super().__init__(id, data_hora, observacao)
        self.marco = marco

    def resumo(self) -> str:
        raise NotImplementedError  # TODO (Sprint 3)

    def impacto(self) -> int:
        return 1
