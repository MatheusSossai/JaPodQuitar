"""Cadastro, login e controle de perfil (RF01, RNF03)."""

from werkzeug.security import check_password_hash, generate_password_hash

from app.repositorios.repositorio_usuario import RepositorioUsuario


class ServicoAutenticacao:
    def __init__(self, repositorio: RepositorioUsuario | None = None) -> None:
        self.repositorio = repositorio or RepositorioUsuario()

    def cadastrar(self, nome: str, email: str, senha: str, consentimento: bool):
        """TODO (Sprint 1): exigir consentimento explicito (RNF04) e gravar
        apenas o hash da senha (RNF03)."""
        raise NotImplementedError

    def autenticar(self, email: str, senha: str):
        """TODO (Sprint 1): validar credenciais com check_password_hash."""
        raise NotImplementedError

    @staticmethod
    def gerar_hash(senha: str) -> str:
        return generate_password_hash(senha)
