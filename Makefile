CALL_CMD=PYTHONPATH=. python
ACTIVATE_VENV=source .venv/bin/activate

export API_PORT = 5000
export HOST = 0.0.0.0

SHELL := /bin/bash
.ONESHELL:

setup:
	python3 -m venv .venv
	$(ACTIVATE_VENV) && \

	pip install -r requirements.txt

pull_weights:
	$(ACTIVATE_VENV)
	dvc pull -R weights

check_linter:
	$(ACTIVATE_VENV)
	flake8 src

run_server:
	$(ACTIVATE_VENV)
	$(CALL_CMD) app.py

run_tests:
	$(ACTIVATE_VENV)
	$(CALL_CMD) -m pytest tests

run_docker:
	docker build -t forest_service .
	docker run -p $(API_PORT):$(API_PORT) -d --name forest_container forest_service

stop_docker:
	docker stop forest_container
	docker container rm forest_container
