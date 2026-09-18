"""Programa de cessacao: agrega a fila de missoes e a pilha do diario.

Composicao 1:1 com FilaMissoes e DiarioProgresso (secao 5.1). Um usuario tem
no maximo um programa com status 'ativo' por vez (RN01).
"""

from datetime import date

from app.dominio.estruturas.diario_progresso import DiarioProgresso
from app.dominio.estruturas.fila_missoes import FilaMissoes

STATUS_ATIVO = "ativo"
STATUS_CONCLUIDO = "concluido"
STATUS_INTERROMPIDO = "interrompido"


class ProgramaCessacao:
    def __init__(
        self,
        id: int | None,
        data_inicio: date,
        meta_dias: int,
        status: str = STATUS_ATIVO,
    ) -> None:
        self.id = id
        self.data_inicio = data_inicio
        self.meta_dias = meta_dias
        self.status = status
        self.fila = FilaMissoes()
        self.diario = DiarioProgresso()

    def proxima_missao(self):
        """Consulta a missao do topo da fila sem remove-la (RN03)."""
        return self.fila.consultar_proxima()

    def concluir_missao(self) -> None:
        """Desenfileira a missao atual e libera a seguinte (RN03).

        TODO (Sprint 2): registrar data de conclusao em PROGRAMA_MISSAO.
        """
        raise NotImplementedError

    def registrar(self, registro) -> None:
        """Empilha uma ocorrencia no diario (RN04)."""
        self.diario.empilhar(registro)

    def percentual_conclusao(self) -> float:
        """Proporcao de missoes concluidas em relacao ao total do programa.

        TODO (Sprint 4): calcular a partir do total persistido, nao da fila.
        """
        raise NotImplementedError
