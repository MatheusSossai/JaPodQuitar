"""Instancias unicas das extensoes do Flask.

Ficam isoladas neste modulo para evitar importacao circular entre a fabrica
da aplicacao e os modelos de persistencia.
"""

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
gerenciador_login = LoginManager()
