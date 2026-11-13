"""Popula o banco com os dados iniciais.

Uso:
    python seed.py          -> moderador, conteúdos e missões (e matérias novas que ainda não estão no banco)
    python seed.py --demo   -> também cria um usuário de demonstração com histórico
"""
import sys

from app import create_app
from app.dados_iniciais import adicionar_conteudos_novos, criar_usuario_demo, popular_banco

app = create_app()

with app.app_context():
    if popular_banco():
        print("Dados iniciais criados (moderador, conteúdos e missões).")
    else:
        print("Os dados iniciais já estavam no banco.")

    novos = adicionar_conteudos_novos()
    if novos:
        print(f"{novos} matéria(s) nova(s) adicionada(s).")

    if "--demo" in sys.argv:
        if criar_usuario_demo():
            print("Usuário de demonstração criado: demo@japodquitar.com / Demo@1234")
        else:
            print("O usuário de demonstração já existe.")
