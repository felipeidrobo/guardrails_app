FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ARG GUARDRAILS_TOKEN

RUN guardrails configure --enable-metrics --enable-remote-inferencing --token ${GUARDRAILS_TOKEN}

RUN guardrails hub install hub://guardrails/toxic_language --quiet

COPY . .

EXPOSE 8080

CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
