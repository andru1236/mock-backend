FROM python:3.6
WORKDIR /app
COPY requirements-docker.txt /app
RUN pip install -r requirements-docker.txt

COPY src /app

EXPOSE 3000-9999
CMD ["python", "main.py"]

