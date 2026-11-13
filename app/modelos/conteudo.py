import math

from app.extensoes import db
from app.formatacao import texto_puro
from app.opcoes import ICONES_CATEGORIA


class ConteudoInformativo(db.Model):
    __tablename__ = "conteudo_informativo"

    id_conteudo = db.Column(db.Integer, primary_key=True)
    id_pessoa_moderador = db.Column(db.Integer, db.ForeignKey("moderador.id_pessoa"), nullable=False)
    titulo = db.Column(db.Text, nullable=False)
    corpo = db.Column(db.Text, nullable=False)
    fonte = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.Text, nullable=False)

    moderador = db.relationship("Moderador", back_populates="conteudos")

    def resumir(self, limite=170):
        texto = texto_puro(self.corpo)
        if len(texto) <= limite:
            return texto
        return texto[:limite].rsplit(" ", 1)[0] + "..."

    def tempo_leitura(self):
        # considerando umas 200 palavras por minuto
        palavras = len(texto_puro(self.corpo).split())
        return max(1, math.ceil(palavras / 200))

    def icone(self):
        return ICONES_CATEGORIA.get(self.categoria, "bi-journal-text")
