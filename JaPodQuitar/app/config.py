"""Configuracoes por ambiente.

O caminho do banco aponta para dados/japodquitar.db, mantendo o SQLite dentro
do projeto conforme justificado na secao 3.3 do documento de concepcao.
"""

import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA_DADOS = RAIZ / "dados"


class ConfiguracaoBase:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-de-desenvolvimento")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{PASTA_DADOS / 'japodquitar.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Regras de negocio parametrizaveis (secao 1.6)
    INTENSIDADE_MINIMA_SINTOMA = 1   # RN09
    INTENSIDADE_MAXIMA_SINTOMA = 5   # RN09
    RECAIDAS_PARA_ALERTA = 3         # RN07
    JANELA_ALERTA_EM_DIAS = 7        # RN07


class ConfiguracaoDesenvolvimento(ConfiguracaoBase):
    DEBUG = True


class ConfiguracaoTeste(ConfiguracaoBase):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ConfiguracaoProducao(ConfiguracaoBase):
    DEBUG = False


_AMBIENTES = {
    "desenvolvimento": ConfiguracaoDesenvolvimento,
    "teste": ConfiguracaoTeste,
    "producao": ConfiguracaoProducao,
}


def obter_configuracao(ambiente: str | None = None):
    nome = ambiente or os.environ.get("FLASK_ENV", "desenvolvimento")
    return _AMBIENTES.get(nome, ConfiguracaoDesenvolvimento)
