PYTHON = .venv/bin/python
PIP = .venv/bin/pip
PYTHONPATH = src

.PHONY: setup run test lint format check clean fclean re

setup:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

run:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/main.py

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check src tests scripts

fix:
	$(PYTHON) -m ruff check src tests scripts --fix

format:
	$(PYTHON) -m ruff format src tests scripts

check: lint test
	$(PYTHON) -m ruff format --check src tests scripts

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

fclean: clean
	rm -rf .venv
	rm -rf *.egg-info
	rm -rf src/*.egg-info

re: fclean setup

.PHONY: release build-release

release:
	$(PYTHON) scripts/release.py request

build-release:
	$(PIP) install -e ".[release]"
	$(PYTHON) scripts/release.py build
