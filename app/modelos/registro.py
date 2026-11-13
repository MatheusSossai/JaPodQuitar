from abc import abstractmethod
from datetime import datetime

from sqlalchemy.orm import validates

from app.excecoes import RegraNegocioErro
from app.extensoes import db
from app.modelos.base import ModeloAbstratoMeta
from app.opcoes import GATILHOS, SINTOMAS
from app.validacao import escolha_com_outro, inteiro, texto_obrigatorio, texto_opcional


class RegistroDiario(db.Model, metaclass=ModeloAbstratoMeta):
    """Registro do diário de progresso (classe abstrata).

    Herança em tabelas separadas (joined): REGISTRO_DIARIO tem o que é comum e
    cada subtipo tem a sua tabela com os campos obrigatórios dele.
    """

    __tablename__ = "registro_diario"

    id_registro = db.Column(db.Integer, primary_key=True)
    id_programa = db.Column(
        db.Integer, db.ForeignKey("programa_cessacao.id_programa", ondelete="CASCADE"), nullable=False
    )
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.now)
    tipo_registro = db.Column(db.Text, nullable=False)
    observacao = db.Column(db.Text)
    posicao_pilha = db.Column(db.Integer, nullable=False)

    programa = db.relationship("ProgramaCessacao", back_populates="registros")

    __mapper_args__ = {"polymorphic_on": tipo_registro}

    @classmethod
    @abstractmethod
    def criar_de_dados(cls, dados):
        """Cria o registro a partir dos dados do formulário, validando os campos do subtipo."""

    @abstractmethod
    def resumo(self):
        """Frase curta que descreve o registro."""

    @abstractmethod
    def impacto(self):
        """-1 zera o contador de dias, 0 é neutro e 1 é positivo."""

    @abstractmethod
    def rotulo(self):
        """Nome do tipo para mostrar na tela."""

    @abstractmethod
    def classe_css(self):
        """Classe usada para a cor da borda na lista do diário."""

    @abstractmethod
    def mensagem_confirmacao(self):
        """Mensagem mostrada depois de salvar."""

    def complementar(self, texto, agora=None):
        """RN05: o registro não pode ser apagado nem reescrito, só complementado."""
        texto = texto_obrigatorio(texto, "complemento", 500)
        carimbo = (agora or datetime.now()).strftime("%d/%m/%Y %H:%M")
        anterior = self.observacao or ""
        separador = "\n" if anterior else ""
        self.observacao = f"{anterior}{separador}[Complemento em {carimbo}] {texto}"

    def para_dict(self):
        return {
            "posicao_pilha": self.posicao_pilha,
            "tipo": self.rotulo(),
            "data_hora": self.data_hora.isoformat(timespec="minutes"),
            "resumo": self.resumo(),
            "observacao": self.observacao,
        }


class RegistroSintoma(RegistroDiario):
    __tablename__ = "registro_sintoma"

    id_registro = db.Column(
        db.Integer, db.ForeignKey("registro_diario.id_registro", ondelete="CASCADE"), primary_key=True
    )
    sintoma = db.Column(db.Text, nullable=False)
    intensidade = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.CheckConstraint("intensidade BETWEEN 1 AND 5", name="ck_intensidade_1_a_5"),)
    __mapper_args__ = {"polymorphic_identity": "sintoma", "polymorphic_load": "inline"}

    @validates("intensidade")
    def _validar_intensidade(self, chave, valor):
        # RN09: escala inteira de 1 a 5
        if isinstance(valor, bool) or not isinstance(valor, int) or not 1 <= valor <= 5:
            raise RegraNegocioErro("A intensidade do sintoma tem que ser um número inteiro de 1 a 5.")
        return valor

    @classmethod
    def criar_de_dados(cls, dados):
        return cls(
            sintoma=escolha_com_outro(dados, "sintoma", "sintoma_outro", SINTOMAS, "sintoma"),
            intensidade=inteiro(dados.get("intensidade"), "intensidade", 1, 5),
            observacao=texto_opcional(dados.get("observacao"), "observação", 500),
        )

    def resumo(self):
        return f"{self.sintoma}, intensidade {self.intensidade} de 5"

    def impacto(self):
        return 0

    def rotulo(self):
        return "Sintoma"

    def classe_css(self):
        return "registro-sintoma"

    def mensagem_confirmacao(self):
        return "Sintoma registrado. Os sintomas de abstinência costumam diminuir com o passar dos dias."

    def para_dict(self):
        dados = super().para_dict()
        dados.update(sintoma=self.sintoma, intensidade=self.intensidade)
        return dados


class RegistroRecaida(RegistroDiario):
    __tablename__ = "registro_recaida"

    id_registro = db.Column(
        db.Integer, db.ForeignKey("registro_diario.id_registro", ondelete="CASCADE"), primary_key=True
    )
    quantidade_puffs = db.Column(db.Integer)
    gatilho = db.Column(db.Text, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "recaida", "polymorphic_load": "inline"}

    @classmethod
    def criar_de_dados(cls, dados):
        puffs = (dados.get("quantidade_puffs") or "").strip()
        return cls(
            quantidade_puffs=inteiro(puffs, "quantidade de puffs", 0, 2000) if puffs else None,
            gatilho=escolha_com_outro(dados, "gatilho", "gatilho_outro", GATILHOS, "gatilho"),
            observacao=texto_opcional(dados.get("observacao"), "observação", 500),
        )

    def resumo(self):
        texto = f"Gatilho: {self.gatilho}"
        if self.quantidade_puffs is not None:
            texto += f", cerca de {self.quantidade_puffs} puffs"
        return texto

    def impacto(self):
        return -1

    def rotulo(self):
        return "Recaída"

    def classe_css(self):
        return "registro-recaida"

    def mensagem_confirmacao(self):
        return (
            "Registro salvo. Uma recaída não apaga o que você já conquistou: "
            "seu recorde e seus dias de programa continuam guardados."
        )

    def para_dict(self):
        dados = super().para_dict()
        dados.update(quantidade_puffs=self.quantidade_puffs, gatilho=self.gatilho)
        return dados


class RegistroConquista(RegistroDiario):
    __tablename__ = "registro_conquista"

    id_registro = db.Column(
        db.Integer, db.ForeignKey("registro_diario.id_registro", ondelete="CASCADE"), primary_key=True
    )
    marco = db.Column(db.Text, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "conquista", "polymorphic_load": "inline"}

    @classmethod
    def criar_de_dados(cls, dados):
        return cls(
            marco=texto_obrigatorio(dados.get("marco"), "conquista", 150),
            observacao=texto_opcional(dados.get("observacao"), "observação", 500),
        )

    def resumo(self):
        return self.marco

    def impacto(self):
        return 1

    def rotulo(self):
        return "Conquista"

    def classe_css(self):
        return "registro-conquista"

    def mensagem_confirmacao(self):
        return "Conquista registrada! Vale lembrar dela nos dias mais difíceis."

    def para_dict(self):
        dados = super().para_dict()
        dados.update(marco=self.marco)
        return dados
