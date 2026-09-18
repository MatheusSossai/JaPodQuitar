"""Camada de persistencia: mapeamento objeto-relacional das tabelas do DER.

Segue o modelo logico da secao 5.2:
- PESSOA -> USUARIO / MODERADOR: heranca por tabelas separadas (joined);
- REGISTRO_DIARIO -> SINTOMA / RECAIDA / CONQUISTA: heranca joined;
- MISSAO: tabela unica com discriminador (tipo_missao);
- PROGRAMA_MISSAO: resolve o N:N e materializa a fila (posicao_fila).
"""

from app.modelos.pessoa_modelo import PessoaModelo, UsuarioModelo, ModeradorModelo
from app.modelos.programa_modelo import ProgramaCessacaoModelo
from app.modelos.missao_modelo import MissaoModelo, ProgramaMissaoModelo
from app.modelos.registro_modelo import (
    RegistroDiarioModelo,
    RegistroSintomaModelo,
    RegistroRecaidaModelo,
    RegistroConquistaModelo,
)
from app.modelos.conteudo_modelo import ConteudoInformativoModelo

__all__ = [
    "PessoaModelo",
    "UsuarioModelo",
    "ModeradorModelo",
    "ProgramaCessacaoModelo",
    "MissaoModelo",
    "ProgramaMissaoModelo",
    "RegistroDiarioModelo",
    "RegistroSintomaModelo",
    "RegistroRecaidaModelo",
    "RegistroConquistaModelo",
    "ConteudoInformativoModelo",
]
