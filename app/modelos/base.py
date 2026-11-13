from abc import ABCMeta

from app.extensoes import db


class ModeloAbstratoMeta(type(db.Model), ABCMeta):
    """Metaclasse que junta a do SQLAlchemy com a ABCMeta.

    Sem isso não dá para usar @abstractmethod nos modelos, porque o db.Model
    já tem uma metaclasse própria e o Python reclama de conflito.
    Com ela, tentar instanciar Pessoa, Missao ou RegistroDiario direto gera TypeError.
    """
