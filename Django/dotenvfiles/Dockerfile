# ----- Stclear


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

CMD ["gunicorn", "GerOndApp.wsgi:application", "--bind", "0.0.0.0:8000"]
