# ----- Stage 1: Build das dependencias -----
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# ----- Stage 2: Imagem final -----
FROM python:3.11-slim

WORKDIR /Django

ENV PYTHONUNBUFFERED=1

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000


CMD ["gunicorn", "GerOndApp.wsgi:application", "--bind", "0.0.0.0:8000"]
