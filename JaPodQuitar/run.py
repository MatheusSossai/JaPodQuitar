"""Ponto de entrada da aplicacao Ja Pod Quitar.

Execucao local:
    python run.py
ou
    flask --app run.py run --debug
"""

from app import criar_app

app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
