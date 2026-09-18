"""Hierarquia Missao -> Reflexiva / Pratica / Educativa.

Os metodos executar() e orientacao() sao abstratos: a camada de servico
percorre a fila tratando todos os elementos pelo tipo Missao, sem verificar
o tipo concreto (polimorfismo, secao 5.1).
"""

from abc import ABC, abstractmethod


class Missao(ABC):
    """Tarefa curta entregue ao usuario, uma por vez (RN02, RN03)."""

    def __init__(self, id: int | None, titulo: str, ordem_dia: int) -> None:
        self.id = id
        self.titulo = titulo
        self.ordem_dia = ordem_dia

    @abstractmethod
    def executar(self) -> str:
        """Conteudo apresentado quando a missao e aberta."""

    @abstractmethod
    def orientacao(self) -> str:
        """Texto de apoio, em linguagem de acolhimento (RNF02)."""

    def pontuacao(self) -> int:
        """Peso da missao no percentual de conclusao do programa."""
        return 10


class MissaoReflexiva(Missao):
    """Devolve uma pergunta de mapeamento de gatilho (missao do dia 1, RN02)."""

    def __init__(self, id, titulo, ordem_dia, pergunta: str = "") -> None:
        super().__init__(id, titulo, ordem_dia)
        self.pergunta = pergunta

    def executar(self) -> str:
        raise NotImplementedError  # TODO (Sprint 2)

    def orientacao(self) -> str:
        raise NotImplementedError  # TODO (Sprint 2)


class MissaoPratica(Missao):
    """Devolve uma acao substituta cronometrada."""

    def __init__(self, id, titulo, ordem_dia, acao_substituta: str = "", duracao_min: int = 0) -> None:
        super().__init__(id, titulo, ordem_dia)
        self.acao_substituta = acao_substituta
        self.duracao_min = duracao_min

    def executar(self) -> str:
        raise NotImplementedError  # TODO (Sprint 2)

    def orientacao(self) -> str:
        raise NotImplementedError  # TODO (Sprint 2)


class MissaoEducativa(Missao):
    """Devolve um ConteudoInformativo publicado por um moderador."""

    def __init__(self, id, titulo, ordem_dia, conteudo=None) -> None:
        super().__init__(id, titulo, ordem_dia)
        self.conteudo = conteudo

    def executar(self) -> str:
        raise NotImplementedError  # TODO (Sprint 2)

    def orientacao(self) -> str:
        raise NotImplementedError  # TODO (Sprint 2)
