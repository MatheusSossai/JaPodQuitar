"""Tabela PROGRAMA_CESSACAO (RN01)."""

from app.extensions import db


class ProgramaCessacaoModelo(db.Model):
    __tablename__ = "programa_cessacao"

    id_programa = db.Column(db.Integer, primary_key=True)
    id_pessoa_usuario = db.Column(
        db.Integer, db.ForeignKey("usuario.id_pessoa"), nullable=False
    )
    data_inicio = db.Column(db.Text, nullable=False)   # ISO-8601
    meta_dias = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Text, nullable=False, default="ativo")

    usuario = db.relationship("UsuarioModelo", back_populates="programas")
    missoes = db.relationship(
        "ProgramaMissaoModelo",
        back_populates="programa",
        cascade="all, delete-orphan",
        order_by="ProgramaMissaoModelo.posicao_fila",
    )
    registros = db.relationship(
        "RegistroDiarioModelo",
        back_populates="programa",
        cascade="all, delete-orphan",
        order_by="RegistroDiarioModelo.posicao_pilha.desc()",
    )
