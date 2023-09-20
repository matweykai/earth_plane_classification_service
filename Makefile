CALL_CMD=PYTHONPATH=. python
ACTIVATE_VENV=source .venv/bin/activate

export API_PORT = 5000
export HOST = 0.0.0.0

SHELL := /bin/bash
.ONESHELL:

check_linter:
	$(ACTIVATE_VENV)
	flake8 src

run_server:
	$(ACTIVATE_VENV)
	$(CALL_CMD) app.py

run_tests:
	$(ACTIVATE_VENV)
	$(CALL_CMD) -m pytest tests