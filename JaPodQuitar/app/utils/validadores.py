"""Validacoes reutilizaveis de entrada."""


def email_valido(email: str) -> bool:
    """TODO (Sprint 1): validacao simples de formato."""
    raise NotImplementedError


def senha_forte(senha: str) -> bool:
    """TODO (Sprint 1): tamanho minimo e combinacao de caracteres."""
    raise NotImplementedError


def intensidade_valida(valor: int) -> bool:
    """Intensidade de sintoma: inteiro de 1 a 5 (RN09)."""
    return isinstance(valor, int) and 1 <= valor <= 5
