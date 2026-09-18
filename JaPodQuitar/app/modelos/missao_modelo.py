"""Tabelas MISSAO (tabela unica com discriminador) e PROGRAMA_MISSAO (fila)."""

from app.extensions import db


class MissaoModelo(db.Model):
    __tablename__ = "missao"

    id_missao = db.Column(db.Integer, primary_key=True)
    id_conteudo = db.Column(
        db.Integer, db.ForeignKey("conteudo_informativo.id_conteudo"), nullable=True
    )
    titulo = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text)
    ordem_dia = db.Column(db.Integer, nullable=False)
    tipo_missao = db.Column(db.Text, nullable=False)   # reflexiva|pratica|educativa
    pergunta_gatilho = db.Column(db.Text, nullable=True)
    acao_substituta = db.Column(db.Text, nullable=True)

    conteudo = db.relationship("ConteudoInformativoModelo")


class ProgramaMissaoModelo(db.Model):
    """Materializa a fila: posicao_fila define a ordem de saida (RN02)."""

    __tablename__ = "programa_missao"

    id_programa_missao = db.Column(db.Integer, primary_key=True)
    id_programa = db.Column(
        db.Integer, db.ForeignKey("programa_cessacao.id_programa"), nullable=False
    )
    id_missao = db.Column(db.Integer, db.ForeignKey("missao.id_missao"), nullable=False)
    posicao_fila = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Text, nullable=False, default="pendente")  # RN03
    data_conclusao = db.Column(db.Text)   # ISO-8601

    programa = db.relationship("ProgramaCessacaoModelo", back_populates="missoes")
    missao = db.relationship("MissaoModelo")
