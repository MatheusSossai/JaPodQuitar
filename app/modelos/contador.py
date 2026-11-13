from app.extensoes import db


class ContadorAcesso(db.Model):
    """Contadores anônimos usados nos indicadores da seção 2.3.

    Não guarda nada sobre quem acessou, só o total por chave.
    """

    __tablename__ = "contador_acesso"

    chave = db.Column(db.Text, primary_key=True)
    total = db.Column(db.Integer, nullable=False, default=0)
