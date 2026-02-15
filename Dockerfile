FROM python:3.11-slim

WORKDIR /app

COPY python/builder_client.py .

CMD ["python", "builder_client.py"]