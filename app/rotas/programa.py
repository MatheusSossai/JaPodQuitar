from datetime import date, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.excecoes import RegraNegocioErro
from app.rotas.acesso import perfil_requerido, usuario_logado
from app.servicos import programa_servico

bp = Blueprint("programa", __name__, url_prefix="/programa")


def _programa_ativo_ou_aviso():
    programa = current_user.programa_ativo()
    if programa is None:
        flash("Você ainda não tem um programa ativo. Que tal começar um agora?", "info")
    return programa


@bp.route("/")
@perfil_requerido("usuario")
def detalhe():
    programa = _programa_ativo_ou_aviso()
    if programa is None:
        return redirect(url_for("programa.novo"))
    return render_template(
        "programa/detalhe.html",
        programa=programa,
        atual=programa.missao_atual(),
        fila=programa.montar_fila(),
        concluidas=programa.missoes_concluidas(),
        hoje=date.today(),
    )


@bp.route("/novo", methods=["GET", "POST"])
@perfil_requerido("usuario")
def novo():
    if current_user.programa_ativo():
        flash("Você já tem um programa ativo. Para começar outro, encerre o atual.", "info")
        return redirect(url_for("programa.detalhe"))
    if not current_user.tem_perfil_consumo():
        flash("Preencha o seu perfil de consumo antes de começar.", "info")
        return redirect(url_for("perfil.consumo"))

    if request.method == "POST":
        try:
            programa_servico.criar_programa(
                usuario_logado(), request.form.get("meta_dias"), request.form.get("data_inicio")
            )
        except RegraNegocioErro as erro:
            flash(str(erro), "danger")
        else:
            flash("Programa criado! A sua primeira missão já está liberada.", "success")
            return redirect(url_for("programa.detalhe"))

    hoje = date.today()
    return render_template(
        "programa/novo.html",
        dados=request.form,
        hoje=hoje,
        data_minima=hoje - timedelta(days=programa_servico.DIAS_MAXIMOS_RETROATIVOS),
        total_missoes=programa_servico.total_missoes_catalogo(),
        ja_teve_programa=len(current_user.programas) > 0,
    )


@bp.route("/missao/concluir", methods=["POST"])
@perfil_requerido("usuario")
def concluir_missao():
    programa = _programa_ativo_ou_aviso()
    if programa is None:
        return redirect(url_for("programa.novo"))
    try:
        proxima = programa_servico.concluir_missao_atual(programa, request.form.get("resposta"))
    except RegraNegocioErro as erro:
        flash(str(erro), "danger")
    else:
        if proxima:
            flash("Missão concluída! A próxima já foi liberada.", "success")
        else:
            flash("Missão concluída! Você terminou todas as missões do programa.", "success")
    return redirect(url_for("programa.detalhe"))


@bp.route("/missao/adiar", methods=["POST"])
@perfil_requerido("usuario")
def adiar_missao():
    programa = _programa_ativo_ou_aviso()
    if programa is None:
        return redirect(url_for("programa.novo"))
    try:
        programa_servico.adiar_missao_atual(programa)
    except RegraNegocioErro as erro:
        flash(str(erro), "danger")
    else:
        flash("Missão adiada. Ela foi para o fim da fila e a próxima foi liberada.", "info")
    return redirect(url_for("programa.detalhe"))


@bp.route("/encerrar", methods=["POST"])
@perfil_requerido("usuario")
def encerrar():
    programa = _programa_ativo_ou_aviso()
    if programa is None:
        return redirect(url_for("programa.novo"))
    motivo = request.form.get("motivo")
    try:
        programa_servico.encerrar_programa(programa, motivo)
    except RegraNegocioErro as erro:
        flash(str(erro), "danger")
        return redirect(url_for("programa.detalhe"))
    if motivo == "concluido":
        flash("Parabéns por chegar até aqui! O programa foi marcado como concluído.", "success")
    else:
        flash("Programa interrompido. Ele continua no seu histórico e você pode começar outro quando quiser.", "info")
    return redirect(url_for("programa.historico"))


@bp.route("/historico")
@perfil_requerido("usuario")
def historico():
    programas = list(reversed(current_user.programas))
    return render_template("programa/historico.html", programas=programas, hoje=date.today())
