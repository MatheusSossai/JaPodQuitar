"""Operacoes comuns a todos os repositorios."""

from app.extensions import db


class RepositorioBase:
    modelo = None

    def buscar_por_id(self, identificador):
        return db.session.get(self.modelo, identificador)

    def listar_todos(self) -> list:
        return db.session.query(self.modelo).all()

    def salvar(self, entidade):
        db.session.add(entidade)
        db.session.commit()
        return entidade

    def remover(self, entidade) -> None:
        db.session.delete(entidade)
        db.session.commit()
