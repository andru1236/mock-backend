
PORT=5000
DB_NAME_MONGO=API_MOCK
MONGO_CONNECTION=mongodb://localhost:27017/

start: run

install:
	/usr/bin/python3 -m venv pyenv
	pyenv/bin/pip install -r requirements-docker.txt;

run:
	PORT=$(PORT) DB_NAME_MONGO=$(DB_NAME_MONGO) MONGO_CONNECTION=$(MONGO_CONNECTION) pyenv/bin/python src/main.py

clean: clean-pyc clean-env

clean-pyc:
	find . -type d -name '__pycache__' -exec rm -rf {} \; || exit 0
	find . -type f -iname '*.pyc' -delete || exit 0

clean-env:
	rm -rf pyenv;

test:
	pyenv/bin/pytest -vv


.PHONY: install start clean