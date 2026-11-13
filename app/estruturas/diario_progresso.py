class DiarioProgresso:
    """Pilha (LIFO) com os registros do diário.

    Garante a RN04: o registro mais recente fica sempre no topo.
    A lista interna é operada só pelo final (append/pop), por isso tudo é O(1).
    """

    def __init__(self):
        self._registros = []

    def empilhar(self, registro):
        self._registros.append(registro)

    def desempilhar(self):
        if self.esta_vazio():
            raise IndexError("O diário está vazio.")
        return self._registros.pop()

    def consultar_topo(self):
        if self.esta_vazio():
            return None
        return self._registros[-1]

    def listar_recentes(self, n=None):
        """Lista do topo para a base (do mais novo para o mais antigo)."""
        do_topo_para_baixo = self._registros[::-1]
        if n is None:
            return do_topo_para_baixo
        return do_topo_para_baixo[:n]

    def esta_vazio(self):
        return len(self._registros) == 0

    def tamanho(self):
        return len(self._registros)

    def __len__(self):
        return self.tamanho()
