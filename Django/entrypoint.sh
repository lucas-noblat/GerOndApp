#!/bin/sh
# entrypoint.sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn GerOndApp.wsgi:application --bind 0.0.0.0:8000
