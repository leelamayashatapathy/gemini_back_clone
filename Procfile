web: gunicorn gemini_backend.wsgi:application
worker: celery -A gemini_backend worker --loglevel=info 