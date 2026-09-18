"""Painel do usuario: contadores, economia e perfil de consumo (RF03, RF07)."""

from flask import Blueprint, render_template

bp_painel = Blueprint("painel", __name__)


@bp_painel.route("/")
def inicio():
    # TODO (Sprint 4): dias sem nicotina e economia via ServicoMetricas.
    return render_template("painel/painel.html")


@bp_painel.route("/perfil-consumo", methods=["GET", "POST"])
def perfil_consumo():
    # TODO (Sprint 1): registrar frequencia, tempo de uso e gasto semanal (RF03).
    return render_template("painel/perfil_consumo.html")


@bp_painel.route("/meus-dados")
def meus_dados():
    # TODO (Sprint 4): exportacao e exclusao de dados (RF12).
    return render_template("painel/meus_dados.html")
