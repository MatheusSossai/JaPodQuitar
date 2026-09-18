"""Motor de missoes: opera a fila do programa (RN02, RN03).

Percorre a fila tratando todos os elementos pelo tipo abstrato Missao. Nenhuma
verificacao de tipo concreto deve aparecer neste modulo.
"""

from app.repositorios.repositorio_missao import RepositorioMissao


class ServicoMissoes:
    def __init__(self, repositorio: RepositorioMissao | None = None) -> None:
        self.repositorio = repositorio or RepositorioMissao()

    def missao_atual(self, id_programa: int):
        """TODO (Sprint 2): consultar o inicio da fila sem desenfileirar (RF05)."""
        raise NotImplementedError

    def concluir_missao_atual(self, id_programa: int):
        """TODO (Sprint 2): so libera a proxima apos conclusao ou adiamento (RN03)."""
        raise NotImplementedError

    def adiar_missao_atual(self, id_programa: int):
        """TODO (Sprint 2): reposiciona a missao no fim da fila."""
        raise NotImplementedError

    def reposicionar_apos_recaida(self, id_programa: int):
        """TODO (Sprint 3): recaida reposiciona a missao correspondente sem zerar
        o progresso registrado (RF09)."""
        raise NotImplementedError
