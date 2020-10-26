FROM python:3.6-alpine
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*
WORKDIR /app
COPY requirements-docker.txt /app
RUN pip install -r requirements-docker.txt

COPY src /app

CMD ["python", "main.py"]

