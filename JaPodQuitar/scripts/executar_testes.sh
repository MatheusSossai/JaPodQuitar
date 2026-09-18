#!/usr/bin/env bash
# Roda a suite de testes com relatorio de cobertura das regras de negocio.
set -e
pytest --cov=app --cov-report=term-missing
