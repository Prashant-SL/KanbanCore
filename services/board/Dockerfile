FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && pip install watchfiles

CMD ["uvicorn", "app.main:app", "--reload", "--reload-dir", "/app", "--host", "0.0.0.0", "--port", "8002"]