"""DiarioProgresso - pilha LIFO sobre list (RN04, RN05).

O registro mais recente fica sempre no topo, que e a forma como o usuario le
o proprio historico. Todas as operacoes custam O(1).
"""


class DiarioProgresso:
    def __init__(self, registros=None) -> None:
        self._registros: list = list(registros or [])

    def empilhar(self, registro) -> None:
        """Insere uma ocorrencia no topo da pilha. O(1)."""
        self._registros.append(registro)

    def desempilhar(self):
        """Remove e devolve o registro do topo. O(1).

        Uso restrito: o usuario nao apaga registros individualmente (RN05).
        Este metodo existe para desfazer uma operacao dentro da mesma sessao.
        """
        if self.esta_vazio():
            raise IndexError("O diario de progresso esta vazio.")
        return self._registros.pop()

    def consultar_topo(self):
        """Devolve o registro mais recente sem remove-lo. O(1)."""
        if self.esta_vazio():
            return None
        return self._registros[-1]

    def listar_recentes(self, n: int = 10) -> list:
        """Ultimos n registros, do mais recente para o mais antigo."""
        return list(reversed(self._registros[-n:]))

    def esta_vazio(self) -> bool:
        return len(self._registros) == 0

    def tamanho(self) -> int:
        return len(self._registros)

    def __len__(self) -> int:
        return len(self._registros)
