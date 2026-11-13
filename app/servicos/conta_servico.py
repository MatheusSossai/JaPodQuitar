"""Cadastro, login, perfil de consumo e direitos da LGPD (exportar e excluir)."""
from datetime import datetime

from app.excecoes import RegraNegocioErro
from app.extensoes import db
from app.modelos import Pessoa, Usuario
from app.opcoes import NIVEIS_DEPENDENCIA
from app.validacao import decimal, email as validar_email, escolha, inteiro, texto_obrigatorio

TAMANHO_MINIMO_SENHA = 8


def _validar_senha(senha, confirmacao):
    if len(senha or "") < TAMANHO_MINIMO_SENHA:
        raise RegraNegocioErro(f"A senha precisa ter pelo menos {TAMANHO_MINIMO_SENHA} caracteres.")
    if senha != confirmacao:
        raise RegraNegocioErro("A confirmação não bate com a senha digitada.")


def _email_em_uso(email):
    return db.session.scalar(db.select(Pessoa.id_pessoa).where(Pessoa.email == email)) is not None


def cadastrar_usuario(nome, email, senha, confirmacao, consentiu):
    nome = texto_obrigatorio(nome, "nome", 60)
    email = validar_email(email)
    _validar_senha(senha, confirmacao)
    # RNF04: consentimento explícito no cadastro
    if not consentiu:
        raise RegraNegocioErro("Para criar a conta você precisa concordar com a política de privacidade.")
    if _email_em_uso(email):
        raise RegraNegocioErro("Já existe uma conta com esse e-mail.")

    usuario = Usuario(nome=nome, email=email, data_consentimento=datetime.now())
    usuario.definir_senha(senha)
    db.session.add(usuario)
    db.session.commit()
    return usuario


def autenticar(email, senha):
    email = (email or "").strip().lower()
    pessoa = db.session.scalar(db.select(Pessoa).where(Pessoa.email == email))
    if pessoa is not None and pessoa.autenticar(senha):
        return pessoa
    return None


def salvar_perfil_consumo(usuario, dados):
    # RF03: transforma o hábito em números para os cálculos do painel
    consumo = inteiro(dados.get("consumo_diario_anterior"), "puffs por dia", 0, 5000)
    custo = decimal(dados.get("custo_semanal_anterior"), "gasto por semana", 0, 10000)
    nivel = escolha(dados.get("nivel_dependencia"), NIVEIS_DEPENDENCIA, "nível de dependência")
    tempo = inteiro(dados.get("tempo_uso_meses"), "tempo de uso", 0, 600)

    usuario.consumo_diario_anterior = consumo
    usuario.custo_semanal_anterior = custo
    usuario.nivel_dependencia = nivel
    usuario.tempo_uso_meses = tempo
    db.session.commit()
    return usuario


def alterar_nome(pessoa, nome):
    pessoa.nome = texto_obrigatorio(nome, "nome", 60)
    db.session.commit()


def alterar_senha(pessoa, senha_atual, nova, confirmacao):
    if not pessoa.autenticar(senha_atual):
        raise RegraNegocioErro("A senha atual está incorreta.")
    _validar_senha(nova, confirmacao)
    pessoa.definir_senha(nova)
    db.session.commit()


def exportar_dados(usuario):
    """RF12: tudo o que o sistema guarda sobre a pessoa, em formato aberto (JSON)."""
    return {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "conta": {
            "nome": usuario.nome,
            "email": usuario.email,
            "data_cadastro": usuario.data_cadastro.isoformat(timespec="seconds"),
            "data_consentimento": (
                usuario.data_consentimento.isoformat(timespec="seconds") if usuario.data_consentimento else None
            ),
        },
        "perfil_consumo": {
            "puffs_por_dia": usuario.consumo_diario_anterior,
            "gasto_semanal": usuario.custo_semanal_anterior,
            "nivel_dependencia": usuario.nivel_dependencia,
            "tempo_uso_meses": usuario.tempo_uso_meses,
            "data_inicio_abstinencia": (
                usuario.data_inicio_abstinencia.isoformat() if usuario.data_inicio_abstinencia else None
            ),
        },
        "programas": [programa.para_dict() for programa in usuario.programas],
    }


def excluir_conta(usuario, senha, confirmou):
    """RF12 e RN05: a única forma de apagar o diário é excluindo a conta inteira."""
    if not confirmou:
        raise RegraNegocioErro("Marque a caixa confirmando que você entende que a exclusão é definitiva.")
    if not usuario.autenticar(senha):
        raise RegraNegocioErro("Senha incorreta. A conta não foi excluída.")
    # o cascade da composição apaga programas, fila e registros junto
    db.session.delete(usuario)
    db.session.commit()
