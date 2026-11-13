import json
from datetime import date

from flask import Blueprint, flash, make_response, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user

from app.excecoes import RegraNegocioErro
from app.opcoes import NIVEIS_DEPENDENCIA
from app.rotas.acesso import perfil_requerido, usuario_logado
from app.servicos import conta_servico

bp = Blueprint("perfil", __name__)


@bp.route("/perfil", methods=["GET", "POST"])
@perfil_requerido("usuario")
def consumo():
    if request.method == "POST":
        try:
            conta_servico.salvar_perfil_consumo(usuario_logado(), request.form)
        except RegraNegocioErro as erro:
            flash(str(erro), "danger")
            return render_template("perfil/consumo.html", dados=request.form, niveis=NIVEIS_DEPENDENCIA)
        flash("Perfil de consumo salvo.", "success")
        if current_user.programa_ativo():
            return redirect(url_for("painel.usuario"))
        return redirect(url_for("programa.novo"))

    dados = {
        "consumo_diario_anterior": current_user.consumo_diario_anterior,
        "custo_semanal_anterior": current_user.custo_semanal_anterior,
        "nivel_dependencia": current_user.nivel_dependencia,
        "tempo_uso_meses": current_user.tempo_uso_meses,
    }
    dados = {chave: ("" if valor is None else valor) for chave, valor in dados.items()}
    return render_template("perfil/consumo.html", dados=dados, niveis=NIVEIS_DEPENDENCIA)


@bp.route("/conta")
@login_required
def conta():
    return render_template("perfil/conta.html")


@bp.route("/conta/nome", methods=["POST"])
@login_required
def alterar_nome():
    try:
        conta_servico.alterar_nome(usuario_logado(), request.form.get("nome"))
    except RegraNegocioErro as erro:
        flash(str(erro), "danger")
    else:
        flash("Nome atualizado.", "success")
    return redirect(url_for("perfil.conta"))


@bp.route("/conta/senha", methods=["POST"])
@login_required
def alterar_senha():
    try:
        conta_servico.alterar_senha(
            usuario_logado(),
            request.form.get("senha_atual"),
            request.form.get("nova_senha"),
            request.form.get("confirmacao"),
        )
    except RegraNegocioErro as erro:
        flash(str(erro), "danger")
    else:
        flash("Senha alterada.", "success")
    return redirect(url_for("perfil.conta"))


@bp.route("/conta/exportar")
@perfil_requerido("usuario")
def exportar():
    dados = conta_servico.exportar_dados(usuario_logado())
    resposta = make_response(json.dumps(dados, ensure_ascii=False, indent=2))
    resposta.headers["Content-Type"] = "application/json; charset=utf-8"
    nome_arquivo = f"japodquitar_meus_dados_{date.today():%Y%m%d}.json"
    resposta.headers["Content-Disposition"] = f"attachment; filename={nome_arquivo}"
    return resposta


@bp.route("/conta/excluir", methods=["POST"])
@perfil_requerido("usuario")
def excluir():
    try:
        conta_servico.excluir_conta(
            usuario_logado(),
            request.form.get("senha"),
            request.form.get("confirmacao") == "sim",
        )
    except RegraNegocioErro as erro:
        flash(str(erro), "danger")
        return redirect(url_for("perfil.conta"))
    logout_user()
    flash("Sua conta e todos os seus dados foram excluídos.", "info")
    return redirect(url_for("principal.index"))
