API_REST_PORT=5000
GRPC_PORT=5001
MONGO_DB=MOCK
COLLECTION_API=apis
COLLECTION_RESPONSE=responses
COLLECTION_DEVICE=devices
MONGO_CONNECTION=mongodb://localhost:27017/
PYTHON_PATH=/home/andru1236/mock/mock-backend/pyenv/bin/python # CHANGE DEPEND OF YOUR LOCAL PATH
# Docker
IMAGE_NAME_BE?=mock-backend
CONTAINER_NAME_BE_REST_API?=mock-backend-rest-container
CONTAINER_NAME_BE_GRPC?=mock-backend-grpc-container

start: run-rest

install:
	/usr/bin/python3 -m venv pyenv
	pyenv/bin/pip install --upgrade pip
	pyenv/bin/python -m pip install --upgrade setuptools
	pyenv/bin/pip install -r requirements-dev.txt;
	pyenv/bin/pip install -r requirements-docker.txt;

run-rest:
	API_REST_PORT=$(API_REST_PORT) \
	MONGO_DB=$(MONGO_DB) \
	COLLECTION_RESPONSE=$(COLLECTION_RESPONSE) \
	COLLECTION_API=$(COLLECTION_API) \
	COLLECTION_DEVICE=$(COLLECTION_DEVICE) \
	MONGO_CONNECTION=$(MONGO_CONNECTION) \
	PYTHON_PATH=$(PYTHON_PATH) \
	pyenv/bin/python src/run_api_rest.py

run-grpc:
	API_REST_PORT=$(API_REST_PORT) \
	GRPC_PORT=$(GRPC_PORT) \
	MONGO_DB=$(MONGO_DB) \
	COLLECTION_RESPONSE=$(COLLECTION_RESPONSE) \
	COLLECTION_API=$(COLLECTION_API) \
	COLLECTION_DEVICE=$(COLLECTION_DEVICE) \
	MONGO_CONNECTION=$(MONGO_CONNECTION) \
	PYTHON_PATH=$(PYTHON_PATH) \
	pyenv/bin/python src/run_grpc_server.py

ipython:
	pyenv/bin/pip install jedi==0.17.2
	cd src; \
	PYTHON_PATH=$(PYTHON_PATH) \
	API_REST_PORT=$(API_REST_PORT) \
	MONGO_DB=$(MONGO_DB) \
	MONGO_CONNECTION=$(MONGO_CONNECTION) \
	COLLECTION_RESPONSE=$(COLLECTION_RESPONSE) \
	COLLECTION_API=$(COLLECTION_API) \
	COLLECTION_DEVICE=$(COLLECTION_DEVICE) \
	../pyenv/bin/ipython


clean: clean-pyc clean-pytest clean-env

clean-pyc:
	find . -type d -name '__pycache__' -exec rm -rf {} \; || exit 0
	find . -type f -iname '*.pyc' -delete || exit 0

clean-env:
	rm -rf pyenv;

clean-pytest:
	rm -rf .pytest_cache

gen-proto:
	cd src; ../pyenv/bin/python -m grpc.tools.protoc -I.  --python_out=. --grpc_python_out=. ./gateway/protocol_buffers/generated_files/simulator_services.proto         

test:
	pyenv/bin/pytest -vv

docker-build:
	docker-compose -f docker/docker-compose.yml build --no-cache

docker-start:
	docker-compose -f docker/docker-compose.yml up 

docker-clean:
	docker-compose -f docker/docker-compose.yml down
	docker rmi ${IMAGE_NAME_BE}


.PHONY: install start clean
