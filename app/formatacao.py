"""Transforma o texto das matérias em HTML simples.

O moderador escreve em texto puro, com algumas marcações fáceis:
- linha começando com "## " vira subtítulo;
- linhas começando com "- " viram lista;
- linha em branco separa os parágrafos.

Todo o texto passa pelo escape, então ninguém consegue colocar HTML ou script no conteúdo.
"""
from markupsafe import Markup, escape


def _fechar_paragrafo(html, linhas):
    if linhas:
        html.append(Markup("<p>{}</p>").format(Markup("<br>").join(escape(l) for l in linhas)))
        linhas.clear()


def _fechar_lista(html, itens):
    if itens:
        html.append(Markup("<ul>{}</ul>").format(Markup("").join(Markup("<li>{}</li>").format(i) for i in itens)))
        itens.clear()


def texto_para_html(texto):
    html = []
    for bloco in (texto or "").replace("\r\n", "\n").split("\n\n"):
        paragrafo, lista = [], []
        for linha in bloco.split("\n"):
            linha = linha.strip()
            if not linha:
                continue
            if linha.startswith("## "):
                _fechar_paragrafo(html, paragrafo)
                _fechar_lista(html, lista)
                html.append(Markup("<h2>{}</h2>").format(linha[3:]))
            elif linha.startswith("- "):
                _fechar_paragrafo(html, paragrafo)
                lista.append(linha[2:])
            else:
                _fechar_lista(html, lista)
                paragrafo.append(linha)
        _fechar_paragrafo(html, paragrafo)
        _fechar_lista(html, lista)
    return Markup("\n").join(html)


def texto_puro(texto):
    """Tira as marcações para usar em resumos e na contagem de palavras."""
    linhas = []
    for linha in (texto or "").split("\n"):
        linha = linha.strip()
        if linha.startswith("## "):
            continue
        if linha.startswith("- "):
            linha = linha[2:]
        linhas.append(linha)
    return " ".join(" ".join(linhas).split())
