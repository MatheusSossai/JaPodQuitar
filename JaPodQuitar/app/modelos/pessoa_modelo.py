"""Tabelas PESSOA, USUARIO e MODERADOR (heranca joined)."""

from flask_login import UserMixin

from app.extensions import db


class PessoaModelo(UserMixin, db.Model):
    __tablename__ = "pessoa"

    id_pessoa = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)   # UK
    senha_hash = db.Column(db.Text, nullable=False)           # RNF03
    data_cadastro = db.Column(db.Text, nullable=False)        # ISO-8601
    tipo_pessoa = db.Column(db.Text, nullable=False)          # discriminador

    __mapper_args__ = {
        "polymorphic_on": tipo_pessoa,
        "polymorphic_identity": "pessoa",
    }

    def get_id(self) -> str:
        return str(self.id_pessoa)


class UsuarioModelo(PessoaModelo):
    __tablename__ = "usuario"

    id_pessoa = db.Column(
        db.Integer, db.ForeignKey("pessoa.id_pessoa"), primary_key=True
    )
    data_inicio_abstinencia = db.Column(db.Text)        # ISO-8601
    consumo_diario_anterior = db.Column(db.Integer)
    custo_semanal_anterior = db.Column(db.Float)   # REAL no SQLite
    nivel_dependencia = db.Column(db.Text)

    programas = db.relationship(
        "ProgramaCessacaoModelo",
        back_populates="usuario",
        cascade="all, delete-orphan",   # composicao: RF12
    )

    __mapper_args__ = {"polymorphic_identity": "usuario"}


class ModeradorModelo(PessoaModelo):
    __tablename__ = "moderador"

    id_pessoa = db.Column(
        db.Integer, db.ForeignKey("pessoa.id_pessoa"), primary_key=True
    )
    registro_profissional = db.Column(db.Text)
    area_atuacao = db.Column(db.Text)

    conteudos = db.relationship(
        "ConteudoInformativoModelo", back_populates="moderador"
    )

    __mapper_args__ = {"polymorphic_identity": "moderador"}
