.PHONY: help install install-dev clean test lint format run examples setup

help:
	@echo "DOU Scraper - Makefile Commands"
	@echo ""
	@echo "Instalação:"
	@echo "  make install      - Instala dependências básicas"
	@echo "  make install-dev  - Instala dependências de desenvolvimento"
	@echo "  make setup        - Instala e configura o projeto"
	@echo ""
	@echo "Desenvolvimento:"
	@echo "  make lint         - Executa linter (pylint)"
	@echo "  make format       - Formata código com black"
	@echo "  make test         - Executa testes"
	@echo "  make clean        - Remove arquivos temporários"
	@echo ""
	@echo "Execução:"
	@echo "  make run          - Executa o scraper principal"
	@echo "  make examples     - Executa exemplos interativos"
	@echo ""

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

setup: install
	@echo "✓ Setup concluído!"
	@echo ""
	@echo "Próximos passos:"
	@echo "1. Leia: SETUP_GUIA.md"
	@echo "2. Configure: config/config.py"
	@echo "3. Execute: make run"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	@echo "✓ Limpeza concluída"

lint:
	@echo "Executando pylint..."
	pylint src/ config/ main.py exemplos.py || true

format:
	@echo "Formatando código com black..."
	black src/ config/ main.py exemplos.py

test:
	@echo "Executando testes..."
	pytest -v || true

run:
	python main.py

examples:
	python exemplos.py

.DEFAULT_GOAL := help
