"""Funções pequenas de validação usadas pelos modelos e pelos serviços."""
import math
import re
from datetime import date

from app.excecoes import RegraNegocioErro

EMAIL_VALIDO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def texto_obrigatorio(valor, campo, maximo=None):
    texto = (valor or "").strip()
    if not texto:
        raise RegraNegocioErro(f"Preencha o campo {campo}.")
    if maximo and len(texto) > maximo:
        raise RegraNegocioErro(f"O campo {campo} aceita no máximo {maximo} caracteres.")
    return texto


def texto_opcional(valor, campo, maximo=None):
    texto = (valor or "").strip()
    if maximo and len(texto) > maximo:
        raise RegraNegocioErro(f"O campo {campo} aceita no máximo {maximo} caracteres.")
    return texto or None


def inteiro(valor, campo, minimo=None, maximo=None):
    try:
        numero = int(str(valor).strip())
    except (TypeError, ValueError):
        raise RegraNegocioErro(f"O campo {campo} precisa ser um número inteiro.") from None
    if minimo is not None and numero < minimo:
        raise RegraNegocioErro(f"O campo {campo} precisa ser no mínimo {minimo}.")
    if maximo is not None and numero > maximo:
        raise RegraNegocioErro(f"O campo {campo} pode ser no máximo {maximo}.")
    return numero


def decimal(valor, campo, minimo=None, maximo=None):
    texto = str(valor or "").strip().replace("R$", "").replace(" ", "")
    if "," in texto:
        # aceita o jeito brasileiro de escrever: 1.234,56
        texto = texto.replace(".", "").replace(",", ".")
    try:
        numero = float(texto)
    except ValueError:
        raise RegraNegocioErro(f"O campo {campo} precisa ser um valor numérico.") from None
    if not math.isfinite(numero):
        raise RegraNegocioErro(f"O campo {campo} precisa ser um valor numérico.")
    if minimo is not None and numero < minimo:
        raise RegraNegocioErro(f"O campo {campo} precisa ser no mínimo {minimo}.")
    if maximo is not None and numero > maximo:
        raise RegraNegocioErro(f"O campo {campo} pode ser no máximo {maximo}.")
    return round(numero, 2)


def data_iso(valor, campo):
    try:
        return date.fromisoformat(str(valor).strip())
    except ValueError:
        raise RegraNegocioErro(f"O campo {campo} precisa ser uma data válida.") from None


def email(valor):
    texto = (valor or "").strip().lower()
    if len(texto) > 120 or not EMAIL_VALIDO.match(texto):
        raise RegraNegocioErro("Informe um e-mail válido.")
    return texto


def escolha(valor, opcoes, campo):
    if valor not in opcoes:
        raise RegraNegocioErro(f"Escolha uma opção válida para {campo}.")
    return valor


def escolha_com_outro(dados, campo_lista, campo_outro, opcoes, nome_campo):
    """Para selects que têm a opção "Outro" com um campo de texto livre."""
    valor = (dados.get(campo_lista) or "").strip()
    if valor == "Outro":
        return texto_obrigatorio(dados.get(campo_outro), f"{nome_campo} (outro)", 80)
    return escolha(valor, opcoes, nome_campo)
