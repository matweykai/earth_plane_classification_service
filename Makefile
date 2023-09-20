CALL_CMD=PYTHONPATH=. python
ACTIVATE_VENV=source .venv/bin/activate

SHELL := /bin/bash
.ONESHELL:

check_linter:
	$(ACTIVATE_VENV)
	flake8 src