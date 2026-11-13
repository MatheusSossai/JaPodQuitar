from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.rotas.acesso import perfil_requerido, usuario_logado
from app.servicos import indicadores_servico, painel_servico

bp = Blueprint("painel", __name__, url_prefix="/painel")


@bp.route("/")
@login_required
def inicio():
    # polimorfismo: cada perfil sabe qual é o seu painel
    return redirect(url_for(current_user.exibir_painel()))


@bp.route("/usuario")
@perfil_requerido("usuario")
def usuario():
    if not current_user.tem_perfil_consumo():
        flash("Antes de começar, preencha o seu perfil de consumo.", "info")
        return redirect(url_for("perfil.consumo"))
    resumo = painel_servico.resumo_progresso(usuario_logado())
    return render_template("painel/usuario.html", **resumo)


@bp.route("/moderador")
@perfil_requerido("moderador")
def moderador():
    return render_template("painel/moderador.html", ind=indicadores_servico.calcular_indicadores())
