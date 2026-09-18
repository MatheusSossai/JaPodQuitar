"""Consultas de PESSOA / USUARIO / MODERADOR."""

from app.modelos import PessoaModelo, UsuarioModelo
from app.repositorios.repositorio_base import RepositorioBase


class RepositorioUsuario(RepositorioBase):
    modelo = UsuarioModelo

    def buscar_por_email(self, email: str):
        """TODO (Sprint 1): consulta usada no login (RF01)."""
        raise NotImplementedError

    def email_ja_cadastrado(self, email: str) -> bool:
        """TODO (Sprint 1): valida a unicidade exigida pela UK de PESSOA."""
        raise NotImplementedError

    def excluir_conta_e_historico(self, id_pessoa: int) -> None:
        """TODO (Sprint 4): exclusao total prevista no RF12 e no RN05."""
        raise NotImplementedError
