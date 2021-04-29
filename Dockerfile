FROM python:3.9-alpine
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*
WORKDIR /app
COPY requirements-docker.txt /app
RUN pip install -r requirements-docker.txt

COPY src /app

CMD ["python", "run_api_rest.py"]

