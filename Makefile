PYTHON ?= python

.PHONY: install run test lint

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) -m uvicorn app.main:app --reload

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check .
