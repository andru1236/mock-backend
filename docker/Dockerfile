FROM python:3.9
RUN apt-get install gcc libc-dev 
WORKDIR /app
COPY requirements-docker.txt /app

RUN pip install --upgrade pip
RUN	python -m pip install --upgrade setuptools
RUN pip install -r requirements-docker.txt

COPY src /app

CMD ["python", "run_api_rest.py"]

