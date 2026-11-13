from collections import deque


class FilaMissoes:
    """Fila (FIFO) com as missões de um programa.

    Garante a RN02: a primeira missão que entra é a primeira que sai.
    O deque fica escondido dentro da classe, quem usa só enxerga os métodos abaixo.
    """

    def __init__(self):
        self._itens = deque()

    def enfileirar(self, item):
        self._itens.append(item)

    def desenfileirar(self):
        if self.esta_vazia():
            raise IndexError("A fila de missões está vazia.")
        return self._itens.popleft()

    def consultar_proxima(self):
        if self.esta_vazia():
            return None
        return self._itens[0]

    def esta_vazia(self):
        return len(self._itens) == 0

    def tamanho(self):
        return len(self._itens)

    def listar(self):
        # devolve uma cópia para ninguém mexer na fila por fora
        return list(self._itens)

    def __len__(self):
        return self.tamanho()
