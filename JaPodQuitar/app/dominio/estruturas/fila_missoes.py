"""FilaMissoes - fila FIFO sobre collections.deque (RN02, RN03).

A ordem de entrega das missoes e a ordem de entrada. A missao do dia 1
(mapeamento de gatilhos) e sempre a primeira a sair. Todas as operacoes
custam O(1).
"""

from collections import deque


class FilaMissoes:
    def __init__(self, missoes=None) -> None:
        self._itens: deque = deque(missoes or [])

    def enfileirar(self, missao) -> None:
        """Insere uma missao no fim da fila. O(1)."""
        self._itens.append(missao)

    def desenfileirar(self):
        """Remove e devolve a missao do inicio da fila. O(1)."""
        if self.esta_vazia():
            raise IndexError("A fila de missoes esta vazia.")
        return self._itens.popleft()

    def consultar_proxima(self):
        """Devolve a proxima missao sem remove-la. O(1)."""
        if self.esta_vazia():
            return None
        return self._itens[0]

    def esta_vazia(self) -> bool:
        return len(self._itens) == 0

    def tamanho(self) -> int:
        return len(self._itens)

    def listar(self) -> list:
        """Copia da fila na ordem de saida, para exibicao."""
        return list(self._itens)

    def __len__(self) -> int:
        return len(self._itens)
