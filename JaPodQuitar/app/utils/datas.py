"""Conversao de datas para o formato ISO-8601, usado nas colunas TEXT do SQLite."""

from datetime import date, datetime

FORMATO_DATA = "%Y-%m-%d"
FORMATO_DATA_HORA = "%Y-%m-%dT%H:%M:%S"


def para_texto(valor: date | datetime) -> str:
    """TODO (Sprint 1): serializar date/datetime no formato ISO."""
    raise NotImplementedError


def para_data(texto: str) -> date:
    """TODO (Sprint 1): leitura inversa de para_texto."""
    raise NotImplementedError


def diferenca_em_dias(inicio: date, fim: date) -> int:
    return (fim - inicio).days
