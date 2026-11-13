"""Módulo informativo aberto, sem precisar de cadastro (RF02)."""
from flask import Blueprint, render_template, request
from flask_login import current_user

from app.extensoes import db
from app.modelos import ConteudoInformativo
from app.opcoes import CATEGORIAS_CONTEUDO
from app.servicos import conteudo_servico, indicadores_servico

bp = Blueprint("conteudo", __name__, url_prefix="/conteudos")


def _contar_visitante():
    # indicador da seção 2.3: acessos de quem não tem cadastro
    if not current_user.is_authenticated:
        indicadores_servico.incrementar(indicadores_servico.CHAVE_ACESSO_ANONIMO)


@bp.route("/")
def lista():
    categoria = request.args.get("categoria") or None
    if categoria not in CATEGORIAS_CONTEUDO:
        categoria = None
    _contar_visitante()
    return render_template(
        "conteudo/lista.html",
        conteudos=conteudo_servico.listar(categoria, recentes=True),
        categorias=CATEGORIAS_CONTEUDO,
        categoria_atual=categoria,
        contagem=conteudo_servico.contar_por_categoria(),
    )


@bp.route("/<int:id_conteudo>")
def detalhe(id_conteudo):
    conteudo = db.get_or_404(ConteudoInformativo, id_conteudo)
    _contar_visitante()
    return render_template(
        "conteudo/detalhe.html",
        conteudo=conteudo,
        outros=conteudo_servico.outros_conteudos(conteudo),
        mesma_categoria=conteudo_servico.listar(conteudo.categoria),
    )
