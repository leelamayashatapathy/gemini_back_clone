#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py makemigrations --noinput || echo "makemigrations failed"
python manage.py migrate --noinput 