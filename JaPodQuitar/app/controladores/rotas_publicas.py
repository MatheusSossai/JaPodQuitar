"""Area aberta: pagina inicial, sobre o projeto e canais de apoio (RF10)."""

from flask import Blueprint, render_template

bp_publico = Blueprint("publico", __name__)


@bp_publico.route("/")
def inicio():
    return render_template("publico/index.html")


@bp_publico.route("/sobre")
def sobre():
    return render_template("publico/sobre.html")


@bp_publico.route("/apoio")
def apoio():
    """Canais oficiais da rede publica de saude (RF10)."""
    return render_template("publico/apoio.html")
