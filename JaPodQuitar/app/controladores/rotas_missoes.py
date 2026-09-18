"""Programa de missoes diarias, entregues uma a uma (RF05)."""

from flask import Blueprint, render_template

bp_missoes = Blueprint("missoes", __name__)


@bp_missoes.route("/")
def missao_atual():
    # TODO (Sprint 2): consultar o inicio da fila (RN03).
    return render_template("missoes/missao_atual.html")


@bp_missoes.route("/concluir", methods=["POST"])
def concluir():
    # TODO (Sprint 2): desenfileirar e liberar a proxima missao.
    return render_template("missoes/missao_atual.html")


@bp_missoes.route("/historico")
def historico():
    return render_template("missoes/historico.html")
