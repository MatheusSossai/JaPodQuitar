"""CRUD do módulo informativo (RF02, RF11, RN10, RNF05)."""
from app.excecoes import RegraNegocioErro
from app.extensoes import db
from app.modelos import ConteudoInformativo, MissaoEducativa
from app.opcoes import CATEGORIAS_CONTEUDO
from app.validacao import escolha, texto_obrigatorio


def listar(categoria=None, limite=None, recentes=False):
    ordem = ConteudoInformativo.id_conteudo.desc() if recentes else ConteudoInformativo.id_conteudo
    consulta = db.select(ConteudoInformativo).order_by(ordem)
    if categoria:
        consulta = consulta.where(ConteudoInformativo.categoria == categoria)
    if limite:
        consulta = consulta.limit(limite)
    return db.session.scalars(consulta).all()


def contar_por_categoria():
    consulta = db.select(ConteudoInformativo.categoria, db.func.count()).group_by(ConteudoInformativo.categoria)
    return dict(db.session.execute(consulta).all())


def outros_conteudos(conteudo, limite=3):
    """Sugestões no fim da matéria: primeiro as da mesma categoria, depois as outras."""
    outros = db.session.scalars(
        db.select(ConteudoInformativo)
        .where(ConteudoInformativo.id_conteudo != conteudo.id_conteudo)
        .order_by(ConteudoInformativo.id_conteudo.desc())
    ).all()
    outros.sort(key=lambda c: c.categoria != conteudo.categoria)  # sort estável: mesma categoria primeiro
    return outros[:limite]


def salvar_conteudo(autor, dados, conteudo=None):
    # RN10: só moderador publica
    if autor.perfil_acesso() != "moderador":
        raise RegraNegocioErro("Somente moderadores podem publicar conteúdo.")

    titulo = texto_obrigatorio(dados.get("titulo"), "título", 150)
    categoria = escolha(dados.get("categoria"), CATEGORIAS_CONTEUDO, "categoria")
    corpo = texto_obrigatorio(dados.get("corpo"), "texto", 10000).replace("\r\n", "\n")
    fonte = texto_obrigatorio(dados.get("fonte"), "fonte", 1000)  # RNF05

    novo = conteudo is None
    if novo:
        conteudo = ConteudoInformativo()
    conteudo.titulo = titulo
    conteudo.categoria = categoria
    conteudo.corpo = corpo
    conteudo.fonte = fonte
    if novo:
        autor.publicar(conteudo)
        db.session.add(conteudo)
    db.session.commit()
    return conteudo


def excluir_conteudo(conteudo):
    missoes = db.session.scalars(
        db.select(MissaoEducativa).where(MissaoEducativa.id_conteudo == conteudo.id_conteudo)
    ).all()
    if missoes:
        nomes = ", ".join(f'"{m.titulo}"' for m in missoes)
        raise RegraNegocioErro(
            f"Esse conteúdo é usado pela missão {nomes}. Troque o conteúdo da missão antes de excluir."
        )
    db.session.delete(conteudo)
    db.session.commit()
