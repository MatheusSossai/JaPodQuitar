"""Modulo informativo aberto (RF02)."""

from flask import Blueprint, render_template

bp_conteudo = Blueprint("conteudo", __name__)


@bp_conteudo.route("/")
def listar():
    return render_template("conteudo/lista.html")


@bp_conteudo.route("/<int:id_conteudo>")
def detalhe(id_conteudo: int):
    # TODO (Sprint 2): exibir sempre a fonte declarada (RNF05).
    return render_template("conteudo/detalhe.html", id_conteudo=id_conteudo)
