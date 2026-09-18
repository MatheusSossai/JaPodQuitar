"""A area aberta responde sem autenticacao (RF02)."""


def test_pagina_inicial_responde_200(cliente):
    assert cliente.get("/").status_code == 200


def test_modulo_informativo_dispensa_cadastro(cliente):
    assert cliente.get("/conteudo/").status_code == 200
