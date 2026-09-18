"""Tabela CONTEUDO_INFORMATIVO (RN10, RNF05)."""

from app.extensions import db


class ConteudoInformativoModelo(db.Model):
    __tablename__ = "conteudo_informativo"

    id_conteudo = db.Column(db.Integer, primary_key=True)
    id_pessoa_moderador = db.Column(
        db.Integer, db.ForeignKey("moderador.id_pessoa"), nullable=False
    )
    titulo = db.Column(db.Text, nullable=False)
    corpo = db.Column(db.Text, nullable=False)
    fonte = db.Column(db.Text, nullable=False)     # obrigatorio (RNF05)
    categoria = db.Column(db.Text)

    moderador = db.relationship("ModeradorModelo", back_populates="conteudos")
