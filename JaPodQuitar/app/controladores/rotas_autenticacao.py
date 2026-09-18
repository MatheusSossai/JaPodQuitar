"""Cadastro, login e logout (RF01)."""

from flask import Blueprint, render_template

bp_autenticacao = Blueprint("autenticacao", __name__)


@bp_autenticacao.route("/entrar", methods=["GET", "POST"])
def login():
    # TODO (Sprint 1): validar credenciais via ServicoAutenticacao.
    return render_template("autenticacao/login.html")


@bp_autenticacao.route("/cadastrar", methods=["GET", "POST"])
def cadastro():
    # TODO (Sprint 1): consentimento explicito antes de gravar (RNF04).
    return render_template("autenticacao/cadastro.html")


@bp_autenticacao.route("/sair")
def logout():
    # TODO (Sprint 1): encerrar sessao com logout_user().
    return render_template("autenticacao/login.html")
