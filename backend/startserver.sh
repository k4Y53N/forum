#!/bin/sh
python3 manage.py migrate --run-sync
gunicorn base.wsgi --bind 0.0.0.0:8000