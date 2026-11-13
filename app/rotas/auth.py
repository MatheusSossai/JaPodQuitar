from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.excecoes import RegraNegocioErro
from app.rotas.acesso import destino_seguro
from app.servicos import conta_servico

bp = Blueprint("auth", __name__)


@bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for("painel.inicio"))

    if request.method == "POST":
        try:
            usuario = conta_servico.cadastrar_usuario(
                nome=request.form.get("nome"),
                email=request.form.get("email"),
                senha=request.form.get("senha"),
                confirmacao=request.form.get("confirmacao"),
                consentiu=request.form.get("consentimento") == "sim",
            )
        except RegraNegocioErro as erro:
            flash(str(erro), "danger")
        else:
            login_user(usuario)
            flash("Conta criada! Agora conte um pouco sobre o seu consumo para a gente calcular o seu progresso.", "success")
            return redirect(url_for("perfil.consumo"))

    return render_template("auth/cadastro.html", dados=request.form)


@bp.route("/entrar", methods=["GET", "POST"])
def entrar():
    if current_user.is_authenticated:
        return redirect(url_for("painel.inicio"))

    if request.method == "POST":
        pessoa = conta_servico.autenticar(request.form.get("email"), request.form.get("senha"))
        if pessoa is None:
            flash("E-mail ou senha incorretos.", "danger")
        else:
            login_user(pessoa, remember=request.form.get("lembrar") == "sim")
            destino = request.args.get("next")
            if not destino_seguro(destino):
                destino = url_for("painel.inicio")
            return redirect(destino)

    return render_template("auth/entrar.html", dados=request.form)


@bp.route("/sair")
@login_required
def sair():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("principal.index"))
