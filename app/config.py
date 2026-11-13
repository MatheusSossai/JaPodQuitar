import os


class Config:
    # em produção a chave tem que vir de variável de ambiente
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-de-desenvolvimento-troque-em-producao")

    # caminho relativo: o Flask-SQLAlchemy salva o arquivo dentro da pasta instance/
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///japodquitar.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_HTTPONLY = True

    # cria moderador, conteúdos e missões na primeira vez que o sistema roda
    POPULAR_AUTOMATICO = True


class ConfigTeste(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    POPULAR_AUTOMATICO = False
