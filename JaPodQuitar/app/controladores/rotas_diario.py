"""Diario de progresso: sintomas, recaidas e conquistas (RF06)."""

from flask import Blueprint, render_template

bp_diario = Blueprint("diario", __name__)


@bp_diario.route("/")
def listar():
    # TODO (Sprint 3): exibir do topo da pilha para baixo (RN04).
    return render_template("diario/diario.html")


@bp_diario.route("/novo", methods=["GET", "POST"])
def novo_registro():
    # TODO (Sprint 3): no maximo tres toques ate aqui (RNF01).
    return render_template("diario/novo_registro.html")
