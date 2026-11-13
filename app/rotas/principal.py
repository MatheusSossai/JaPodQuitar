from flask import Blueprint, render_template, request

from app.opcoes import CANAIS_APOIO
from app.servicos import conteudo_servico, indicadores_servico

bp = Blueprint("principal", __name__)


@bp.route("/")
def index():
    return render_template(
        "index.html",
        recentes=conteudo_servico.listar(limite=4, recentes=True),
        total_materias=len(conteudo_servico.listar()),
    )


@bp.route("/apoio")
def apoio():
    return render_template("apoio.html", canais=CANAIS_APOIO)


@bp.route("/apoio/clique", methods=["POST"])
def registrar_clique():
    # chamado pelo JavaScript quando alguém clica em um canal de apoio (indicador da seção 2.3)
    canal = request.form.get("canal", "")
    if canal in CANAIS_APOIO:
        indicadores_servico.incrementar(indicadores_servico.chave_clique(canal))
    return "", 204


@bp.route("/privacidade")
def privacidade():
    return render_template("privacidade.html")
