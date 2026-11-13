from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.excecoes import RegraNegocioErro
from app.opcoes import GATILHOS, SINTOMAS
from app.rotas.acesso import perfil_requerido, usuario_logado
from app.servicos import diario_servico, programa_servico

bp = Blueprint("diario", __name__, url_prefix="/diario")


@bp.route("/")
@perfil_requerido("usuario")
def lista():
    id_programa = request.args.get("programa", type=int)
    if id_programa:
        programa = programa_servico.obter_programa_do_usuario(usuario_logado(), id_programa)
        if programa is None:
            abort(404)
    else:
        programa = current_user.programa_ativo()

    registros = programa.montar_diario().listar_recentes() if programa else []
    return render_template("diario/lista.html", programa=programa, registros=registros)


@bp.route("/novo", methods=["GET", "POST"])
@perfil_requerido("usuario")
def novo():
    tipo = request.args.get("tipo", "sintoma")
    if tipo not in diario_servico.TIPOS_REGISTRO:
        tipo = "sintoma"
    if current_user.programa_ativo() is None:
        flash("Para usar o diário você precisa de um programa ativo.", "info")
        return redirect(url_for("programa.novo"))

    if request.method == "POST":
        usuario = usuario_logado()
        try:
            registro = diario_servico.registrar_ocorrencia(usuario, tipo, request.form)
        except RegraNegocioErro as erro:
            flash(str(erro), "danger")
        else:
            # polimorfismo: cada tipo de registro tem a sua mensagem
            flash(registro.mensagem_confirmacao(), "success")
            if diario_servico.precisa_alerta_apoio(usuario):
                flash(
                    "Você registrou várias recaídas nos últimos 7 dias. Isso acontece com muita gente. "
                    "Talvez seja um bom momento para buscar apoio, veja a página Onde buscar ajuda.",
                    "warning",
                )
            return redirect(url_for("diario.lista"))

    return render_template(
        "diario/novo.html", tipo=tipo, dados=request.form, sintomas=SINTOMAS, gatilhos=GATILHOS
    )


@bp.route("/<int:id_registro>/complementar", methods=["GET", "POST"])
@perfil_requerido("usuario")
def complementar(id_registro):
    registro = diario_servico.obter_registro_do_usuario(usuario_logado(), id_registro)
    if registro is None:
        abort(404)

    if request.method == "POST":
        try:
            diario_servico.complementar_registro(usuario_logado(), id_registro, request.form.get("complemento"))
        except RegraNegocioErro as erro:
            flash(str(erro), "danger")
        else:
            flash("Complemento adicionado ao registro.", "success")
            return redirect(url_for("diario.lista", programa=registro.id_programa))

    return render_template("diario/complementar.html", registro=registro)


@bp.route("/padroes")
@perfil_requerido("usuario")
def padroes():
    return render_template("diario/padroes.html", resumo=diario_servico.resumo_padroes(usuario_logado()))
