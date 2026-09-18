"""Tabelas REGISTRO_DIARIO e especializacoes (heranca joined)."""

from app.extensions import db


class RegistroDiarioModelo(db.Model):
    """posicao_pilha materializa a pilha; data_hora e o criterio de desempate."""

    __tablename__ = "registro_diario"

    id_registro = db.Column(db.Integer, primary_key=True)
    id_programa = db.Column(
        db.Integer, db.ForeignKey("programa_cessacao.id_programa"), nullable=False
    )
    data_hora = db.Column(db.Text, nullable=False)     # ISO-8601
    tipo_registro = db.Column(db.Text, nullable=False)  # discriminador
    observacao = db.Column(db.Text)
    posicao_pilha = db.Column(db.Integer, nullable=False)

    programa = db.relationship("ProgramaCessacaoModelo", back_populates="registros")

    __mapper_args__ = {
        "polymorphic_on": tipo_registro,
        "polymorphic_identity": "registro",
    }


class RegistroSintomaModelo(RegistroDiarioModelo):
    __tablename__ = "registro_sintoma"

    id_registro = db.Column(
        db.Integer, db.ForeignKey("registro_diario.id_registro"), primary_key=True
    )
    sintoma = db.Column(db.Text, nullable=False)
    intensidade = db.Column(db.Integer, nullable=False)   # 1 a 5 (RN09)

    __mapper_args__ = {"polymorphic_identity": "sintoma"}


class RegistroRecaidaModelo(RegistroDiarioModelo):
    __tablename__ = "registro_recaida"

    id_registro = db.Column(
        db.Integer, db.ForeignKey("registro_diario.id_registro"), primary_key=True
    )
    quantidade_puffs = db.Column(db.Integer)
    gatilho = db.Column(db.Text)

    __mapper_args__ = {"polymorphic_identity": "recaida"}


class RegistroConquistaModelo(RegistroDiarioModelo):
    __tablename__ = "registro_conquista"

    id_registro = db.Column(
        db.Integer, db.ForeignKey("registro_diario.id_registro"), primary_key=True
    )
    marco = db.Column(db.Text, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "conquista"}
