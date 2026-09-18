"""Area do moderador: publicacao de conteudo referenciado (RF11, RN10)."""

from flask import Blueprint, render_template

bp_moderacao = Blueprint("moderacao", __name__)


@bp_moderacao.route("/")
def inicio():
    # TODO (Sprint 2): restringir o acesso ao perfil moderador.
    return render_template("moderacao/painel_moderador.html")


@bp_moderacao.route("/conteudo/novo", methods=["GET", "POST"])
def novo_conteudo():
    # TODO (Sprint 2): campo fonte obrigatorio (RN10).
    return render_template("moderacao/formulario_conteudo.html")
