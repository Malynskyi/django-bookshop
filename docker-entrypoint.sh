#!/bin/sh

echo "Waiting for PostgreSQL..."

# while ! nc -z db 5432; do
#   sleep 1
# done

# echo "PostgreSQL is up"

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn db_django_proj.wsgi:application --bind 0.0.0.0:8000