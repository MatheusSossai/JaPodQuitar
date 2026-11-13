from datetime import date

from flask import Flask, render_template
from flask_wtf.csrf import CSRFError
from markupsafe import Markup, escape

from app.config import Config
from app.extensoes import csrf, db, login_manager
from app.formatacao import texto_para_html
from app.opcoes import ICONES_CATEGORIA


def create_app(config=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.entrar"
    login_manager.login_message = "Entre na sua conta para acessar essa página."
    login_manager.login_message_category = "info"

    # importa os modelos para o SQLAlchemy conhecer todas as tabelas
    from app import modelos  # noqa: F401
    from app.modelos import Pessoa

    @login_manager.user_loader
    def carregar_pessoa(id_pessoa):
        return db.session.get(Pessoa, int(id_pessoa))

    from app.rotas import registrar_blueprints

    registrar_blueprints(app)
    registrar_filtros(app)
    registrar_erros(app)

    @app.context_processor
    def variaveis_globais():
        return {"ano_atual": date.today().year, "icones_categoria": ICONES_CATEGORIA}

    with app.app_context():
        db.create_all()
        if app.config.get("POPULAR_AUTOMATICO"):
            from app.dados_iniciais import popular_banco

            popular_banco()

    return app


def registrar_filtros(app):
    @app.template_filter("data_br")
    def data_br(valor):
        return valor.strftime("%d/%m/%Y") if valor else "-"

    @app.template_filter("data_hora_br")
    def data_hora_br(valor):
        return valor.strftime("%d/%m/%Y às %H:%M") if valor else "-"

    @app.template_filter("moeda")
    def moeda(valor):
        texto = f"{valor or 0:,.2f}"
        # troca o formato americano (1,234.56) pelo brasileiro (1.234,56)
        return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")

    @app.template_filter("pct")
    def pct(valor):
        valor = valor or 0
        if valor == int(valor):
            return f"{int(valor)}%"
        return f"{valor:.1f}%".replace(".", ",")

    @app.template_filter("nl2br")
    def nl2br(texto):
        if not texto:
            return ""
        return Markup("<br>").join(escape(linha) for linha in texto.split("\n"))

    @app.template_filter("formatar_texto")
    def formatar_texto(texto):
        return texto_para_html(texto)


def registrar_erros(app):
    @app.errorhandler(403)
    def proibido(erro):
        return render_template("erro.html", codigo=403, mensagem="Você não tem permissão para acessar essa página."), 403

    @app.errorhandler(404)
    def nao_encontrado(erro):
        return render_template("erro.html", codigo=404, mensagem="Não encontramos a página que você procurou."), 404

    @app.errorhandler(CSRFError)
    def erro_csrf(erro):
        return render_template("erro.html", codigo=400, mensagem="O formulário expirou. Volte, recarregue a página e tente de novo."), 400
