FROM python:3.6
WORKDIR /app
COPY requirements-docker.txt /app
RUN pip install -r requirements-docker.txt

COPY src /app

ENV PORT=5000
ENV DB_NAME_MONGO=API_MOCK
ENV MONGO_CONNECTION=mongodb://localhost:27017/

CMD ["python", "main.py"]

