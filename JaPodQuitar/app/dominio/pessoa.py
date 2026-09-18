"""Hierarquia Pessoa -> Usuario / Moderador (heranca e polimorfismo)."""

from abc import ABC, abstractmethod
from datetime import date


class Pessoa(ABC):
    """Classe abstrata comum a todos os perfis da plataforma."""

    def __init__(self, id: int | None, nome: str, email: str, senha_hash: str) -> None:
        self.id = id
        self.nome = nome
        self.email = email
        self._senha_hash = senha_hash

    @property
    def senha_hash(self) -> str:
        """Somente leitura: senha nunca trafega em texto puro (RNF03)."""
        return self._senha_hash

    def autenticar(self, senha: str) -> bool:
        """Compara a senha informada com o hash armazenado.

        TODO (Sprint 1): usar check_password_hash do Werkzeug.
        """
        raise NotImplementedError

    @abstractmethod
    def exibir_painel(self) -> str:
        """Nome da rota/painel inicial do perfil."""

    @abstractmethod
    def perfil_acesso(self) -> str:
        """Identificador do nivel de acesso ('usuario' ou 'moderador')."""


class Usuario(Pessoa):
    """Pessoa que usa a plataforma para reduzir ou cessar o uso de POD."""

    def __init__(
        self,
        id: int | None,
        nome: str,
        email: str,
        senha_hash: str,
        data_inicio: date | None = None,
        consumo_anterior: int = 0,
        custo_semanal: float = 0.0,
        nivel_dependencia: str = "nao informado",
    ) -> None:
        super().__init__(id, nome, email, senha_hash)
        self.data_inicio = data_inicio
        self.consumo_anterior = consumo_anterior
        self.custo_semanal = custo_semanal
        self.nivel_dependencia = nivel_dependencia

    def exibir_painel(self) -> str:
        return "painel.inicio"

    def perfil_acesso(self) -> str:
        return "usuario"

    def calcular_economia(self, dias_sem_nicotina: int) -> float:
        """RN08: (dias sem nicotina / 7) x custo semanal anterior.

        TODO (Sprint 4): mover o arredondamento para a camada de apresentacao.
        """
        return (dias_sem_nicotina / 7) * self.custo_semanal

    def dias_sem_nicotina(self) -> int:
        """Dias consecutivos desde o ultimo registro de recaida (RN06).

        TODO (Sprint 4): delegar ao ServicoMetricas, que consulta o diario.
        """
        raise NotImplementedError


class Moderador(Pessoa):
    """Profissional de saude ou educador responsavel pelo conteudo (RN10)."""

    def __init__(
        self,
        id: int | None,
        nome: str,
        email: str,
        senha_hash: str,
        registro_prof: str = "",
        area_atuacao: str = "",
    ) -> None:
        super().__init__(id, nome, email, senha_hash)
        self.registro_prof = registro_prof
        self.area_atuacao = area_atuacao

    def exibir_painel(self) -> str:
        return "moderacao.inicio"

    def perfil_acesso(self) -> str:
        return "moderador"

    def publicar(self, conteudo) -> None:
        """Publica um ConteudoInformativo; exige o campo fonte (RN10/RNF05).

        TODO (Sprint 2): validar fonte e delegar ao ServicoConteudo.
        """
        raise NotImplementedError
