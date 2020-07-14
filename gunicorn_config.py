command = '/usr/bin/gunicorn'
pythonpath = '/app/dinner_time'
bind = "0.0.0.0:8000"
workers = 3
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=dinner_time.backend_settings.settings'