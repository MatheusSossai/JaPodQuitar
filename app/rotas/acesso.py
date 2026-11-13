from functools import wraps
from urllib.parse import urlsplit

from flask import abort
from flask_login import current_user, login_required


def perfil_requerido(perfil):
    """Libera a rota só para quem está logado com o perfil indicado ('usuario' ou 'moderador')."""

    def decorador(funcao):
        @wraps(funcao)
        @login_required
        def verificar(*args, **kwargs):
            if current_user.perfil_acesso() != perfil:
                abort(403)
            return funcao(*args, **kwargs)

        return verificar

    return decorador


def usuario_logado():
    # o current_user é um proxy; para o SQLAlchemy precisa ser o objeto de verdade
    return current_user._get_current_object()


def destino_seguro(url):
    """Evita redirecionar para outro site depois do login (open redirect)."""
    if not url or not url.startswith("/") or url.startswith("//") or "\\" in url:
        return False
    return urlsplit(url).netloc == ""
