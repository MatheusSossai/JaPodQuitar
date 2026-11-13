import pytest

from app import create_app
from app.config import ConfigTeste
from app.dados_iniciais import popular_banco
from app.extensoes import db
from app.servicos import conta_servico, programa_servico

SENHA_PADRAO = "senha1234"
PERFIL_PADRAO = {
    "consumo_diario_anterior": "200",
    "custo_semanal_anterior": "70",
    "nivel_dependencia": "Moderado",
    "tempo_uso_meses": "12",
}


@pytest.fixture
def app():
    app = create_app(ConfigTeste)
    with app.app_context():
        popular_banco()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def ctx(app):
    """Para os testes que chamam os serviços direto, sem passar pelas rotas."""
    with app.app_context():
        yield


@pytest.fixture
def usuario(ctx):
    u = conta_servico.cadastrar_usuario("Teste", "teste@email.com", SENHA_PADRAO, SENHA_PADRAO, True)
    conta_servico.salvar_perfil_consumo(u, PERFIL_PADRAO)
    return u


@pytest.fixture
def programa(usuario):
    return programa_servico.criar_programa(usuario, 30)


@pytest.fixture
def cliente(app):
    return app.test_client()


@pytest.fixture
def criar_conta(app):
    """Cria um usuário pronto (com perfil e programa) e devolve o id."""

    def _criar(email, com_programa=True):
        with app.app_context():
            u = conta_servico.cadastrar_usuario("Pessoa", email, SENHA_PADRAO, SENHA_PADRAO, True)
            conta_servico.salvar_perfil_consumo(u, PERFIL_PADRAO)
            if com_programa:
                programa_servico.criar_programa(u, 30)
            return u.id_pessoa

    return _criar


@pytest.fixture
def login(cliente):
    def _login(email, senha=SENHA_PADRAO):
        return cliente.post("/entrar", data={"email": email, "senha": senha}, follow_redirects=True)

    return _login
