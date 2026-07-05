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
	$(PYTHON) -m ruff check src tests

fix:
	$(PYTHON) -m ruff check src tests --fix

format:
	$(PYTHON) -m ruff format src tests

check: lint test

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

.PHONY: bump-patch bump-minor bump-major publish-version

bump-patch:
	$(PYTHON) scripts/bump_version.py patch

bump-minor:
	$(PYTHON) scripts/bump_version.py minor

bump-major:
	$(PYTHON) scripts/bump_version.py major

publish-version:
	$(PYTHON) scripts/publish_version.py --push
