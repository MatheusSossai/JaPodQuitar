"""Cria o arquivo dados/japodquitar.db com todas as tabelas do DER.

Uso:
    python scripts/criar_banco.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import criar_app           # noqa: E402
from app.extensions import db       # noqa: E402
import app.modelos                  # noqa: F401,E402  (registra os modelos)


def main() -> None:
    aplicacao = criar_app()
    with aplicacao.app_context():
        db.create_all()
        print("Banco criado em:", aplicacao.config["SQLALCHEMY_DATABASE_URI"])


if __name__ == "__main__":
    main()
