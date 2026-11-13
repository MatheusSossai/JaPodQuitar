"""Área do moderador: CRUD de conteúdos (RF11) e do catálogo de missões."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.excecoes import RegraNegocioErro
from app.extensoes import db
from app.modelos import ConteudoInformativo, Missao
from app.opcoes import CATEGORIAS_CONTEUDO
from app.rotas.acesso import perfil_requerido, usuario_logado
from app.servicos import conteudo_servico, missao_servico

bp = Blueprint("moderacao", __name__, url_prefix="/moderacao")


# ---------- conteúdos ----------

@bp.route("/conteudos")
@perfil_requerido("moderador")
def conteudos():
    return render_template("moderacao/conteudos.html", conteudos=conteudo_servico.listar())


@bp.route("/conteudos/novo", methods=["GET", "POST"])
@perfil_requerido("moderador")
def novo_conteudo():
    if request.method == "POST":
        try:
            conteudo_servico.salvar_conteudo(usuario_logado(), request.form)
        except RegraNegocioErro as erro:
            flash(str(erro), "danger")
        else:
            flash("Conteúdo publicado.", "success")
            return redirect(url_for("moderacao.conteudos"))
    return render_template(
        "moderacao/conteudo_form.html", conteudo=None, dados=request.form, categorias=CATEGORIAS_CONTEUDO
    )


@bp.route("/conteudos/<int:id_conteudo>/editar", methods=["GET", "POST"])
@perfil_requerido("moderador")
def editar_conteudo(id_conteudo):
    conteudo = db.get_or_404(ConteudoInformativo, id_conteudo)
    if request.method == "POST":
        try:
            conteudo_servico.salvar_conteudo(usuario_logado(), request.form, conteudo)
        except RegraNegocioErro as erro:
            flash(str(erro), "danger")
        else:
            flash("Conteúdo atualizado.", "success")
            return redirect(url_for("moderacao.conteudos"))
        dados = request.form
    else:
        dados = {
            "titulo": conteudo.titulo,
            "categoria": conteudo.categoria,
            "corpo": conteudo.corpo,
            "fonte": conteudo.fonte,
        }
    return render_template(
        "moderacao/conteudo_form.html", conteudo=conteudo, dados=dados, categorias=CATEGORIAS_CONTEUDO
    )


@bp.route("/conteudos/<int:id_conteudo>/excluir", methods=["POST"])
@perfil_requerido("moderador")
def excluir_conteudo(id_conteudo):
    conteudo = db.get_or_404(ConteudoInformativo, id_conteudo)
    try:
        conteudo_servico.excluir_conteudo(conteudo)
    except RegraNegocioErro as erro:
        flash(str(erro), "danger")
    else:
        flash("Conteúdo excluído.", "success")
    return redirect(url_for("moderacao.conteudos"))


# ---------- missões ----------

@bp.route("/missoes")
@perfil_requerido("moderador")
def missoes():
    return render_template("moderacao/missoes.html", catalogo=missao_servico.listar_catalogo())


@bp.route("/missoes/nova", methods=["GET", "POST"])
@perfil_requerido("moderador")
def nova_missao():
    tipo = request.args.get("tipo", "reflexiva")
    if tipo not in missao_servico.TIPOS_MISSAO:
        tipo = "reflexiva"
    if request.method == "POST":
        dados = request.form.to_dict()
        dados["tipo_missao"] = tipo
        try:
            missao_servico.salvar_missao(dados)
        except RegraNegocioErro as erro:
            flash(str(erro), "danger")
        else:
            flash("Missão adicionada ao catálogo.", "success")
            return redirect(url_for("moderacao.missoes"))
    return render_template(
        "moderacao/missao_form.html",
        missao=None,
        tipo=tipo,
        dados=request.form,
        conteudos=conteudo_servico.listar(),
    )


@bp.route("/missoes/<int:id_missao>/editar", methods=["GET", "POST"])
@perfil_requerido("moderador")
def editar_missao(id_missao):
    missao = db.get_or_404(Missao, id_missao)
    if request.method == "POST":
        try:
            missao_servico.salvar_missao(request.form, missao)
        except RegraNegocioErro as erro:
            flash(str(erro), "danger")
        else:
            flash("Missão atualizada.", "success")
            return redirect(url_for("moderacao.missoes"))
        dados = request.form
    else:
        dados = {
            "titulo": missao.titulo,
            "descricao": missao.descricao,
            "ordem_dia": missao.ordem_dia,
            "pergunta_gatilho": getattr(missao, "pergunta_gatilho", ""),
            "acao_substituta": getattr(missao, "acao_substituta", ""),
            "duracao_min": getattr(missao, "duracao_min", ""),
            "id_conteudo": getattr(missao, "id_conteudo", ""),
        }
    return render_template(
        "moderacao/missao_form.html",
        missao=missao,
        tipo=missao.tipo_missao,
        dados=dados,
        conteudos=conteudo_servico.listar(),
    )


@bp.route("/missoes/<int:id_missao>/excluir", methods=["POST"])
@perfil_requerido("moderador")
def excluir_missao(id_missao):
    missao = db.get_or_404(Missao, id_missao)
    try:
        missao_servico.excluir_missao(missao)
    except RegraNegocioErro as erro:
        flash(str(erro), "danger")
    else:
        flash("Missão excluída do catálogo.", "success")
    return redirect(url_for("moderacao.missoes"))
