"""Fixtures compartilhadas pelos testes (RNF06)."""

import pytest

from app import criar_app
from app.extensions import db


@pytest.fixture
def app():
    aplicacao = criar_app("teste")
    with aplicacao.app_context():
        db.create_all()
        yield aplicacao
        db.session.remove()
        db.drop_all()


@pytest.fixture
def cliente(app):
    return app.test_client()
