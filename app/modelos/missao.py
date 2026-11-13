from abc import abstractmethod

from app.excecoes import RegraNegocioErro
from app.extensoes import db
from app.modelos.base import ModeloAbstratoMeta
from app.modelos.conteudo import ConteudoInformativo
from app.validacao import inteiro, texto_obrigatorio


class Missao(db.Model, metaclass=ModeloAbstratoMeta):
    """Missão do catálogo.

    Herança em tabela única: todas as missões ficam na tabela MISSAO e a coluna
    tipo_missao diz qual é a subclasse. As colunas específicas são declaradas
    nas subclasses, mas no banco ficam na mesma tabela (podem ser nulas).
    """

    __tablename__ = "missao"

    id_missao = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    ordem_dia = db.Column(db.Integer, nullable=False)
    tipo_missao = db.Column(db.Text, nullable=False)

    __mapper_args__ = {"polymorphic_on": tipo_missao}

    @abstractmethod
    def executar(self):
        """Texto principal com o que a pessoa precisa fazer."""

    @abstractmethod
    def orientacao(self):
        """Dica de como fazer a missão."""

    @abstractmethod
    def rotulo(self):
        """Nome do tipo para mostrar na tela."""

    def exige_resposta(self):
        return False

    def pode_ser_dia_um(self):
        # RN02: só a missão de mapeamento de gatilhos (reflexiva) pode abrir o programa
        return False

    def pontuacao(self):
        # missões mais para o fim do programa valem um pouco mais
        return 10 + (self.ordem_dia // 7) * 5

    def preencher(self, dados):
        """Preenche os campos comuns a partir de um formulário. As subclasses completam."""
        self.titulo = texto_obrigatorio(dados.get("titulo"), "título", 120)
        self.descricao = texto_obrigatorio(dados.get("descricao"), "descrição", 1000)
        self.ordem_dia = inteiro(dados.get("ordem_dia"), "dia da missão", 1, 365)


class MissaoReflexiva(Missao):
    pergunta_gatilho = db.Column(db.Text)

    __mapper_args__ = {"polymorphic_identity": "reflexiva"}

    def executar(self):
        return self.pergunta_gatilho

    def orientacao(self):
        return "Responda com calma, não existe resposta certa. O que você escrever fica guardado só para você."

    def rotulo(self):
        return "Reflexiva"

    def exige_resposta(self):
        return True

    def pode_ser_dia_um(self):
        return True

    def preencher(self, dados):
        super().preencher(dados)
        self.pergunta_gatilho = texto_obrigatorio(dados.get("pergunta_gatilho"), "pergunta", 1000)


class MissaoPratica(Missao):
    acao_substituta = db.Column(db.Text)
    duracao_min = db.Column(db.Integer)

    __mapper_args__ = {"polymorphic_identity": "pratica"}

    def executar(self):
        return self.acao_substituta

    def orientacao(self):
        return (
            f"Use o cronômetro de {self.duracao_min} min abaixo. A vontade forte costuma durar "
            "poucos minutos, a ideia é atravessar esse tempo fazendo outra coisa."
        )

    def rotulo(self):
        return "Prática"

    def preencher(self, dados):
        super().preencher(dados)
        self.acao_substituta = texto_obrigatorio(dados.get("acao_substituta"), "ação substituta", 1000)
        self.duracao_min = inteiro(dados.get("duracao_min"), "duração", 1, 240)


class MissaoEducativa(Missao):
    id_conteudo = db.Column(db.Integer, db.ForeignKey("conteudo_informativo.id_conteudo"))

    # associação simples: a missão usa um conteúdo publicado pelo moderador
    conteudo = db.relationship("ConteudoInformativo")

    __mapper_args__ = {"polymorphic_identity": "educativa"}

    def executar(self):
        titulo = self.conteudo.titulo if self.conteudo else "indicado"
        return f'Leia o texto "{titulo}" no módulo de informações.'

    def orientacao(self):
        return "Leia com atenção e depois marque como concluída. Se algo chamar sua atenção, anote no diário."

    def rotulo(self):
        return "Educativa"

    def preencher(self, dados):
        super().preencher(dados)
        id_conteudo = inteiro(dados.get("id_conteudo"), "conteúdo", 1)
        conteudo = db.session.get(ConteudoInformativo, id_conteudo)
        if conteudo is None:
            raise RegraNegocioErro("Escolha um conteúdo informativo que exista.")
        self.conteudo = conteudo
