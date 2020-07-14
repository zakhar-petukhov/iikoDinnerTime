#!/usr/bin/env bash

python dinner_time/manage.py makemigrations && dinner_time/manage.py migrate && dinner_time/manage.py collectstatic --no-input
gunicorn -c gunicorn_config.py dinner_time.backend_settings.wsgi