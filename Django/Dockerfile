# ----- Stage 1: Build das dependências -----
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# ----- Stage 2: Imagem final -----
FROM python:3.11-slim

WORKDIR /gerondapp

ENV PYTHONUNBUFFERED=1

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

COPY . .

RUN pip install gunicorn

# Coleta dos estáticos
RUN python manage.py collectstatic --no-input


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
