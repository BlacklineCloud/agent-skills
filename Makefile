PYTHON ?= python3

.PHONY: install-dev lint test validate check

install-dev:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .[dev]

lint:
	$(PYTHON) -m ruff check .

test:
	$(PYTHON) -m pytest

validate:
	$(PYTHON) scripts/repo_manager.py validate-all

check: lint test validate

