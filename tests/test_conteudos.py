"""Testes do módulo de matérias: formatação do texto e carga das matérias."""
from app.dados_iniciais import CONTEUDOS, adicionar_conteudos_novos
from app.extensoes import db
from app.formatacao import texto_para_html
from app.modelos import ConteudoInformativo
from app.opcoes import CATEGORIAS_CONTEUDO


def test_formatacao_de_subtitulo_lista_e_paragrafo():
    html = str(texto_para_html("Primeiro parágrafo.\n\n## Resultado\n- item um;\n- item dois.\n\nFim."))
    assert "<p>Primeiro parágrafo.</p>" in html
    assert "<h2>Resultado</h2>" in html
    assert "<ul><li>item um;</li><li>item dois.</li></ul>" in html
    assert html.endswith("<p>Fim.</p>")


def test_formatacao_nao_deixa_passar_html():
    html = str(texto_para_html("<script>alert(1)</script>\n\n## <b>oi</b>"))
    assert "<script>" not in html
    assert "&lt;script&gt;" in html
    assert "<b>" not in html


def test_todas_as_materias_tem_fonte_e_categoria_valida():
    for dados in CONTEUDOS.values():
        assert dados["fonte"].strip()
        assert dados["categoria"] in CATEGORIAS_CONTEUDO


def test_resumo_sem_marcacoes_e_tempo_de_leitura(ctx):
    conteudo = db.session.scalar(
        db.select(ConteudoInformativo).where(ConteudoInformativo.titulo == CONTEUDOS["diacetil"]["titulo"])
    )
    assert "##" not in conteudo.resumir()
    assert conteudo.tempo_leitura() >= 1


def test_adicionar_conteudos_novos_em_banco_antigo(ctx):
    total = len(CONTEUDOS)
    # simula um banco criado antes das matérias novas
    antiga = db.session.scalar(
        db.select(ConteudoInformativo).where(ConteudoInformativo.titulo == CONTEUDOS["mitos"]["titulo"])
    )
    db.session.delete(antiga)
    db.session.commit()

    assert adicionar_conteudos_novos() == 1
    assert adicionar_conteudos_novos() == 0
    assert len(db.session.scalars(db.select(ConteudoInformativo)).all()) == total


def test_pagina_da_materia_mostra_subtitulos(cliente):
    resposta = cliente.get("/conteudos/")
    assert "Pulmão de pipoca" in resposta.get_data(as_text=True)

    resposta = cliente.get("/conteudos/?categoria=Pulmões")
    texto = resposta.get_data(as_text=True)
    assert "Tosse e bronquite em adolescentes" in texto
    assert "Nicotina e dependência" not in texto
