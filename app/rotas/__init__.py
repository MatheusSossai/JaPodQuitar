def registrar_blueprints(app):
    from app.rotas import auth, conteudo, diario, moderacao, painel, perfil, principal, programa

    for modulo in (principal, auth, painel, perfil, programa, diario, conteudo, moderacao):
        app.register_blueprint(modulo.bp)
