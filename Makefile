
PORT=5000
MONGO_DB=MOCK
COLLECTION_API=apis
COLLECTION_RESPONSE=responses
COLLECTION_DEVICE=devices
MONGO_CONNECTION=mongodb://localhost:27017/
PYTHON_PATH=/home/andru1236/mock/mock-backend/pyenv/bin/python # CHANGE DEPEND OF YOUR LOCAL PATH

start: run

install:
	/usr/bin/python3 -m venv pyenv
	pyenv/bin/pip install -r requirements-docker.txt;
	pyenv/bin/pip install -r requirements-dev.txt;

run:
	PORT=$(PORT) \
	MONGO_DB=$(MONGO_DB) \
	COLLECTION_RESPONSE=$(COLLECTION_RESPONSE) \
	COLLECTION_API=$(COLLECTION_API) \
	COLLECTION_DEVICE=$(COLLECTION_DEVICE) \
	MONGO_CONNECTION=$(MONGO_CONNECTION) \
	pyenv/bin/python src/main.py

ipython:
	pyenv/bin/pip install jedi==0.17.2
	cd src; \
	PYTHON_PATH=$(PYTHON_PATH) \
	PORT=$(PORT) \
	DB_NAME_MONGO=$(DB_NAME_MONGO) \
	MONGO_CONNECTION=$(MONGO_CONNECTION) \
	COLLECTION_RESPONSE=$(COLLECTION_RESPONSE) \
	COLLECTION_API=$(COLLECTION_API) \
	COLLECTION_DEVICE=$(COLLECTION_DEVICE) \
	../pyenv/bin/ipython


clean: clean-pyc clean-env

clean-pyc:
	find . -type d -name '__pycache__' -exec rm -rf {} \; || exit 0
	find . -type f -iname '*.pyc' -delete || exit 0

clean-env:
	rm -rf pyenv;

test:
	pyenv/bin/pytest -vv


.PHONY: install start clean