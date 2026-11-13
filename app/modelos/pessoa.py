from abc import abstractmethod
from datetime import date, datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.excecoes import RegraNegocioErro
from app.extensoes import db
from app.modelos.base import ModeloAbstratoMeta


class Pessoa(UserMixin, db.Model, metaclass=ModeloAbstratoMeta):
    """Classe abstrata com o que usuário e moderador têm em comum.

    Herança mapeada em tabelas separadas (joined): PESSOA guarda os dados comuns
    e USUARIO / MODERADOR guardam só o que é de cada um.
    """

    __tablename__ = "pessoa"

    id_pessoa = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    senha_hash = db.Column(db.Text, nullable=False)
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.now)
    tipo_pessoa = db.Column(db.Text, nullable=False)

    __mapper_args__ = {"polymorphic_on": tipo_pessoa}

    def get_id(self):
        # o Flask-Login procura um atributo "id", aqui a chave se chama id_pessoa
        return str(self.id_pessoa)

    def definir_senha(self, senha):
        # RNF03: a senha nunca é guardada em texto puro
        self.senha_hash = generate_password_hash(senha)

    def autenticar(self, senha):
        return check_password_hash(self.senha_hash, senha or "")

    @abstractmethod
    def exibir_painel(self):
        """Nome da rota do painel inicial de cada perfil."""

    @abstractmethod
    def perfil_acesso(self):
        """Texto que identifica o perfil: 'usuario' ou 'moderador'."""


class Usuario(Pessoa):
    __tablename__ = "usuario"

    id_pessoa = db.Column(db.Integer, db.ForeignKey("pessoa.id_pessoa", ondelete="CASCADE"), primary_key=True)
    data_inicio_abstinencia = db.Column(db.Date)
    consumo_diario_anterior = db.Column(db.Integer)
    custo_semanal_anterior = db.Column(db.Float)
    nivel_dependencia = db.Column(db.Text)
    tempo_uso_meses = db.Column(db.Integer)
    data_consentimento = db.Column(db.DateTime)

    # composição: se a conta for excluída, os programas vão junto (RF12)
    programas = db.relationship(
        "ProgramaCessacao",
        back_populates="usuario",
        cascade="all, delete-orphan",
        order_by="ProgramaCessacao.id_programa",
    )

    __mapper_args__ = {"polymorphic_identity": "usuario", "polymorphic_load": "inline"}

    def exibir_painel(self):
        return "painel.usuario"

    def perfil_acesso(self):
        return "usuario"

    def tem_perfil_consumo(self):
        return self.consumo_diario_anterior is not None and self.custo_semanal_anterior is not None

    def programa_ativo(self):
        # RN01: só pode existir um programa ativo por vez
        for programa in self.programas:
            if programa.status == "ativo":
                return programa
        return None

    def dias_sem_nicotina(self, hoje=None):
        if self.data_inicio_abstinencia is None:
            return 0
        hoje = hoje or date.today()
        return max((hoje - self.data_inicio_abstinencia).days, 0)

    def calcular_economia(self, hoje=None):
        # RN08: (dias sem nicotina / 7) x custo semanal informado no perfil
        if not self.custo_semanal_anterior:
            return 0.0
        return round(self.dias_sem_nicotina(hoje) / 7 * self.custo_semanal_anterior, 2)


class Moderador(Pessoa):
    __tablename__ = "moderador"

    id_pessoa = db.Column(db.Integer, db.ForeignKey("pessoa.id_pessoa", ondelete="CASCADE"), primary_key=True)
    registro_profissional = db.Column(db.Text)
    area_atuacao = db.Column(db.Text)

    conteudos = db.relationship("ConteudoInformativo", back_populates="moderador")

    __mapper_args__ = {"polymorphic_identity": "moderador", "polymorphic_load": "inline"}

    def exibir_painel(self):
        return "painel.moderador"

    def perfil_acesso(self):
        return "moderador"

    def publicar(self, conteudo):
        # RN10 e RNF05: nenhum conteúdo de saúde sai sem fonte
        if not (conteudo.fonte or "").strip():
            raise RegraNegocioErro("Todo conteúdo de saúde precisa ter a fonte preenchida.")
        conteudo.moderador = self
