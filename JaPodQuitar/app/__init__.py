"""Fabrica da aplicacao Flask (camada de configuracao/inicializacao).

Concentra a criacao do objeto Flask, a inicializacao das extensoes e o
registro dos blueprints (camada de controle). Manter a criacao em uma funcao
permite subir a aplicacao com configuracoes diferentes em desenvolvimento,
teste e producao sem duplicar codigo.
"""

from flask import Flask, render_template

from app.config import obter_configuracao
from app.extensions import db, gerenciador_login


def criar_app(ambiente: str | None = None) -> Flask:
    """Cria e configura uma instancia da aplicacao."""
    app = Flask(__name__)
    app.config.from_object(obter_configuracao(ambiente))

    _inicializar_extensoes(app)
    _registrar_blueprints(app)
    _registrar_tratadores_de_erro(app)

    return app


def _inicializar_extensoes(app: Flask) -> None:
    db.init_app(app)
    gerenciador_login.init_app(app)
    gerenciador_login.login_view = "autenticacao.login"
    gerenciador_login.login_message = "Entre na sua conta para continuar."

    # Importar os modelos registra as tabelas no metadata do SQLAlchemy,
    # o que e necessario antes de qualquer db.create_all().
    from app.modelos import PessoaModelo  # noqa: F401

    @gerenciador_login.user_loader
    def carregar_pessoa(id_pessoa: str):
        return db.session.get(PessoaModelo, int(id_pessoa))


def _registrar_blueprints(app: Flask) -> None:
    from app.controladores.rotas_publicas import bp_publico
    from app.controladores.rotas_autenticacao import bp_autenticacao
    from app.controladores.rotas_painel import bp_painel
    from app.controladores.rotas_missoes import bp_missoes
    from app.controladores.rotas_diario import bp_diario
    from app.controladores.rotas_conteudo import bp_conteudo
    from app.controladores.rotas_moderacao import bp_moderacao

    app.register_blueprint(bp_publico)
    app.register_blueprint(bp_autenticacao, url_prefix="/conta")
    app.register_blueprint(bp_painel, url_prefix="/painel")
    app.register_blueprint(bp_missoes, url_prefix="/missoes")
    app.register_blueprint(bp_diario, url_prefix="/diario")
    app.register_blueprint(bp_conteudo, url_prefix="/conteudo")
    app.register_blueprint(bp_moderacao, url_prefix="/moderacao")


def _registrar_tratadores_de_erro(app: Flask) -> None:
    @app.errorhandler(404)
    def pagina_nao_encontrada(_erro):
        return render_template("erros/404.html"), 404

    @app.errorhandler(500)
    def erro_interno(_erro):
        db.session.rollback()
        return render_template("erros/500.html"), 500
