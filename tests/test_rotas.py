"""Testes passando pelas rotas, como se fosse alguém usando o site."""
from app.dados_iniciais import EMAIL_MODERADOR, SENHA_MODERADOR
from app.extensoes import db
from app.modelos import ContadorAcesso, ConteudoInformativo, Pessoa, ProgramaCessacao, RegistroDiario
from app.servicos import diario_servico


def test_modulo_informativo_aberto_sem_login(cliente):
    resposta = cliente.get("/conteudos/")
    assert resposta.status_code == 200
    assert "O que tem dentro de um pod" in resposta.get_data(as_text=True)


def test_acesso_anonimo_e_contado(app, cliente):
    cliente.get("/conteudos/")
    cliente.get("/conteudos/1")
    with app.app_context():
        assert db.session.get(ContadorAcesso, "acesso_informativo_anonimo").total == 2


def test_paginas_publicas(cliente):
    for url in ["/", "/apoio", "/privacidade", "/entrar", "/cadastro"]:
        assert cliente.get(url).status_code == 200


def test_painel_exige_login(cliente):
    resposta = cliente.get("/painel/")
    assert resposta.status_code == 302
    assert "/entrar" in resposta.headers["Location"]


def test_cadastro_login_e_perfil(cliente):
    resposta = cliente.post("/cadastro", data={
        "nome": "Bia", "email": "bia@email.com", "senha": "senha1234",
        "confirmacao": "senha1234", "consentimento": "sim",
    }, follow_redirects=True)
    assert "Perfil de consumo" in resposta.get_data(as_text=True)

    resposta = cliente.post("/perfil", data={
        "consumo_diario_anterior": "150", "custo_semanal_anterior": "45,50",
        "nivel_dependencia": "Alto", "tempo_uso_meses": "8",
    }, follow_redirects=True)
    assert "Começar o programa" in resposta.get_data(as_text=True)

    resposta = cliente.post("/programa/novo", data={"meta_dias": "30"}, follow_redirects=True)
    texto = resposta.get_data(as_text=True)
    assert "Mapeie seus gatilhos" in texto

    cliente.get("/sair")
    resposta = cliente.post("/entrar", data={"email": "bia@email.com", "senha": "senha1234"}, follow_redirects=True)
    assert "Olá, Bia" in resposta.get_data(as_text=True)


def test_cadastro_sem_consentimento(cliente):
    resposta = cliente.post("/cadastro", data={
        "nome": "Caio", "email": "caio@email.com", "senha": "senha1234", "confirmacao": "senha1234",
    })
    assert "precisa concordar com a política de privacidade" in resposta.get_data(as_text=True)
    assert cliente.get("/painel/").status_code == 302


def test_login_com_senha_errada(cliente, criar_conta, login):
    criar_conta("ana@email.com")
    resposta = login("ana@email.com", "errada123")
    assert "E-mail ou senha incorretos" in resposta.get_data(as_text=True)


def test_registro_pelo_diario_em_poucos_passos(app, cliente, criar_conta, login):
    criar_conta("dani@email.com")
    login("dani@email.com")

    resposta = cliente.post("/diario/novo?tipo=sintoma", data={
        "sintoma": "Insônia ou sono ruim", "intensidade": "3",
    }, follow_redirects=True)
    texto = resposta.get_data(as_text=True)
    assert "Sintoma registrado" in texto
    assert "Insônia ou sono ruim, intensidade 3 de 5" in texto


def test_usuario_nao_ve_diario_de_outra_pessoa(app, cliente, criar_conta, login):
    id_dono = criar_conta("dono@email.com")
    criar_conta("curioso@email.com")
    with app.app_context():
        dono = db.session.get(Pessoa, id_dono)
        registro = diario_servico.registrar_ocorrencia(dono, "conquista", {"marco": "segredo"})
        id_registro = registro.id_registro
        id_programa = registro.id_programa

    login("curioso@email.com")
    assert cliente.get(f"/diario/{id_registro}/complementar").status_code == 404
    assert cliente.get(f"/diario/?programa={id_programa}").status_code == 404


def test_usuario_nao_entra_na_moderacao(cliente, criar_conta, login):
    criar_conta("comum@email.com")
    login("comum@email.com")
    assert cliente.get("/moderacao/conteudos").status_code == 403


def test_moderador_crud_de_conteudo(app, cliente, login):
    login(EMAIL_MODERADOR, SENHA_MODERADOR)

    # sem fonte não publica (RN10)
    resposta = cliente.post("/moderacao/conteudos/novo", data={
        "titulo": "Teste", "categoria": "Pulmões", "corpo": "Texto de teste.", "fonte": "",
    }, follow_redirects=True)
    assert "Preencha o campo fonte" in resposta.get_data(as_text=True)

    cliente.post("/moderacao/conteudos/novo", data={
        "titulo": "Teste", "categoria": "Pulmões", "corpo": "Texto de teste.", "fonte": "INCA, 2016.",
    })
    with app.app_context():
        conteudo = db.session.scalar(db.select(ConteudoInformativo).where(ConteudoInformativo.titulo == "Teste"))
        assert conteudo is not None
        id_conteudo = conteudo.id_conteudo

    cliente.post(f"/moderacao/conteudos/{id_conteudo}/editar", data={
        "titulo": "Teste editado", "categoria": "Pulmões", "corpo": "Texto novo.", "fonte": "INCA, 2016.",
    })
    with app.app_context():
        assert db.session.get(ConteudoInformativo, id_conteudo).titulo == "Teste editado"

    cliente.post(f"/moderacao/conteudos/{id_conteudo}/excluir")
    with app.app_context():
        assert db.session.get(ConteudoInformativo, id_conteudo) is None


def test_moderador_nao_exclui_conteudo_usado_em_missao(app, cliente, login):
    login(EMAIL_MODERADOR, SENHA_MODERADOR)
    resposta = cliente.post("/moderacao/conteudos/1/excluir", follow_redirects=True)
    assert "usado pela missão" in resposta.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(ConteudoInformativo, 1) is not None


def test_rn02_moderador_nao_cria_missao_pratica_no_dia_1(cliente, login):
    login(EMAIL_MODERADOR, SENHA_MODERADOR)
    resposta = cliente.post("/moderacao/missoes/nova?tipo=pratica", data={
        "titulo": "Teste", "descricao": "x", "ordem_dia": "1", "acao_substituta": "y", "duracao_min": "5",
    }, follow_redirects=True)
    assert "precisa ser reflexiva" in resposta.get_data(as_text=True)


def test_exportar_e_excluir_conta(app, cliente, criar_conta, login):
    criar_conta("sai@email.com")
    login("sai@email.com")

    resposta = cliente.get("/conta/exportar")
    assert resposta.status_code == 200
    dados = resposta.get_json()
    assert dados["conta"]["email"] == "sai@email.com"
    assert len(dados["programas"]) == 1

    resposta = cliente.post("/conta/excluir", data={"senha": "senha1234", "confirmacao": "sim"}, follow_redirects=True)
    assert "foram excluídos" in resposta.get_data(as_text=True)

    with app.app_context():
        assert db.session.scalar(db.select(Pessoa).where(Pessoa.email == "sai@email.com")) is None
        assert db.session.scalars(db.select(ProgramaCessacao)).all() == []
        assert db.session.scalars(db.select(RegistroDiario)).all() == []
